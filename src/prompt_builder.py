from config import CATEGORIES

def build_prompt(review_text: str) -> str:

    categories_text = "\n".join(CATEGORIES)

    prompt = f"""
    Extract the following fields from the review:

    - product
    - sentiment (Positive or Negative or Mixed)
    - category (choose ONLY one from the list below)
    - issue_summary
    - confidence (0-1)

    Categories:
    {categories_text}

    Review:
    {review_text}

    Return output strictly in JSON.
    """

    return prompt