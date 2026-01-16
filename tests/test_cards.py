"""
Testes unitários para o sistema de cartas.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from models.card import Card, Attributes, Pantheon, SyncretismLink
from data.deck_data import create_deck


class TestAttributes(unittest.TestCase):
    """Testes para a classe Attributes."""
    
    def test_create_attributes(self):
        """Testa criação de atributos."""
        attrs = Attributes(
            combat_power=80,
            wisdom=70,
            justice=60,
            eternity=90
        )
        self.assertEqual(attrs.combat_power, 80)
        self.assertEqual(attrs.wisdom, 70)
        self.assertEqual(attrs.justice, 60)
        self.assertEqual(attrs.eternity, 90)
    
    def test_get_attribute(self):
        """Testa obtenção de atributo por nome."""
        attrs = Attributes(85, 75, 65, 95)
        self.assertEqual(attrs.get_attribute("combat_power"), 85)
        self.assertEqual(attrs.get_attribute("wisdom"), 75)
        self.assertEqual(attrs.get_attribute("invalid"), 0)
    
    def test_apply_bonus(self):
        """Testa aplicação de bônus."""
        attrs = Attributes(80, 70, 60, 90)
        bonus = {"combat_power": 10, "wisdom": 5}
        new_attrs = attrs.apply_bonus(bonus)
        
        self.assertEqual(new_attrs.combat_power, 90)
        self.assertEqual(new_attrs.wisdom, 75)
        self.assertEqual(new_attrs.justice, 60)  # Inalterado
        
    def test_bonus_cap_at_100(self):
        """Testa que bônus não ultrapassa 100."""
        attrs = Attributes(95, 70, 60, 90)
        bonus = {"combat_power": 20}
        new_attrs = attrs.apply_bonus(bonus)
        
        self.assertEqual(new_attrs.combat_power, 100)


class TestCard(unittest.TestCase):
    """Testes para a classe Card."""
    
    def setUp(self):
        """Prepara cartas para teste."""
        self.zeus = Card(
            card_id="1A",
            group=1,
            name="Zeus",
            pantheon=Pantheon.GRECO_ROMAN,
            base_attributes=Attributes(95, 85, 80, 100),
            syncretism_links=[
                SyncretismLink("Júpiter", Pantheon.GRECO_ROMAN, {"justice": 10}),
                SyncretismLink("Amon-Rá", Pantheon.EGYPTIAN, {"wisdom": 15})
            ],
            is_super_trump=True
        )
        
        self.thor = Card(
            card_id="2A",
            group=2,
            name="Thor",
            pantheon=Pantheon.NORSE,
            base_attributes=Attributes(100, 50, 70, 55)
        )
    
    def test_card_creation(self):
        """Testa criação de carta."""
        self.assertEqual(self.zeus.name, "Zeus")
        self.assertEqual(self.zeus.pantheon, Pantheon.GRECO_ROMAN)
        self.assertTrue(self.zeus.is_super_trump)
    
    def test_current_name(self):
        """Testa nome atual considerando sincretismo."""
        self.assertEqual(self.zeus.current_name, "Zeus")
        
        self.zeus.activate_syncretism(Pantheon.EGYPTIAN)
        self.assertEqual(self.zeus.current_name, "Amon-Rá")
    
    def test_syncretism_activation(self):
        """Testa ativação de sincretismo."""
        # Antes do sincretismo
        original_wisdom = self.zeus.current_attributes.wisdom
        
        # Ativar sincretismo egípcio (+15 sabedoria)
        result = self.zeus.activate_syncretism(Pantheon.EGYPTIAN)
        self.assertTrue(result)
        self.assertEqual(self.zeus.current_pantheon, Pantheon.EGYPTIAN)
        self.assertEqual(
            self.zeus.current_attributes.wisdom, 
            min(100, original_wisdom + 15)
        )
    
    def test_syncretism_reset(self):
        """Testa reset de sincretismo."""
        self.zeus.activate_syncretism(Pantheon.EGYPTIAN)
        self.zeus.reset_syncretism()
        
        self.assertEqual(self.zeus.current_pantheon, Pantheon.GRECO_ROMAN)
        self.assertEqual(self.zeus.current_name, "Zeus")
    
    def test_card_comparison(self):
        """Testa comparação entre cartas."""
        # Thor tem mais combate
        result = self.thor.compare(self.zeus, "combat_power")
        self.assertEqual(result, 1)
        
        # Zeus tem mais sabedoria
        result = self.zeus.compare(self.thor, "wisdom")
        self.assertEqual(result, 1)
    
    def test_super_trump_wins(self):
        """Testa que Super Trunfo vence."""
        # Mesmo com atributo menor, Super Trunfo vence
        result = self.zeus.compare(self.thor, "combat_power")
        self.assertEqual(result, 1)
    
    def test_protection(self):
        """Testa sistema de proteção."""
        self.thor.apply_protection(3)
        
        self.assertTrue(self.thor.is_protected)
        self.assertEqual(self.thor.protection_turns, 3)
        self.assertFalse(self.thor.can_be_destroyed())
        
        # Diminuir proteção
        self.thor.decrease_protection()
        self.assertEqual(self.thor.protection_turns, 2)
        
        self.thor.decrease_protection()
        self.thor.decrease_protection()
        
        self.assertFalse(self.thor.is_protected)
        self.assertTrue(self.thor.can_be_destroyed())
    
    def test_destroy(self):
        """Testa destruição de carta."""
        self.assertTrue(self.thor.destroy())
        self.assertTrue(self.thor.is_destroyed)
        
        # Não pode destruir novamente
        self.assertFalse(self.thor.destroy())
        
    def test_protected_card_cannot_be_destroyed(self):
        """Testa que carta protegida não pode ser destruída."""
        self.thor.apply_protection(2)
        self.assertFalse(self.thor.destroy())
        self.assertFalse(self.thor.is_destroyed)


class TestDeck(unittest.TestCase):
    """Testes para o baralho completo."""
    
    def test_deck_size(self):
        """Testa que o baralho tem 32 cartas."""
        deck = create_deck()
        self.assertEqual(len(deck), 32)
    
    def test_deck_groups(self):
        """Testa que há 8 grupos com 4 cartas cada."""
        deck = create_deck()
        groups = {}
        
        for card in deck:
            if card.group not in groups:
                groups[card.group] = []
            groups[card.group].append(card)
        
        self.assertEqual(len(groups), 8)
        for group_num, cards in groups.items():
            self.assertEqual(len(cards), 4, f"Grupo {group_num} não tem 4 cartas")
    
    def test_card_ids_format(self):
        """Testa formato dos IDs das cartas."""
        deck = create_deck()
        
        for card in deck:
            self.assertRegex(card.card_id, r'^[1-8][A-D]$')
    
    def test_super_trump_exists(self):
        """Testa que existe um Super Trunfo."""
        deck = create_deck()
        super_trumps = [c for c in deck if c.is_super_trump]
        
        self.assertEqual(len(super_trumps), 1)
        self.assertEqual(super_trumps[0].name, "Zeus")
    
    def test_all_pantheons_represented(self):
        """Testa que todos os panteões estão representados."""
        deck = create_deck()
        pantheons = set(card.pantheon for card in deck)
        
        self.assertEqual(len(pantheons), 4)
        self.assertIn(Pantheon.EGYPTIAN, pantheons)
        self.assertIn(Pantheon.NORSE, pantheons)
        self.assertIn(Pantheon.GRECO_ROMAN, pantheons)
        self.assertIn(Pantheon.MESOPOTAMIAN, pantheons)


if __name__ == "__main__":
    unittest.main()
