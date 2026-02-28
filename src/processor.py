from itertools import product
from unicodedata import category

import pandas as pd
from prompt_builder import build_prompt
from agent_runner import run_agent
from decision_engine import evaluate_and_act
from embeddings import generate_embedding
from vector_store import search_similar_reviews, upload_review_document

def process_reviews(review_df: pd.DataFrame,orders_df: pd.DataFrame, project_client, agent_id) -> pd.DataFrame:

    structured_rows = []
     # Create lookup dictionary: user_id → product
    #user_product_map = dict(zip(review_df["user_id"], orders_df["product_name"]))
    thread = project_client.agents.threads.create()
    #print(thread.id)
    for _, row in review_df.iterrows():
        user_id = row["user_id"]

        # Get product from orders mapping
        product =orders_df.get("user_id")
        #product = user_product_map.get(user_id, "Unknown")
        review_text = row["review_text"]
        prompt = build_prompt(review_text)
        extracted = run_agent(project_client, agent_id, thread.id,prompt)
        #print(extracted)
        # Safety check
        if not isinstance(extracted, dict):
            print(f"Invalid agent response for user {user_id}")
        else:
            product= extracted.get("product")      
            category = extracted.get("category")
            summary = extracted.get("issue_summary")
            # Create embedding text
            rag_text = f"{product} {category} {summary}"
            #print(f"RAG text for embedding: {rag_text}")
            embedding = generate_embedding(rag_text)
            # Search similar past reviews
            similar_reviews = search_similar_reviews(embedding, top_k=3)
            print(f"Found similar reviews: {len(similar_reviews)}")
            similar_count = len(similar_reviews)
            print(f"Found {similar_count} similar complaints")

# Escalate only if recurring
            if similar_count >= 2:
                evaluate_and_act(user_id, extracted)

# Upload current review to vector index
            document = {
                 "review_id": str(row.get("review_id")),
                "user_id": user_id,
                "product": product,
                "category": category,
                "issue_summary": summary,
                "embedding": embedding
            }

            upload_review_document(document)

        #evaluate_and_act(user_id, extracted)
            structured_rows.append({
                 "review_id": row.get("review_id"),
                 "user_id": row.get("user_id"),
                "review_text": review_text,
                "product": extracted.get("product"),
                "category": extracted.get("category"),
                "sentiment": extracted.get("sentiment"),
                "issue_summary": extracted.get("issue_summary"),
                "confidence": extracted.get("confidence")
                })
    print("completed the processing of reviews")
    return pd.DataFrame(structured_rows)