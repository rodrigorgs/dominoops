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
    if name is None:
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

  def is_subclass_of(self, klass):
    # TODO: implementar
    return True

  def is_compatible_with(self, klass):
    # TODO: implementar
    # se é a própria classe ou é uma subclasse dela
    return klass is not None and klass == self or self in klass.descendants()

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
    # TODO: completar implementação
    top = self.get_klass_at_orientation(ORIENTATION_TOP)
    right = self.get_klass_at_orientation(ORIENTATION_RIGHT)
    return f"(Class {self.className})"
    # return f"ClassName: {self.className}, Hierarchy: {self.hierarchy}, LeftVar: {self.leftVar}, TopVar: {self.topVar}, RightVar: {self.rightVar}, BottomVar: {self.bottomVar}"

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
    # TODO: implementar
    pass

  def can_be_placed_on(self, orientation, card):
    # can_be_placed_on(fulano, ORIENTATION_RIGHT)
    #  fulano:Pessoa
    #     Objeto
    #            Pessoa
    #
    card_dependency = card.get_klass_at_orientation(orientation)
    self_dependency = self.get_klass_at_orientation((orientation + 2) % 4)
    print(f"card {self.klass} dependencies: {card.name} {card_dependency} {card.klass.is_compatible_with(self_dependency)}, {self.name} {self_dependency} {self.klass.is_compatible_with(card_dependency)}")

    return self.klass.is_compatible_with(card_dependency) or card.klass.is_compatible_with(self_dependency)

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


  fulano = cards[0]
  sicrana = cards[1]
  bob = cards[4]

  print(fulano.get_klass_at_orientation(ORIENTATION_TOP))
  print(fulano.get_klass_at_orientation(ORIENTATION_RIGHT))

  fulano.rotation = 1

  print(fulano.get_klass_at_orientation(ORIENTATION_TOP))
  print(fulano.get_klass_at_orientation(ORIENTATION_RIGHT))

  # fulano.rotation = 1
  print(bob.can_be_placed_on(ORIENTATION_RIGHT, fulano))
  print(manager.get_klass("Pessoa").descendants())
  # print(fulano.can_be_placed_on(ORIENTATION_TOP, sicrana))
  # pessoa = manager.get_klass("Construtor")
  # print(pessoa)
