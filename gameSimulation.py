import csv
import json
import random
import copy
import unittest

MATRIX_WIDTH = 20
MATRIX_HEIGHT = MATRIX_WIDTH
CARDS_PER_PLAYER = 5

ORIENTATION_TOP = 0
ORIENTATION_RIGHT = 1
ORIENTATION_BOTTOM = 2
ORIENTATION_LEFT = 3

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Table:
  def __init__(self, card):
    self.matrix = [[None for x in range(MATRIX_HEIGHT)] for y in range(MATRIX_HEIGHT)] 
    self.edge1_pos = Point(MATRIX_WIDTH // 2, MATRIX_HEIGHT // 2)
    self.edge2_pos = copy.copy(self.edge1_pos)
    self.put_card(card, self.edge1_pos)

  def get_edge1(self):
    # TODO: retornar card_info
    return #get_card(self.edge1_pos)

  def get_edge2(self):
    return #get_card(self.edge2_pos)

  def get_card(self, point):
    return self.matrix[point.y][point.x]

  def put_card(self, card, point):
    self.matrix[point.y][point.x] = card

class CardInfo:
  def __init__(self, card, empty_sides):
    pass

class PlayerMove:
  def __init__(self, card, position, rotation):
    self.card = card
    self.position = position
    self.rotation = rotation

class Player:
  def __init__(self, table):
    self.hand = []
    self.table = table

  def draw_card(self, card):
    self.hand.append(card)

  def play_card(self):
    #moves = []
    #edges = [self.table.get_edge1(), self.table.get_edge2()]
    #for edge in edges:


    raise Exception("Not implemented yet!")

class Match:
  def __init__(self, cards):
    self.deck = copy.copy(cards)
    random.shuffle(self.deck)
    center_card = self.deck[0]
    self.deck = self.deck[1:]
    self.table = Table(center_card)
    self.players = [Player(self.table), Player(self.table)]
    self.setup()
    self.play()
    self.current_player_idx = 0

  def setup(self):
    for _ in range(CARDS_PER_PLAYER):
      for p in range(len(self.players)):
          card = self.deck[0]
          self.players[p].draw_card(card)
          self.deck = self.deck[1:]
  
  def play(self):
    while not self.finished():
      player = self.get_next_player()
      player.play_card()

  def get_next_player(self):
    raise Exception('Not implemented yet!')

  def finished(self):
    if len(self.deck) == 0:
      return True

    #for player in self.players:
    #  if len(player.cards) == 0:
    #    return True
    
    return False

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


class Tests(unittest.TestCase):
  def test_can_be_placed(self):
    fulano = cards[0]
    bob = cards[4]
    result = True
    self.assertEqual(result, bob.can_be_placed_on(ORIENTATION_RIGHT, fulano))
  
  def test_can_be_placed_rotation(self):
    fulano = cards[0]
    bob = cards[4]
    fulano.rotation = 1
    result = False
    self.assertEqual(result, bob.can_be_placed_on(ORIENTATION_RIGHT, fulano))
    

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
      
  ##########################
  #match = Match(cards)
  #print(match.players[0].cards)
  fulano = cards[0]
  bob = cards[4]
  print(bob.can_be_placed_on(ORIENTATION_TOP, fulano))
# TODO: fazer testes unitários
  #unittest.main()