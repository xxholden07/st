"""
GameState - Gerencia o estado do jogo.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import random

from models.card import Card, Pantheon
from models.events import MythologicalEvent, EventType, EventResult
from game.player import Player
from data.deck_data import create_deck


class GamePhase(Enum):
    """Fases do jogo."""
    SETUP = "Preparação"
    DRAW = "Compra"
    CHOOSE_ATTRIBUTE = "Escolha de Atributo"
    BATTLE = "Batalha"
    EVENT = "Evento"
    END_TURN = "Fim do Turno"
    GAME_OVER = "Fim de Jogo"


@dataclass
class GameState:
    """Gerencia todo o estado do jogo."""
    
    players: List[Player] = field(default_factory=list)
    deck: List[Card] = field(default_factory=list)
    cards_in_play: List[Card] = field(default_factory=list)
    devoured_cards: List[Card] = field(default_factory=list)  # Cartas devoradas por Ammit
    
    current_player_index: int = 0
    current_phase: GamePhase = GamePhase.SETUP
    turn_number: int = 0
    
    # Atributo escolhido para a rodada atual
    chosen_attribute: Optional[str] = None
    
    # Histórico de eventos
    event_history: List[str] = field(default_factory=list)
    
    def initialize_game(self, player_names: List[str]):
        """Inicializa o jogo com os jogadores especificados."""
        # Criar jogadores
        self.players = [
            Player(id=i, name=name) 
            for i, name in enumerate(player_names)
        ]
        
        # Criar e embaralhar o baralho
        self.deck = create_deck()
        random.shuffle(self.deck)
        
        # Distribuir cartas
        self._distribute_cards()
        
        # Definir jogador inicial aleatoriamente
        self.current_player_index = random.randint(0, len(self.players) - 1)
        self.current_phase = GamePhase.CHOOSE_ATTRIBUTE
        self.turn_number = 1
        
        self.event_history.append(
            f"Jogo iniciado com {len(self.players)} jogadores. "
            f"{self.current_player.name} começa!"
        )
    
    def _distribute_cards(self):
        """Distribui as cartas igualmente entre os jogadores."""
        cards_per_player = len(self.deck) // len(self.players)
        reserve_cards = 2  # Cartas que vão para a reserva (Midgard)
        
        for i, player in enumerate(self.players):
            start = i * cards_per_player
            end = start + cards_per_player
            player_cards = self.deck[start:end]
            
            # Algumas vão para reserva, resto para mão
            for j, card in enumerate(player_cards):
                if j < reserve_cards:
                    player.add_to_reserve(card)
                else:
                    player.add_card(card)
    
    def redistribute_cards(self):
        """Redistribui cartas após Ragnarök."""
        # Coletar todas as cartas não destruídas
        all_cards = []
        for player in self.players:
            all_cards.extend([c for c in player.hand if not c.is_destroyed])
            all_cards.extend([c for c in player.reserve if not c.is_destroyed])
            player.hand.clear()
            player.reserve.clear()
        
        # Adicionar cartas do deck que não foram usadas
        all_cards.extend([c for c in self.deck if not c.is_destroyed])
        
        # Resetar estado das cartas
        for card in all_cards:
            card.reset_syncretism()
            card.is_protected = False
            card.protection_turns = 0
        
        random.shuffle(all_cards)
        
        # Redistribuir
        cards_per_player = len(all_cards) // len(self.players)
        for i, player in enumerate(self.players):
            start = i * cards_per_player
            end = start + cards_per_player
            for card in all_cards[start:end]:
                player.add_card(card)
    
    @property
    def current_player(self) -> Player:
        """Retorna o jogador atual."""
        return self.players[self.current_player_index]
    
    def get_player(self, player_id: int) -> Optional[Player]:
        """Retorna um jogador pelo ID."""
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def get_opponent(self, player_id: int) -> Optional[Player]:
        """Retorna o oponente de um jogador (para jogo de 2 jogadores)."""
        for player in self.players:
            if player.id != player_id:
                return player
        return None
    
    def next_player(self):
        """Avança para o próximo jogador."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def add_to_devoured(self, card: Card):
        """Adiciona uma carta às devoradas por Ammit."""
        self.devoured_cards.append(card)
    
    def choose_attribute(self, attribute: str) -> bool:
        """Define o atributo para a rodada de comparação."""
        valid_attributes = ["combat_power", "wisdom", "justice", "eternity"]
        if attribute in valid_attributes:
            self.chosen_attribute = attribute
            self.current_phase = GamePhase.BATTLE
            return True
        return False
    
    def play_cards(self, cards: Dict[int, Card]):
        """
        Jogadores colocam suas cartas para batalha.
        cards: Dict[player_id, Card]
        """
        self.cards_in_play = list(cards.values())
    
    def resolve_battle(self) -> Dict[str, any]:
        """
        Resolve a batalha atual e retorna o resultado.
        """
        if len(self.cards_in_play) < 2 or not self.chosen_attribute:
            return {"success": False, "message": "Batalha inválida"}
        
        # Para 2 jogadores
        card1 = self.cards_in_play[0]
        card2 = self.cards_in_play[1]
        
        result = card1.compare(card2, self.chosen_attribute)
        
        if result == 1:
            winner = self.players[0]
            loser = self.players[1]
            winning_card = card1
            losing_card = card2
        elif result == -1:
            winner = self.players[1]
            loser = self.players[0]
            winning_card = card2
            losing_card = card1
        else:
            # Empate - cartas retornam às mãos
            self.cards_in_play.clear()
            self.current_phase = GamePhase.END_TURN
            return {
                "success": True,
                "winner": None,
                "message": "Empate! As divindades se equivalem.",
                "attribute": self.chosen_attribute
            }
        
        # Vencedor ganha ambas as cartas
        winner.win_card(winning_card)
        winner.win_card(losing_card)
        
        # Remover cartas das mãos
        loser.remove_card(losing_card)
        
        self.cards_in_play.clear()
        self.current_phase = GamePhase.END_TURN
        
        return {
            "success": True,
            "winner": winner,
            "winning_card": winning_card,
            "losing_card": losing_card,
            "attribute": self.chosen_attribute,
            "message": f"{winner.name} vence com {winning_card.current_name}!"
        }
    
    def end_turn(self):
        """Finaliza o turno atual."""
        # Diminuir contadores de proteção
        for player in self.players:
            player.decrease_protection_counters()
        
        # Verificar condições de fim de jogo
        if self._check_game_over():
            self.current_phase = GamePhase.GAME_OVER
        else:
            self.next_player()
            self.turn_number += 1
            self.chosen_attribute = None
            self.current_phase = GamePhase.CHOOSE_ATTRIBUTE
    
    def _check_game_over(self) -> bool:
        """Verifica se o jogo acabou."""
        # Jogo acaba quando algum jogador fica sem cartas
        for player in self.players:
            if not player.has_cards():
                return True
        return False
    
    def get_winner(self) -> Optional[Player]:
        """Retorna o vencedor do jogo."""
        if self.current_phase != GamePhase.GAME_OVER:
            return None
        
        # Vencedor é quem tem mais pontos
        return max(self.players, key=lambda p: p.score)
    
    def execute_event(self, event: MythologicalEvent, 
                      player_id: int, **kwargs) -> EventResult:
        """Executa um evento mitológico."""
        player = self.get_player(player_id)
        
        if not player:
            return EventResult(False, "Jogador não encontrado.")
        
        if not player.use_event():
            return EventResult(False, "Sem eventos disponíveis.")
        
        if not event.can_activate(self, player_id):
            player.events_available += 1  # Devolve o evento
            return EventResult(False, "Condições para o evento não satisfeitas.")
        
        result = event.execute(self, player_id, **kwargs)
        
        if result.success:
            self.event_history.append(
                f"Turno {self.turn_number}: {player.name} ativou {event.name} - {result.message}"
            )
        
        return result
    
    def get_game_status(self) -> str:
        """Retorna um resumo do estado atual do jogo."""
        status = [
            f"=== TURNO {self.turn_number} ===",
            f"Fase: {self.current_phase.value}",
            f"Jogador atual: {self.current_player.name}",
            ""
        ]
        
        for player in self.players:
            status.append(player.show_stats())
            status.append("")
        
        if self.devoured_cards:
            status.append(f"Cartas devoradas por Ammit: {len(self.devoured_cards)}")
        
        return "\n".join(status)
