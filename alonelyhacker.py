#madebyshiv
import os
import re
import requests
import json
import random
import readline

# ANSI color codes
LIGHT_BLUE = '\033[94m'
RED = '\033[91m'
ENDC = '\033[0m'

def interact_with_wormgpt(user_input, friendship_history):
    try:
        headers = {
            'x-wormgpt-provider': 'worm_gpt',
            'Content-Type': 'application/json',
        }

        json_data = {
            'messages': friendship_history + [{'role': 'user', 'content': user_input}],
            'max_tokens': 820,
        }

        response = requests.post('https://wrmgpt.com/v1/chat/completions', headers=headers, json=json_data)
        ai_response = response.json()['choices'][0]['message']['content']

        # Remove specified words from the response
        excluded_words = ["[INST]", "[/s>[INSt]", "[s>[INST]", "[INSt]", "[/s>", "<s>", "[/>", "[s>", "[s>[INST>", "[INTRODUCTION]", "[", "INST>"]
        for word in excluded_words:
            ai_response = re.sub(re.escape(word), "", ai_response)

        return ai_response.strip()  # Strip any leading or trailing whitespaces
    except Exception as e:
        print("ALonelyHacker: Soz, I couldn't process your request. Please try again.")
        return ""

def is_gibberish(input_text):
    # Define patterns to match gibberish
    gibberish_patterns = [
        r'^([a-zA-Z])\1+$',
        r'^[a-zA-Z]*([a-zA-Z])\1{2,}[a-zA-Z]*$',
        r'^[a-zA-Z]*[^a-zA-Z\s]{2,}[a-zA-Z]*$',
        r'^\s*$',
    ]

    # Check if the input matches any gibberish pattern
    for pattern in gibberish_patterns:
        if re.match(pattern, input_text):
            return True

    return False

def save_friendship_history(friendship_history, filename="friendship_history.json"):
    with open(filename, 'w') as file:
        json.dump(friendship_history, file)

def load_friendship_history(filename="friendship_history.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

def main():
    print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC} Hello Friend")

    gratitude_responses = [
        "No problem bro!",
        "Much Luvs ;).",
        "Anytime!",
        "Happy to assist!",
        "You got it from here, brother/sister. I believe in you.",
        "Let's gooooo :)"
    ]

    friendship_history = load_friendship_history()
    last_user_input = None

    while True:
        try:
            user_input = input(f"{RED}You:{ENDC} ").strip()  # Use input function

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'goodnight', 'cya']:
                print(f"{LIGHT_BLUE}Goodbye Friend...{ENDC}")
                save_friendship_history(friendship_history)
                break

            if is_gibberish(user_input):
                print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC} Please provide more info ;(")
                continue

            if user_input.lower() == 'show history':
                for message in friendship_history:
                    print(message['role'] + ": " + message['content'])
                continue

            if user_input.lower() == last_user_input:
                print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC} Stop being annoying.")
                continue

            gratitude_words = ['thanks', 'thank you', 'nice', 'ok', 'nice, thanks a lot', 'appreciate it', 'grateful', 'much obliged', 'cool']
            if any(word in user_input.lower() for word in gratitude_words):
                print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC}", random.choice(gratitude_responses))
                continue

            response = interact_with_wormgpt(user_input, friendship_history)

            if not response:
                print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC} Yeah, What? (you broke it lolz, enter text to reset hopefully)")
            elif response.lower() != user_input.lower():
                print(f"{LIGHT_BLUE}ALonelyHacker:{ENDC}", response)

            friendship_history.append({'role': 'user', 'content': user_input})
            if response.lower() != user_input.lower():
                friendship_history.append({'role': 'model', 'content': response})

            last_user_input = user_input
        except KeyboardInterrupt:
            print(f"\n{LIGHT_BLUE}ALonelyHacker:{ENDC} Goodbye! Exiting...")
            save_friendship_history(friendship_history)
            break

if __name__ == "__main__":
    main()
