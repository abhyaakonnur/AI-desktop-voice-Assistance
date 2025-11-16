import traceback
from openai import OpenAI

try:
    client = OpenAI()
    print('OpenAI client created:', type(client))
except Exception:
    print('EXCEPTION OCCURRED')
    traceback.print_exc()
