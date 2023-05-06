# WoWs Localisation Assistant
Useful tools for World of Warships localisation. This project now uses gpt-3.5-turbo to assist with localisation. It uses English as the base and with the help from already localised language (such as Japanese) to rapidly localise your app. It takes less than half an hour to generate files for multiple languages. However, manual checking is still required after the generation.

This project mainly helps with [WoWs-ShipBuilder](https://github.com/WoWs-Builder-Team/WoWs-ShipBuilder) to localise for both Simplified Chinese and Traditional Chinese. It can also be used for other languages with some modifications.

## Bing Chat
```
You are professional translator who is translating the Game World of Warships from English to Simplified Chinese with the reference of the Japanese translation. Only output the result. The English translation is "|ENGLISH|", the Japanese version is "|JAPANESE|". Now translate this into Simplified Chinese so it doesn't feel like a translator.
```
