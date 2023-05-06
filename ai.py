"""
Use OpenAI to translate text by using the English and Japanese languages to the Chinese languages.
"""

import openai

with open("key.md") as key:
    openai.api_key = key.read().strip()


def translate(english: str, japanese: str, targets: list[str] = None) -> dict:
    if targets is None:
        targets = ["Simplified Chinese", "Traditional Chinese"]
    target_languages = " & ".join(targets)
    content = f'You are best translator who is translating World of Warships (a second WW warship game) from English to Chinese with the help of Japanese. Strictly output the result only. The English translation is "{english}", the Japanese version is "{japanese}". Now translate this into {target_languages} so it doesn\'t feel like a translator.'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": content,
            },
        ],
    )
    output = response["choices"][0]["message"]["content"]
    output = output.replace("：", ":")
    output = output.split("\n")
    # not empty line
    output = [line for line in output if line]
    print(output)
    translated_dict = {}
    for index, lang in enumerate(output):
        lang = lang.split(":")
        translated_dict[targets[index]] = lang[1].strip()
    return translated_dict


def extract_from_tags(raw: str) -> str:
    return raw.split(">")[1].split("</")[0]


if __name__ == "__main__":
    target_languages = ["Simplified Chinese", "Traditional Chinese"]
    # read the ja.xliff first to obtain all English and Japanese strings
    with open("translation/Translation.ja.xliff", "r", encoding="utf-8") as f:
        lines = f.readlines()

    simplified_cn_temp = open("temp.zh.xliff", "w", encoding="utf-8")
    traditional_cn_temp = open("temp.zh_tw.xliff", "w", encoding="utf-8")

    language_map = {
        "Simplified Chinese": simplified_cn_temp,
        "Traditional Chinese": traditional_cn_temp,
    }

    unit_info = None
    english = None
    japanese = None
    note = None
    for line in lines:
        if "<trans-unit id=" in line:
            unit_info = line
        if "<source>" in line:
            english = extract_from_tags(line)
        if "<target" in line:
            japanese = extract_from_tags(line)
        if "<note from" in line:
            note = line

        if not unit_info or not english or not japanese or not note:
            continue

        # now, we have everything, let's translate
        print(f"Translating {english}...")
        try:
            translated_dict = translate(english, japanese, target_languages)
        except Exception as e:
            translated_dict = None

        print(translated_dict)
        if translated_dict is None:
            translated_dict = {}
            # map it to the English version
            for lang in target_languages:
                translated_dict[lang] = english

        for lang in translated_dict:
            if lang not in target_languages:
                continue
            current_lang = language_map[lang]
            current_lang.write(unit_info)
            current_lang.write(f"\t<source>{english}</source>\n")

            current_lang.write(
                f'\t<target state="translated">{translated_dict[lang]}</target>\n'
            )
            current_lang.write(note)
            current_lang.write("</note>\n\t</trans-unit>\n")

        unit_info = None
        english = None
        japanese = None
        note = None
    language_map.values().close()
    print("Done!")
