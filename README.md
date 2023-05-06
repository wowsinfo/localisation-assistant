# WoWs Localisation Assistant
Useful tools for World of Warships localisation. This project now uses gpt-3.5-turbo to assist with localisation. It uses English as the base and with the help from already localised language (such as Japanese) to rapidly localise your app. It takes less than half an hour to generate files for multiple languages. However, manual checking is still required after the generation.

This project mainly helps with [WoWs-ShipBuilder](https://github.com/WoWs-Builder-Team/WoWs-ShipBuilder) to localise for both Simplified Chinese and Traditional Chinese. It can also be used for other languages with some modifications.

## Bing Chat
```
You are professional translator who is translating the Game World of Warships from English to Simplified Chinese with the reference of the Japanese translation. Only output the result. The English translation is "|ENGLISH|", the Japanese version is "|JAPANESE|". Now translate this into Simplified Chinese so it doesn't feel like a translator.
```

## Setup
- Run `python -m venv .env` to create a virtual environment
- Enter the environment
- Run `pip install -r requirements.txt` to install dependencies
- Place your `OPENAI` key in `key.md`
- Run `main.py` to unpack language files to fetch game translations
- Run `ai.py` to generate translations

The cost is about 0.2$ for two languages. You may spend a bit more if you want to localise more languages. Note that this project aims to assist with the localisation, make sure you still verify the results before using them.
