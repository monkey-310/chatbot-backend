import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(message, memories):
  if len(memories) == 0:
    prompt = message
  else:
    prompt = f"User's current question is: '{message}', and the user asked previously: '{" ,".join(memories)}'. Please answer the current question based on the previous questions."
    print(prompt)

  response = openai.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}]
  )

  return response.choices[0].message.content.strip()