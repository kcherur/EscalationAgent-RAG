import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from data_loader import load_data
from processor import process_reviews
from storage import save_processed_data
from analytics import category_negative_counts
from dotenv import load_dotenv

def main():
    # Connect to the AI Project and OpenAI clients
    load_dotenv()
    project_endpoint= os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
    project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
    )
    
    agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="kch-agent1",
    instructions="You are an assistant who knows capital cities. Provide answer in 1 word."
    )
    print(f"Created agent, ID: {agent.id}")
    raw_df, user_orders = load_data()

    processed_df = process_reviews(raw_df,user_orders,project_client, agent.id)
    #print("====================================")
    #print(processed_df)
    save_processed_data(processed_df)
    #print("====================================")

    agg = category_negative_counts(processed_df)

    print("\nNegative Complaints Per Category:")
    print(agg)


if __name__ == "__main__":
    main()