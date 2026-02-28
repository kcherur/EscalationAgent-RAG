import time
import json
import re

def run_agent(project_client, agent_id,thread_id, prompt):

   # thread = project_client.agents.threads.create()
    #print("Thread ID:", thread_id)
    #print("Agent ID:", agent_id)
    project_client.agents.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = project_client.agents.runs.create(
        thread_id=thread_id,
        agent_id=agent_id
    )
   
    while run.status in ["queued", "in_progress"]:
        time.sleep(2)
        run = project_client.agents.runs.get(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = project_client.agents.messages.list(thread_id)

    for msg in messages:
        if msg.role == "assistant":
            raw_text = msg.content[0].text.value
            #print("Raw agent response:", raw_text)
            return safe_parse_json(raw_text)
        

def safe_parse_json(text: str):
    try:
        # First try normal parsing
        return json.loads(text)
    except json.JSONDecodeError:
        # Remove markdown code fences if present
        cleaned = re.sub(r"```json|```", "", text).strip()
        try:
            return json.loads(cleaned)
        except:
            # Last attempt: extract JSON block using regex
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
    return None