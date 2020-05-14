import csv
import json

ORIENTATION_TOP = 0
ORIENTATION_RIGHT = 1
ORIENTATION_BOTTOM = 2
ORIENTATION_LEFT = 3

class KlassManager:
  def __init__(self):
    self.klass_name_to_klass = {}

  def add_klass(self, name, klass):
    if name is not None:
      self.klass_name_to_klass[name] = klass
  
  def get_klass(self, name):
    if name is None or name == "":
      return None
    elif name in self.klass_name_to_klass:
      return self.klass_name_to_klass[name]
    else:
      klass = Klass(name)
      self.add_klass(name, klass)
      return klass

class Klass:
  def __init__(self, className):
    self.classes = [None, None, None, None]
    self.className = className
    self.superklass = None
    self.subklasses = set()

  def is_descendant_of(self, klass):
    return self in klass.descendants()

  def is_compatible_with(self, klass):
    # se é a própria classe ou é uma subclasse dela
    return klass is not None and (klass == self or self.is_descendant_of(klass))

  def add_superklass(self, klass):
    if klass is None:
        return
    self.superklass = klass
    klass.subklasses.add(self)
  
  def descendants(self):
    res = set()
    for sub in self.subklasses:
        res.add(sub)
        res = res.union(sub.descendants())
    return res

  def set_klass_at_orientation(self, orientation, klass):
    self.classes[orientation] = klass

  def get_klass_at_orientation(self, orientation):
    return self.classes[orientation]

  def __repr__(self):
    return f"(Class {self.className})"

class Card:
  # 0 < rotation <= 3
  def __init__(self, name, klass, rotation = 0):
    self.name = name
    self.klass = klass
    self.rotation = rotation

  # classe:   carta rotacionada 1 vez:
  #   t              l       3
  #  l r            b t     2  0
  #   b              r        1
  #
  def get_klass_at_orientation(self, orientation):
    klass_orientation = (orientation - self.rotation + 4) % 4
    return self.klass.get_klass_at_orientation(klass_orientation)

  def can_be_placed_on_top(self, card):
    return self.klass.is_descendant_of(card.klass)

  def can_be_placed_on(self, orientation, card):
    # can_be_placed_on(bob, ORIENTATION_RIGHT, fulano)
    #  fulano:Pessoa         bob:Construtor
    #     Objeto                Ferramenta
    #            Pessoa                     Pessoa
    #
    card_dependency = card.get_klass_at_orientation(orientation)
    self_dependency = self.get_klass_at_orientation((orientation + 2) % 4) # card a ser jogado precisa ser orientado
    return self.klass.is_compatible_with(card_dependency) or card.klass.is_compatible_with(self_dependency) # checar condição

  def __repr__(self):
    return f"(Card {self.name} ({self.klass.className}))"

##################

if __name__ == '__main__':
  ### Importa as cartas que serao usadas e instancia objetos da classe Card

  fileCsv = open('base-classes.csv', 'r')
  reader = csv.DictReader(fileCsv)
  klasses = {}

  # Mapeia para um dicionario

  for row in reader:
    klasses[row['class']] = row

  # Instancia objetos a partir do dicionario
  manager = KlassManager()
  cardsObj = [] # É a lista de objetos Klass
  for card in klasses:
      c = klasses[card]
      klass = manager.get_klass(c['class'])
      klass.add_superklass(manager.get_klass(c['hierarchy']))
      klass.set_klass_at_orientation(ORIENTATION_TOP, manager.get_klass(c['topClass']))
      klass.set_klass_at_orientation(ORIENTATION_RIGHT, manager.get_klass(c['rightClass']))
      klass.set_klass_at_orientation(ORIENTATION_BOTTOM, manager.get_klass(c['bottomClass']))
      klass.set_klass_at_orientation(ORIENTATION_LEFT, manager.get_klass(c['leftClass']))
      klass.leftVar = c['leftVar']
      klass.topVar = c['topVar']
      klass.rightVar = c['rightVar']
      klass.bottomVar = c['bottomVar']
      cardsObj.append(klass)

  # Lê cartas (objetos)
  cards = []
  with open('base-objects.csv') as fileCsv:
    reader = csv.DictReader(fileCsv)
    for row in reader:
      if len(row['class']) == 0:
        continue
      klass = manager.get_klass(row['class'])
      card = Card(row['object'], klass)
      cards.append(card)

# TODO: fazer testes unitários