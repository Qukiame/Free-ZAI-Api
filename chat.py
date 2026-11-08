from openai import OpenAI

MODEL_NAME = "x-preview-l" 
# You could insert a different model here;
# I used this one because it was the only one that worked for me.

SYSTEM_PROMPT = "ur prompt"

client = OpenAI(base_url="http://127.0.0.1:8492/v1", api_key="sk-nothing")

messages = []

if SYSTEM_PROMPT:
    messages.append({"role": "system", "content": SYSTEM_PROMPT})

print(f"chat from {MODEL_NAME} has started.")
print("write answer (exit from exit):")

while True:
    q = input("\nYou: ")
    if q.lower() == "exit":
        break
    
    messages.append({"role": "user", "content": q})
    
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        
        answer = resp.choices[0].message.content
        print(f"GLM: {answer}")
        
        messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        print(f"\n[Error]: {e}")
        messages.pop()
