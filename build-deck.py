import os
import sys
import glob
from PIL import Image, ImageDraw

MAX_COLS = 10
MAX_ROWS = 7
CARD_WIDTH = 400
CARD_HEIGHT = 400

deck = Image.new('RGB', (CARD_WIDTH * MAX_COLS, CARD_HEIGHT * MAX_ROWS), color = 'white')

x, y = (0, 0)
for filename in glob.glob("individual/card--*.png"):
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
