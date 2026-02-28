from concurrent.futures import thread
import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path
import asyncio
from azure.identity import AzureCliCredential, DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import pandas as pd


# Add references


async def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Display the data to be analyzed
    script_dir = Path(__file__).parent  # Get the directory of the script
    file_path = script_dir / 'data/data.txt'

    with file_path.open('r') as file:
        data = file.read() + "\n"
        print(data)


    # Connect to the AI Project and OpenAI clients
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

   
        # Upload the data file and create a CodeInterpreterTool
    script_dir = Path(__file__).parent  # Get the directory of the script
    file_path_order = script_dir / 'data/orders.csv'
    file_path_reviews = script_dir / 'data/reviews.csv'
    orders_df = pd.read_csv(file_path_order)
    reviews_df = pd.read_csv(file_path_reviews)

# Create dictionary: user -> purchased products
    user_orders = (
        orders_df.groupby("user_id")["product_name"]
        .apply(list)
        .to_dict()
    )

    print(user_orders)    
    row = reviews_df.iloc[0]

    user_id = row["user_id"]
    review_text = row["review_text"]
    purchased_products = user_orders.get(user_id, [])

    prompt = f"""
    User ID: {user_id}
    Purchased Products: {purchased_products}
    Review: "{review_text}"

    Tasks:
    1. Identify which purchased product is discussed.
    2. Determine sentiment.
    3. Extract complaint theme.

    Return ONLY valid JSON like:
    {{
     "user_id": "...",
    "product": "...",
    "sentiment": "...",
    "issue": "..."
    }}
    """
    thread = project_client.agents.threads.create()
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Run status: {run.status}")
    run = project_client.agents.runs.get(
    thread_id=thread.id,
    run_id=run.id   
    )
    messages = project_client.agents.messages.list(
    thread_id=thread.id
    )

    for msg in messages:
        if msg.role == "assistant":
            print("Assistant:", msg.content[0].text.value)


    # messages.create()
    # runs.create()
    # poll
    # messages.list()
        # Define an agent that uses the CodeInterpreterTool
        

        # Create a conversation for the chat session
        

        # Loop until the user types 'quit'
    while True:
            # Get input text
            user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Please enter a prompt.")
                continue

            # Send a prompt to the agent
            

            # Check the response status for failures
            

            # Show the latest response from the agent
            

        # Get the conversation history


        # Clean up


if __name__ == '__main__': 
    asyncio.run(main())