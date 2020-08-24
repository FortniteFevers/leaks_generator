import io

import urllib3
from PIL import Image, ImageFont, ImageDraw

import SETTINGS

urllib3.disable_warnings()
http = urllib3.PoolManager()


def GetBlendColor(Rarity):
    if Rarity.lower() == "frozen":
        return 148, 223, 255
    elif Rarity.lower() == "lava":
        return 234, 141, 35
    elif Rarity.lower() == "legendary":
        return 211, 120, 65
    elif Rarity.lower() == "dark":
        return 251, 34, 223
    elif Rarity.lower() == "starwars":
        return 231, 196, 19
    elif Rarity.lower() == "marvel":
        return 197, 51, 52
    elif Rarity.lower() == "dc":
        return 84, 117, 199
    elif Rarity.lower() == "icon":
        return 54, 183, 183
    elif Rarity.lower() == "shadow":
        return 113, 113, 113
    elif Rarity.lower() == "epic":
        return 177, 91, 226
    elif Rarity.lower() == "rare":
        return 73, 172, 242
    elif Rarity.lower() == "uncommon":
        return 96, 170, 58
    elif Rarity.lower() == "common":
        return 190, 190, 190
    elif Rarity == "slurp":
        return 41, 150, 182
    else:
        return 255, 255, 255


def GenerateCard(Item):
    card = Image.new("RGB", (300, 545))
    Draw = ImageDraw.Draw(card)

    try:
        layer = Image.open(f"assets/Images/card_top_{Item['rarity']['value'].lower().lower()}.png")
    except:
        layer = Image.open("assets/Images/card_top_common.png")

    card.paste(layer)

    if Item["images"]["featured"]:
        Icon = Item["images"]["featured"]
    else:
        if Item["images"]["icon"]:
            Icon = Item["images"]["icon"]
        else:
            if Item["images"]["smallIcon"]:
                Icon = Item["images"]["smallIcon"]
            else:
                if Item["images"]["other"]:
                    Icon = Item["images"]["other"]
                else:
                    Icon = "https://i.imgur.com/JPuoAAu.png"
    # Download the Item icon
    Icon = Image.open(io.BytesIO(http.urlopen("GET", Icon).data)).resize((512, 512), Image.ANTIALIAS)
    if (Item["type"]["value"] == "outfit") or (Item["type"]["value"] == "emote"):
        ratio = max(285 / Icon.width, 365 / Icon.height)
    elif Item["type"]["value"] == "wrap":
        ratio = max(230 / Icon.width, 310 / Icon.height)
    else:
        ratio = max(310 / Icon.width, 390 / Icon.height)
    Icon = Icon.resize((int(Icon.width * ratio), int(Icon.height * ratio)), Image.ANTIALIAS)
    Middle = int((card.width - Icon.width) / 2)  # Get the middle of card and icon
    if (Item["type"]["value"] == "outfit") or (Item["type"]["value"] == "emote"):
        card.paste(Icon, (Middle, 0), Icon)
    else:
        card.paste(Icon, (Middle, 15), Icon)
    try:
        card.paste(Image.open(f"assets/Images/card_faceplate_{Item['rarity']['value'].lower()}.png"),
                   Image.open(f"assets/Images/card_faceplate_{Item['rarity']['value'].lower()}.png"))
    except:
        card.paste(Image.open("assets/Images/card_faceplate_common.png"),
                   Image.open("assets/Images/card_faceplate_common.png"))

    Middle = int((card.width - ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 30).getsize(
        f"{Item['rarity']['displayValue'].capitalize()} {Item['type']['displayValue'].capitalize()}")[0]) / 2)
    Draw.text((Middle, 385),
              f"{Item['rarity']['displayValue'].capitalize()} {Item['type']['displayValue'].capitalize()}",
              GetBlendColor(Item['rarity']['value']),
              font=ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 30))

    FontSize = 56
    while ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize).getsize(Item['name'])[0] > 265:
        FontSize -= 1

    BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize)
    textWidth = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 30).getsize(Item['name'])[0]
    change = 56 - FontSize

    Middle = int((card.width - textWidth) / 2)
    Top = 425 + change / 2
    Draw.text((Middle, Top), Item['name'], (255, 255, 255), font=BurbankBigCondensed)

    if SETTINGS.watermark != "":
        font = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 25)
        Draw.text((0, 0), SETTINGS.watermark, GetBlendColor(Item['rarity']['value']), font=font)

    return card
