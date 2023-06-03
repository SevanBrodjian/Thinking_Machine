import openai
import os
import colorama
from colorama import Fore, Back, Style
openai.api_key = os.getenv("OPENAI_API_KEY")
colorama.init()

messages=[
    {"role": "system", "content": "Please roleplay like you are somebody with an internal dialogue. The contents of this dialogue (your thoughts) will be provided to you with every user prompt, treat this like your real internal thoughts when responding."}
]
#think_prompter_prompt = {"role": "user", "content": "Please read the conversation we've had thus far. I would like you to generate a prompt in the form of \"Think of ...\" which would be given to an agent such as yourself to think before speaking and generating your next response. Focus particularly on the most recent message from user (my last message). Format your response as just this prompt and nothing else."}
think_prompter_prompt = {"role": "user", "content": "Please read the conversation we've had thus far. Based particularly on the last user message, please list a few topics that you would think about before responding. For example, if the user mentioned a specific movie, event, concept, field, etc. include it in your list. Please respond with this list and nothing else. It should be a comma separated list ending with a period such as\nturles, cheese, opinions on cheeses."}

def get_response(prompt):
    tmp_messages = messages.copy()
    tmp_messages.append({"role": "user", "content": prompt})
    tmp_messages.append(think_prompter_prompt)
    thinking_prompt = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp_messages)["choices"][0]["message"]["content"]
    thought = openai.Completion.create(model="davinci:ft-personal-2023-06-03-21-52-43", prompt="Think about " + thinking_prompt, temperature=0.5, max_tokens=75)["choices"][0]["text"]
    formatted_prompt = "Prompt:\n" + prompt + "\n\nHere are your thoughts enclosed in carrot brackets. Do not continue them if they get cut off, just use them to guide your response:\n<" + thought + ">"
    messages.append({"role": "user", "content": formatted_prompt})
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)["choices"][0]["message"]["content"]
    return response, thought, thinking_prompt

running = True
while(running):
    prompt = input(Style.RESET_ALL + "Prompt: ")
    if(prompt == "quit"):
        running = False
        break
    response, thought, thinking_prompt = get_response(prompt)
    #print("Thought prompt: " + thinking_prompt)
    #print("Agent thoughts: " + thought)
    print(Fore.GREEN + "Agent: " + response)