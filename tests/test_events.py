"""
Testes unitários para os eventos mitológicos.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from models.card import Card, Attributes, Pantheon
from models.events import (
    RagnarokEvent, OsirisJudgmentEvent, BifrostEvent, MysteriesEvent,
    EventType, create_event
)
from game.game_state import GameState
from game.player import Player


class MockGameState:
    """GameState simplificado para testes."""
    
    def __init__(self):
        self.players = []
        self.cards_in_play = []
        self.devoured_cards = []
    
    def get_player(self, player_id):
        for p in self.players:
            if p.id == player_id:
                return p
        return None
    
    def redistribute_cards(self):
        pass
    
    def add_to_devoured(self, card):
        self.devoured_cards.append(card)


class TestOsirisJudgmentEvent(unittest.TestCase):
    """Testes para o Julgamento de Osíris."""
    
    def setUp(self):
        self.game = MockGameState()
        self.player1 = Player(id=0, name="Player 1")
        self.player2 = Player(id=1, name="Player 2")
        self.game.players = [self.player1, self.player2]
        
        # Carta com alta justiça (sobrevive)
        self.just_card = Card(
            card_id="4A",
            group=4,
            name="Maat",
            pantheon=Pantheon.EGYPTIAN,
            base_attributes=Attributes(30, 85, 100, 100)  # Justiça = 100
        )
        
        # Carta com baixa justiça (devorada)
        self.unjust_card = Card(
            card_id="2D",
            group=2,
            name="Nergal",
            pantheon=Pantheon.MESOPOTAMIAN,
            base_attributes=Attributes(88, 50, 40, 85)  # Justiça = 40
        )
        
        self.event = OsirisJudgmentEvent()
    
    def test_can_activate(self):
        """Testa condições de ativação."""
        # Sem cartas, não pode ativar
        self.assertFalse(self.event.can_activate(self.game, 0))
        
        # Com carta no oponente, pode ativar
        self.player2.add_card(self.just_card)
        self.assertTrue(self.event.can_activate(self.game, 0))
    
    def test_judgment_pass(self):
        """Testa carta que passa no julgamento."""
        self.player2.add_card(self.just_card)
        
        result = self.event.execute(
            self.game, 
            player_id=0, 
            target_player_id=1,
            target_card_id="4A"
        )
        
        self.assertTrue(result.success)
        self.assertIn("passou no Julgamento", result.message)
        self.assertFalse(self.just_card.is_destroyed)
    
    def test_judgment_fail_devoured(self):
        """Testa carta que falha e é devorada."""
        self.player2.add_card(self.unjust_card)
        
        result = self.event.execute(
            self.game,
            player_id=0,
            target_player_id=1,
            target_card_id="2D"
        )
        
        self.assertTrue(result.success)
        self.assertIn("Ammit devorou", result.message)
        self.assertTrue(self.unjust_card.is_destroyed)
        self.assertIn(self.unjust_card, self.game.devoured_cards)
    
    def test_protected_card_survives(self):
        """Testa que carta protegida não é julgada."""
        self.unjust_card.apply_protection(2)
        self.player2.add_card(self.unjust_card)
        
        result = self.event.execute(
            self.game,
            player_id=0,
            target_player_id=1,
            target_card_id="2D"
        )
        
        self.assertFalse(result.success)
        self.assertIn("protegida", result.message)
        self.assertFalse(self.unjust_card.is_destroyed)


class TestBifrostEvent(unittest.TestCase):
    """Testes para o evento Bifrost."""
    
    def setUp(self):
        self.game = MockGameState()
        self.player = Player(id=0, name="Player 1")
        self.game.players = [self.player]
        
        self.reserve_card = Card(
            card_id="3C",
            group=3,
            name="Mímir",
            pantheon=Pantheon.NORSE,
            base_attributes=Attributes(30, 98, 80, 70)
        )
        
        self.event = BifrostEvent()
    
    def test_can_activate_with_reserve(self):
        """Testa que pode ativar com cartas na reserva."""
        self.player.add_to_reserve(self.reserve_card)
        self.assertTrue(self.event.can_activate(self.game, 0))
    
    def test_cannot_activate_empty_reserve(self):
        """Testa que não pode ativar com reserva vazia."""
        self.assertFalse(self.event.can_activate(self.game, 0))
    
    def test_summon_card(self):
        """Testa invocação de carta."""
        self.player.add_to_reserve(self.reserve_card)
        
        result = self.event.execute(self.game, player_id=0, card_id="3C")
        
        self.assertTrue(result.success)
        self.assertIn("Bifrost brilha", result.message)
        self.assertIn(self.reserve_card, self.player.hand)
        self.assertNotIn(self.reserve_card, self.player.reserve)


class TestMysteriesEvent(unittest.TestCase):
    """Testes para os Mistérios de Ísis/Orfeu."""
    
    def setUp(self):
        self.game = MockGameState()
        self.player = Player(id=0, name="Player 1")
        self.game.players = [self.player]
        
        self.card = Card(
            card_id="7A",
            group=7,
            name="Ísis",
            pantheon=Pantheon.EGYPTIAN,
            base_attributes=Attributes(60, 95, 85, 95)
        )
        
        self.event = MysteriesEvent()
    
    def test_apply_protection(self):
        """Testa aplicação de proteção."""
        self.player.add_card(self.card)
        
        result = self.event.execute(self.game, player_id=0)
        
        self.assertTrue(result.success)
        self.assertTrue(self.card.is_protected)
        self.assertEqual(self.card.protection_turns, 3)
    
    def test_cannot_protect_already_protected(self):
        """Testa que não protege carta já protegida."""
        self.card.apply_protection(2)
        self.player.add_card(self.card)
        
        result = self.event.execute(self.game, player_id=0)
        
        self.assertFalse(result.success)


class TestEventFactory(unittest.TestCase):
    """Testes para a factory de eventos."""
    
    def test_create_ragnarok(self):
        """Testa criação do Ragnarök."""
        event = create_event(EventType.RAGNAROK)
        self.assertIsInstance(event, RagnarokEvent)
    
    def test_create_osiris(self):
        """Testa criação do Julgamento de Osíris."""
        event = create_event(EventType.OSIRIS_JUDGMENT)
        self.assertIsInstance(event, OsirisJudgmentEvent)
    
    def test_create_bifrost(self):
        """Testa criação do Bifrost."""
        event = create_event(EventType.BIFROST)
        self.assertIsInstance(event, BifrostEvent)
    
    def test_create_mysteries(self):
        """Testa criação dos Mistérios."""
        event = create_event(EventType.MYSTERIES)
        self.assertIsInstance(event, MysteriesEvent)


if __name__ == "__main__":
    unittest.main()
