from dotenv import load_dotenv
import os

import anthropic


load_dotenv()
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

res = client.messages.create(
    # model='claude-3-5-sonnet-20241022',
    model='claude-3-haiku-20240307',
    max_tokens=1024,
    messages=[
        {'role': 'user', 'content': 'hey, how are you'},
        {'role': 'assistant', 'content': 'I am good. let us talk about blue sky'},
        {'role': 'user', 'content': 'well, tell me something about'},

    ]
)
text_answer = res.content[0].text
print(text_answer)
