"""
Use OpenAI to translate text by using the English and Japanese languages to the Chinese languages.
"""

import os
import openai

with open("key.md") as key:
    openai.api_key = key.read().strip()

english = "Rudder shift time"
japanese = "転舵所要時間"
output_lang = "Simplified Chinese"
content = f"You are top1 translator who is translating World of Warships (a second WW warship game) from English to Chinese with the help of Japanese. Only output the result. The English translation is \"{english}\", the Japanese version is \"{japanese}\". Now translate this into \"{output_lang}\" so it doesn't feel like a translator."
# use gpt-3.5-turbo model to translate text
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "assistant",
            "content": content,
        },
    ],
)
content = response["choices"][0]["message"]["content"]
print(response)
print(content)
