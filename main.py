from __future__ import annotations
import ollama


def annotate(note):
    response = ollama.chat(model='mistral', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    print(response['message']['content'])


def main():
    test_chat('you are going to be my notes app, what do you think about that?')


if __name__ == "__main__":
    main()
