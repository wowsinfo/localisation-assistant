"""
Validate our temp files with the original files
"""

import os
import json
from ai import extract_from_tags, translate

def extract_from_unit(raw: str) -> str:
    return raw.split(' id="')[1].split('"')[0]

def validate_xliff_with(temp: str, original: str):
    with open(temp, "r", encoding="utf-8") as f:
        temp_lines = f.readlines()
    with open(original, "r", encoding="utf-8") as f:
        original_lines = f.readlines()
    
    orginal_dict = {}
    for line in original_lines:
        if "<trans-unit id=" in line:
            unit_id = extract_from_unit(line)
            orginal_dict[unit_id] = False
    print(len(orginal_dict))

    with open(f"patched_{temp}", "w", encoding="utf-8") as f:
        for line in temp_lines:
            if "<trans-unit id=" in line:
                unit_id = extract_from_unit(line)
                orginal_dict[unit_id] = True

            # check if the translation is broken
            if "<target" in line:
                translation = extract_from_tags(line)
                # remove quotes around
                translation = translation.replace('"', "").strip()
                # remove hanyu pinyin
                translation = translation.split(" (")[0]
                if len(translation) > 8:
                    print(f"Broken translation: {translation}")
                    fixed_version = input("Update with: ")
                    if fixed_version:
                        line = line.replace(translation, fixed_version)
            f.write(line)

    # check missing keys
    for k, v in orginal_dict.items():
        if not v:
            print(f"Missing key: {k}")

def fix_missing_tag(temp: str):
    with open(temp, "r", encoding="utf-8") as f:
        temp_lines = f.readlines()
    
    unit_tag_f = 0
    unit_tag_t = 0
    flag = False

    for line in temp_lines:
        if "<trans-unit" in line:
            if flag:
                print(line)
            unit_tag_t += 1
            flag = True
        if "</trans-unit" in line:
            unit_tag_f += 1
            flag = False
        
    print(unit_tag_f, unit_tag_t)

if __name__ == "__main__":
    # validate_xliff_with("temp.zh.xliff", "translation/Translation.zh-CN.xliff")
    # validate_xliff_with("temp.zh_tw.xliff", "translation/Translation.zh-TW.xliff")
    fix_missing_tag("temp.zh.xliff")
    fix_missing_tag("temp.zh_tw.xliff")