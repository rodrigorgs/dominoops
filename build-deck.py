import os
import sys
import glob
import csv
from PIL import Image, ImageDraw

MAX_COLS = 10
MAX_ROWS = 7
CARD_WIDTH = 400
CARD_HEIGHT = 400

deck = Image.new('RGBA', (CARD_WIDTH * MAX_COLS, CARD_HEIGHT * MAX_ROWS), color = None)

x, y = (0, 0)

with open('base-objects.csv') as csvFile:
    if not os.path.isdir('individual'):
        print("Folder `individual` does not exist.")
        print("You need to run render-images.py and render-cards.py before building the deck.")
        sys.exit(1)
    objects = csv.DictReader(csvFile)
    for obj in objects:
        if len(obj['object'].strip()) == 0 or len(obj['class'].strip()) == 0:
            continue
        filename = f"individual/card--{obj['object']}.png"

# for filename in glob.glob("individual/card--*.png"):
        with Image.open(filename) as image:
            deck.paste(image, (x * CARD_WIDTH, y * CARD_HEIGHT))

        x += 1
        if x == MAX_COLS:
            x = 0
            y += 1
            if y == MAX_ROWS:
                print("Too many cards in the deck.")
                sys.exit(0)

if not os.path.exists('deck'):
    os.mkdir('deck')
deck.save('deck/deck.png')

# Build back
back = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), color = 'red')
draw = ImageDraw.Draw(back)
x = 0
y = 0
step = 30
for y in range(-CARD_HEIGHT, CARD_HEIGHT, step):
    draw.line([0, y, CARD_WIDTH, y + CARD_WIDTH], fill = 'white', width = 3)
    draw.line([CARD_WIDTH, y, 0, y + CARD_WIDTH], fill = 'white', width = 3)
back.save('deck/back.png')

# Build arrow
inpath = os.path.abspath('arrow.svg')
outpath = os.path.abspath('deck/arrow.png')
os.system(f"inkscape --export-type=png --export-filename={outpath} {inpath}")
