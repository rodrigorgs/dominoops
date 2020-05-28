import gameSimulation as sim
import csv
import json
import random
import copy
import unittest

class Tests(unittest.TestCase):
  def test_can_be_placed(self):
    fulano = cards[0]
    bob = cards[4]
    result = True
    self.assertEqual(result, bob.can_be_placed_on(sim.ORIENTATION_RIGHT, fulano))
  
  def test_can_be_placed_on_rotation(self):
    fulano = cards[0]
    bob = cards[4]
    fulano.rotation = 1
    result = False
    self.assertEqual(result, bob.can_be_placed_on(sim.ORIENTATION_RIGHT, fulano))

  def test_is_descendant(self):
    fulano = cards[0]
    bob = cards[4]
    result = True
    self.assertEqual(result, bob.klass.is_descendant_of(fulano.klass))

  def test_can_be_placed_on_top_1(self):
    fulano = cards[0]
    sicrana = cards[1]
    result = False
    self.assertEqual(result, fulano.can_be_placed_on(sim.ORIENTATION_TOP, sicrana))

  def test_can_be_placed_on_top_2(self):
    fulano = cards[0]
    bob = cards[4]
    result = True
    self.assertEqual(result, bob.can_be_placed_on(sim.ORIENTATION_TOP, fulano))
    
if __name__ == '__main__':

  fileCsv = open('base-classes.csv', 'r')
  reader = csv.DictReader(fileCsv)
  klasses = {}

  # Mapeia para um dicionario

  for row in reader:
    klasses[row['class']] = row

  # Instancia objetos a partir do dicionario
  manager = sim.KlassManager()
  cardsObj = [] # É a lista de objetos Klass
  for card in klasses:
      c = klasses[card]
      klass = manager.get_klass(c['class'])
      klass.add_superklass(manager.get_klass(c['hierarchy']))
      klass.set_klass_at_orientation(sim.ORIENTATION_TOP, manager.get_klass(c['topClass']))
      klass.set_klass_at_orientation(sim.ORIENTATION_RIGHT, manager.get_klass(c['rightClass']))
      klass.set_klass_at_orientation(sim.ORIENTATION_BOTTOM, manager.get_klass(c['bottomClass']))
      klass.set_klass_at_orientation(sim.ORIENTATION_LEFT, manager.get_klass(c['leftClass']))
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
      card = sim.Card(row['object'], klass)
      cards.append(card)
      
  unittest.main()