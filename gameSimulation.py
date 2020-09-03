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
ORIENTATIONS = [ORIENTATION_TOP, ORIENTATION_RIGHT, ORIENTATION_BOTTOM, ORIENTATION_LEFT]

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def with_offset(self, p):
    return Point(self.x + p.x, self.y + p.y)

  def __eq__(self, p):
    return self.x == p.x and self.y == p.y
  
  def __hash__(self):
    return 0  # TODO

  def __str__(self):
    return "Point(" + str(self.x) + ", " + str(self.y) + ")"

orientation_to_offset = {
  ORIENTATION_TOP: Point(0, -1),
  ORIENTATION_BOTTOM: Point(0, 1),
  ORIENTATION_LEFT: Point(-1, 0),
  ORIENTATION_RIGHT: Point(1, 0)
}

offset_to_orientation = {
  Point(0, -1): ORIENTATION_TOP,
  Point(0, 1): ORIENTATION_BOTTOM,
  Point(-1, 0): ORIENTATION_LEFT,
  Point(1, 0): ORIENTATION_RIGHT,
}

class Table:
  def __init__(self, card):
    self.matrix = [[None for x in range(MATRIX_HEIGHT)] for y in range(MATRIX_HEIGHT)] 
    self.edge1_pos = Point(MATRIX_WIDTH // 2, MATRIX_HEIGHT // 2)
    self.edge2_pos = copy.copy(self.edge1_pos)
    self.put_card(card, self.edge1_pos, None)

  def get_card(self, point):
    return self.matrix[point.y][point.x]
  
  def get_card_at_orientation(self, point, orientation):
    # ex.: se point é (5, 7) e orientation é ORIENTATION_TOP,
    # então vai retornar carta no ponto (5, 6) 
    pass

  # Put card "card" on position "point", connected to the card in position "edge_point"
  def put_card(self, card, point, edge_point):
    # TODO: checar se pode colocar a carta lá
    
    self.matrix[point.y][point.x] = card

    if edge_point is not None:
      if edge_point == self.edge1_pos:
        self.edge1_pos = copy.copy(point)
      else:
        self.edge2_pos = copy.copy(point)    

  def get_available_orientations_for_card_at_position(self, point):
      return [x for x in ORIENTATIONS if self.get_card(point.with_offset(orientation_to_offset[x])) is None]

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
    moves = []
    # para cada uma das duas extremidades
    for p in [self.table.edge1_pos, self.table.edge2_pos]:
      card = self.table.get_card(p)
      orientacoes_livres = self.table.get_available_orientations_for_card_at_position(p)
      # para cada uma das laterais da carta
      for orientation in orientacoes_livres:
        attr_klass = card.get_klass_at_orientation(orientation)
        print(attr_klass)
        # considera cada uma das cartas do jogador
        for player_card in self.hand:
          # considera cada um dos lados da carta do jogador
          for player_card_orientation in ORIENTATIONS:
            player_attr_klass = player_card.get_klass_at_orientation(player_card_orientation)
            
            if player_attr_klass is not None and player_attr_klass.is_compatible_with(attr_klass):
              # movimento válido!
              player_pos = p.with_offset(orientation_to_offset[orientation])
              m = PlayerMove(player_card, player_pos, 0)   # TODO: trocar 0 pela orientação correta (CALCULAR!)
              print("Move: " + str(player_card) + ", " + str(player_pos))
              moves.append(m)
            elif attr_klass is not None and attr_klass.is_compatible_with(player_attr_klass):
              # TODO
              pass
      #     # considera jogada de upgrade
      #     if player_card.klass.can_be_placed_on_top(card):
      #       # TODO: checar adjacências
      #       pass
            
        


    # raise Exception("Not implemented yet!")

class Match:
  def __init__(self, cards):
    self.deck = copy.copy(cards)
    random.shuffle(self.deck)
    center_card = self.deck[0]
    self.deck = self.deck[1:]
    self.table = Table(center_card)
    self.players = [Player(self.table), Player(self.table)]
    self.setup()
    # self.play()
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
    pass
    #raise Exception('Not implemented yet!')

  def finished(self):
    if len(self.deck) == 0:
      return True

    #for player in self.players:
    #  if len(player.hand) == 0:
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
  match = Match(cards)

  match.table.put_card(match.deck[0], match.table.edge1_pos.with_offset(Point(1, 0)), match.table.edge1_pos)
  # print(match.table.edge1_pos)
  # print(match.table.edge2_pos)
  #print(match.players[0].hand)
  match.players[0].play_card()
  
  #unittest.main()