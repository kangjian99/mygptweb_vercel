import os
import openai

# openai.api_key = os.environ.get('OPENAI_API_KEY')
model = 'gpt-3.5-turbo' # or text-davinci-003
SESSION_SECRET_KEY = os.environ.get('SESSION_SECRET_KEY')

MONGODB_URI = os.environ.get('MONGODB_URI')

openai_api_key = os.environ.get('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"

directory = 'session_messages'