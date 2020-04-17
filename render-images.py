import csv
import os
import sys

if not os.path.exists('individual'):
    os.mkdir('individual')

templateSvg = None
with open('images.svg') as file:
    templateSvg = file.read()

classes = set()
with open('base-classes.csv') as file:
    data = csv.DictReader(file)
    for row in data:
        classes.add(row['class'])

print(classes)

with open('base-objects.csv') as csvFile:
    for klass in classes.union({'undefined'}):
        if f'id="{klass}"' in templateSvg:
            print(klass)

            inpath = os.path.abspath('images.svg')
            outpath = os.path.abspath(f"individual/image--{klass}.png")
            os.system(f"inkscape --without-gui --export-id={klass} --export-png={outpath} {inpath}")
