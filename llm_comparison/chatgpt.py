#chatgpt
from openai import OpenAI


def call_openai(client = None, model='gpt-3.5-turbo', messages=None):
    completion = client.chat.completions.create(
        model = model,
        messages = messages
    )

    #return the latest answer
    return(completion.choices[0].message.content)

def openai_test():
    return("Yes it works")
