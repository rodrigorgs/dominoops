import csv
import os
import sys
import glob
import re

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
        return ''
    else:
        return 'image--' + class_name

##################################################

if not os.path.exists('individual'):
    os.mkdir('individual')

classes = load_classes('base-classes.csv')
images = load_images()

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
        svg = svg.replace('>left<', quote("" +   card['leftVar'] + " : " + card['leftClass']))
        svg = svg.replace('>right<', quote("" +  card['rightVar'] + " : " + card['rightClass']))
        svg = svg.replace('>top<', quote("" +    card['topVar'] + " : " + card['topClass']))
        svg = svg.replace('>bottom<', quote("" + card['bottomVar'] + " : " + card['bottomClass']))

        svg = svg.replace('xlink:href="image--left.png"', f'xlink:href="{image_name(card["leftClass"])}.png"')
        svg = svg.replace('xlink:href="image--right.png"', f'xlink:href="{image_name(card["rightClass"])}.png"')
        svg = svg.replace('xlink:href="image--top.png"', f'xlink:href="{image_name(card["topClass"])}.png"')
        svg = svg.replace('xlink:href="image--bottom.png"', f'xlink:href="{image_name(card["bottomClass"])}.png"')
        svg = svg.replace('xlink:href="image--center.png"', f'xlink:href="{image_name(card["class"])}.png"')

        with open('individual/custom.svg', 'w') as customFile:
            customFile.write(svg)
        
        inpath = os.path.abspath('individual/custom.svg')
        outpath = os.path.abspath(f"individual/card--{obj['object']}.png")
        os.system(f"inkscape --without-gui --export-png={outpath} {inpath}")
