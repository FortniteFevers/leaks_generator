import io
import json
import math
import sys
import time

import urllib3
from PIL import Image

import SETTINGS
import module

urllib3.disable_warnings()
http = urllib3.PoolManager()

lang = SETTINGS.lang
if not lang:
    lang = "en"


def get_response():
    with open('cache/fortniteapi.json', 'r') as fnapi_file:
        fnapi_cache = json.load(fnapi_file)
    fnapi_new = json.loads(
        http.request("get", f'https://fortnite-api.com/v2/cosmetics/br/new?language={lang}').data.decode('utf-8'))

    if fnapi_cache != fnapi_new:
        print("FN API NEW COSMETICS")
        globaldata = {
            "status": 200,
            "data": {
                "items": [
                ]
            }
        }
        for cosmetic in fnapi_new["data"]["items"]:
            cosmetic["rarity"] = {
                    "value": cosmetic["rarity"]["value"],
                    "displayValue": cosmetic["rarity"]["displayValue"],
                    "backendValue": cosmetic["rarity"]["backendValue"]
                }
            globaldata["data"]["items"].append(cosmetic)

        with open('cache/fortniteapi.json', 'w') as file:
            json.dump(fnapi_new, file, indent=3)
        return fnapi_new

    with open('cache/benbot.json', 'r') as fnapi_file:
        benbot_cache = json.load(fnapi_file)
    benbot_new = json.loads(
        http.request("get", f'https://benbotfn.tk/api/v1/newCosmetics?lang={lang}').data.decode('utf-8'))
    if benbot_cache != benbot_new:
        print("BENBOT NEW COSMETICS")
        with open('cache/benbot.json', 'w') as file:
            json.dump(benbot_new, file, indent=3)
        globaldata = {
            "status": 200,
            "data": {
                "items": [
                ]
            }
        }
        for cosmetic in benbot_new["items"]:
            cosmeticdata = {
                "id": cosmetic["id"],
                "name": cosmetic["name"],
                "description": cosmetic["description"],
                "type": {
                    "value": cosmetic["shortDescription"],
                    "displayValue": cosmetic["shortDescription"],
                    "backendValue": cosmetic["backendType"]
                },
                "rarity": {
                    "value": cosmetic["backendRarity"].split("::")[1],
                    "displayValue": cosmetic["rarity"],
                    "backendValue": cosmetic["backendRarity"]
                },
                "images": {
                    "smallIcon": cosmetic["icons"]["icon"],
                    "featured": cosmetic["icons"]["featured"],
                    "icon": cosmetic["icons"]["icon"],
                    "other": cosmetic["icons"]["icon"],
                }
            }
            globaldata["data"]["items"].append(cosmeticdata)
        with open('cache/benbot.json', 'w') as file:
            json.dump(benbot_new, file, indent=3)
        return globaldata
    return None


def check():
    new = get_response()
    if new is not None:
        start = time.time()
        print("Leaks detected, starting now with image generation.\n\nDONT CANCEL THE PROCESS!")
        files = []
        c = 0
        for i in new["data"]["items"]:
            if i["name"].lower().startswith("tbd"):
                i["images"]["featured"] = SETTINGS.placeholderurl
            c += 1
            try:
                files.append(module.GenerateCard(i))
                print(f"{c}/{len(new['data']['items'])}")
            except:
                continue
        if files is None:
            raise print("No Images")
        print("Parse now all Images to one Image")
        gerundet = round(math.sqrt(len(files)) + 0.45)
        result = Image.new("RGB", (gerundet * 305 - 5, gerundet * 550 - 5))
        if SETTINGS.backgroundurl != "":
            result.paste(Image.open(io.BytesIO(http.urlopen("GET", SETTINGS.backgroundurl).data)).resize(
                (int(gerundet * 305 - 5), int(gerundet * 550 - 5)),
                Image.ANTIALIAS))
        x = -305
        y = 0
        count = 0
        for img in files:
            try:
                img.thumbnail((305, 550), Image.ANTIALIAS)
                w, h = img.size
                if count >= gerundet:
                    y += 550
                    x = -305
                    count = 0
                x += 305
                count += 1
                result.paste(img, (x, y, x + w, y + h))
            except:
                continue
        result.save(f"leaks.png", optimized=True)
        ende = time.time()
        print(f"Finished.\n\nGenerating Image in {round(ende - start, 2)}sec")
        result.show()
        time.sleep(60)
        sys.exit()


if __name__ == "__main__":
    while True:
        print("Checking for Leaks")
        check()
        time.sleep(20)
