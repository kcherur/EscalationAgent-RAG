from tools.email_tool import send_alert_email


def evaluate_and_act(user_id, extracted_json):
    """
    Applies business rules and triggers tools.
    """

    if not extracted_json:
        return

    sentiment = extracted_json.get("sentiment")
    confidence = extracted_json.get("confidence", 0)
    product = extracted_json.get("product")
    category = extracted_json.get("category")
    summary = extracted_json.get("issue_summary")

    # Rule 1: Trigger alert only for strong negative complaints
    if sentiment == "Negative" and confidence >= 0.7:
        send_alert_email(user_id, product, category, summary)