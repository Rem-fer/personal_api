import os
from dotenv import load_dotenv
import anthropic
import time
load_dotenv()

def generate_weekly_focus(plus, minus, next_, retries=3):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Based on last week's review, suggest a weekly focus and 3 main goals.

Plus (what went well): {plus}
Minus (what didn't): {minus}
Next (actions planned): {next_}

Return in this format:
Focus: <one sentence>
Goals:
- <goal 1>
- <goal 2>
- <goal 3>"""

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < retries - 1:
                time.sleep(5)
            else:
                raise
    return None