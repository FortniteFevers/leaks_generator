import io

import urllib3
from PIL import Image, ImageFont, ImageDraw

import SETTINGS

urllib3.disable_warnings()
http = urllib3.PoolManager()

def GetBlendColor(Rarity):
    if Rarity.lower() == "frozen":
        blendColor = (148, 223, 255)
    elif Rarity.lower() == "lava":
        blendColor = (234, 141, 35)
    elif Rarity.lower() == "legendary":
        blendColor = (211, 120, 65)
    elif Rarity.lower() == "dark":
        blendColor = (251, 34, 223)
    elif Rarity.lower() == "starwars":
        blendColor = (231, 196, 19)
    elif Rarity.lower() == "marvel":
        blendColor = (197, 51, 52)
    elif Rarity.lower() == "dc":
        blendColor = (84, 117, 199)
    elif Rarity.lower() == "icon":
        blendColor = (54, 183, 183)
    elif Rarity.lower() == "shadow":
        blendColor = (113, 113, 113)
    elif Rarity.lower() == "epic":
        blendColor = (177, 91, 226)
    elif Rarity.lower() == "rare":
        blendColor = (73, 172, 242)
    elif Rarity.lower() == "uncommon":
        blendColor = (96, 170, 58)
    elif Rarity.lower() == "common":
        blendColor = (190, 190, 190)
    elif Rarity == "slurp":
        blendColor = (41, 150, 182)
    else:
        blendColor = (255, 255, 255)

    return blendColor


def GenerateCard(Item):
    card = Image.new("RGBA", (300, 545))
    Draw = ImageDraw.Draw(card)

    Name = Item["name"]
    Rarity = Item["rarity"]["value"].lower()
    displayRarity = Item["rarity"]["displayValue"]
    blendColor = GetBlendColor(Rarity)
    Category = Item["type"]["value"]
    displayCategory = Item["type"]["displayValue"]

    try:
        layer = Image.open(f"assets/Images/card_top_{Rarity.lower()}.png")
    except:
        layer = Image.open("assets/Images/card_top_common.png")

    card.paste(layer)

    if Item["images"]["featured"] is not None:
        Icon = Item["images"]["featured"]
    else:
        if Item["images"]["icon"] is not None:
            Icon = Item["images"]["icon"]
        else:
            if Item["images"]["smallIcon"] is not None:
                Icon = Item["images"]["smallIcon"]
            else:
                if Item["images"]["other"] is not None:
                    Icon = Item["images"]["other"]
                else:
                    Icon = SETTINGS.placeholderurl
    # Download the Item icon
    Icon = Image.open(io.BytesIO(http.urlopen("GET", Icon).data)).resize((512, 512), Image.ANTIALIAS)
    if (Category == "outfit") or (Category == "emote"):
        ratio = max(285 / Icon.width, 365 / Icon.height)
    elif Category == "wrap":
        ratio = max(230 / Icon.width, 310 / Icon.height)
    else:
        ratio = max(310 / Icon.width, 390 / Icon.height)
    Icon = Icon.resize((int(Icon.width * ratio), int(Icon.height * ratio)), Image.ANTIALIAS)
    Middle = int((card.width - Icon.width) / 2)  # Get the middle of card and icon
    # Paste the image
    if (Category == "outfit") or (Category == "emote"):
        card.paste(Icon, (Middle, 0), Icon)
    else:
        card.paste(Icon, (Middle, 15), Icon)

    try:
        layer = Image.open(f"assets/Images/card_faceplate_{Rarity.lower()}.png")
        card.paste(layer, layer)
    except Exception as ex:
        layer = Image.open("assets/Images/card_faceplate_common.png")
        card.paste(layer, layer)

    BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", 30)
    textWidth = BurbankBigCondensed.getsize(f"{displayRarity.capitalize()} {displayCategory.capitalize()}")[0]

    Middle = int((card.width - textWidth) / 2)
    Draw.text((Middle, 385), f"{displayRarity.capitalize()} {displayCategory.capitalize()}", blendColor,
              font=BurbankBigCondensed)

    FontSize = 56
    while ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize).getsize(Name)[0] > 265:
        FontSize -= 1

    BurbankBigCondensed = ImageFont.truetype(f"assets/Fonts/BurbankBigCondensed-Black.otf", FontSize)
    textWidth = BurbankBigCondensed.getsize(Name)[0]
    change = 56 - FontSize

    Middle = int((card.width - textWidth) / 2)
    Top = 425 + change / 2
    Draw.text((Middle, Top), Name, (255, 255, 255), font=BurbankBigCondensed)

    return card


def GetMiddle(x, y):
    return (x - y) / 2