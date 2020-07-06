import csv
import os
import sys
import glob
import re
from PIL import Image, ImageDraw

templateSvg = None
with open('card.svg') as file:
    templateSvg = file.read()

def quote(string):
    return ">" + string + "<"

def load_classes(filename):
    classes = dict()
    rows = None
    with open(filename) as file:
        rows = csv.DictReader(file)
        for klass in rows:
            classes[klass['class']] = klass
    return classes

def load_images():
    images = []
    for path in glob.glob("individual/image--*.png"):
        filename = os.path.basename(path)
        m = re.match(r'image--(.*?).png', filename)
        images.append(m.group(1))
    return images

def image_name(class_name):
    if len(class_name) == 0:
        return 'blank'
    else:
        return 'image--' + class_name

def create_blank_image():
    image = Image.new('RGBA', (80, 80), (255, 0, 0, 0))
    image.save('individual/blank.png')

##################################################

if not os.path.exists('individual'):
    os.mkdir('individual')

create_blank_image()
classes = load_classes('base-classes.csv')
images = load_images()

def render_attribute(card, orientation):
    if card[orientation + 'Class'] == '':
        return quote('')
    else:
        return quote("" +   card[orientation + 'Var'] + " : " + card[orientation + 'Class'])

with open('base-objects.csv') as csvFile:
    objects = csv.DictReader(csvFile)
    for obj in objects:
        print(obj['object'] + " : " + obj['class'])
        if len(obj['object'].strip()) == 0 or len(obj['class'].strip()) == 0:
            print("pulando...")
            continue
        # print(obj['object'])
        card = classes[obj['class']]

        hierarchyList = []
        if len(card['hierarchy']) > 0:
            hierarchyList = card['hierarchy'].split(" > ")
        hierarchyList = [card['class']] + hierarchyList
        svg = templateSvg
        svg = svg.replace('>name<', quote(obj['object']))
        svg = svg.replace('>hierarchy<', quote(' ⇾ '.join(hierarchyList)))
        # ↓
        svg = svg.replace('>left<', render_attribute(card, 'left'))
        svg = svg.replace('>right<', render_attribute(card, 'right'))
        svg = svg.replace('>top<', render_attribute(card, 'top'))
        svg = svg.replace('>bottom<', render_attribute(card, 'bottom'))
        
        svg = svg.replace('xlink:href="image--left.png"', f'xlink:href="{image_name(card["leftClass"])}.png"')
        svg = svg.replace('xlink:href="image--right.png"', f'xlink:href="{image_name(card["rightClass"])}.png"')
        svg = svg.replace('xlink:href="image--top.png"', f'xlink:href="{image_name(card["topClass"])}.png"')
        svg = svg.replace('xlink:href="image--bottom.png"', f'xlink:href="{image_name(card["bottomClass"])}.png"')
        svg = svg.replace('xlink:href="image--center.png"', f'xlink:href="{image_name(card["class"])}.png"')

        with open('individual/custom.svg', 'w') as customFile:
            customFile.write(svg)
        inpath = os.path.abspath('individual/custom.svg')
        outpath = os.path.abspath(f"individual/card--{obj['object']}.png")
        os.system(f"inkscape --export-type=png --export-filename={outpath} {inpath}")

        