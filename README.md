# Dominoops

A dominoes-based card game to teach concepts used in Object-Oriented Programming (OOP), as implemented by statically-typed languages like Java. Each card represents an object from a specific class, which can be associated to other objects through typed attributes. Concepts explored in the game include association, inheritance, interface implementation, and type compatibility.

## Creating the images for the game

The images used in the deck are located in `deck/` for your convenience. Those interested in recreating the images or modifying the deck should read below.

The card deck is defined by the data in `base-classes.csv` and `base-objects.csv`, by the design in `card.svg`, and by the icons contained in `images.svg`. Run the following scripts (in this order) to build the deck:

1. `render-images.py`: creates a PNG for each icon in `images.svg`
2. `render-cards.py`: creates a PNG for each card in `base-objects.csv`, using the layout from `card.svg`
3. `build-deck.py`: combines the PNG files for all cards in a single PNG file; also creates the back of the cards and the arrow card. The files are create in the `deck/` folder.

## Importing into Tabletop Simulator

- Open [Tabletop Simulator](https://www.tabletopsimulator.com/)
- Create a single player game
- Create a custom deck and import the images for the front and back (you may need to upload them somewhere or to start a local web server)
- Create a custom card and import the arrow card image

## Rules

The rules are available at this [draft specification](https://docs.google.com/document/d/16VswJkhtAEHbi0EtAEPJx98WvsazJfi2fQ9Siv7qhqk/edit) (in Portuguese).

