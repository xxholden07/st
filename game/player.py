"""
Classe Player - Representa um jogador no jogo.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from models.card import Card


@dataclass
class Player:
    """Representa um jogador no jogo de cartas mitológicas."""
    
    id: int
    name: str
    hand: List[Card] = field(default_factory=list)      # Cartas na mão
    reserve: List[Card] = field(default_factory=list)   # Cartas em reserva (Midgard)
    won_cards: List[Card] = field(default_factory=list) # Cartas ganhas em disputas
    score: int = 0
    events_available: int = 2  # Quantidade de eventos que pode usar por partida
    
    def add_card(self, card: Card):
        """Adiciona uma carta à mão do jogador."""
        self.hand.append(card)
    
    def add_to_reserve(self, card: Card):
        """Adiciona uma carta à reserva."""
        self.reserve.append(card)
    
    def remove_card(self, card: Card) -> bool:
        """Remove uma carta da mão do jogador."""
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False
    
    def remove_from_reserve(self, card: Card) -> bool:
        """Remove uma carta da reserva."""
        if card in self.reserve:
            self.reserve.remove(card)
            return True
        return False
    
    def get_card(self, card_id: str) -> Optional[Card]:
        """Retorna uma carta específica da mão pelo ID."""
        for card in self.hand:
            if card.card_id == card_id:
                return card
        return None
    
    def get_card_from_reserve(self, card_id: str) -> Optional[Card]:
        """Retorna uma carta específica da reserva pelo ID."""
        for card in self.reserve:
            if card.card_id == card_id:
                return card
        return None
    
    def win_card(self, card: Card):
        """Adiciona uma carta às cartas ganhas."""
        self.won_cards.append(card)
        self.score += self._calculate_card_value(card)
    
    def _calculate_card_value(self, card: Card) -> int:
        """Calcula o valor de pontos de uma carta."""
        attrs = card.current_attributes
        base_value = (attrs.combat_power + attrs.wisdom + 
                     attrs.justice + attrs.eternity) // 4
        
        # Super Trunfo vale mais
        if card.is_super_trump:
            base_value += 50
        
        return base_value
    
    def has_cards(self) -> bool:
        """Verifica se o jogador ainda tem cartas na mão."""
        return len(self.hand) > 0
    
    def total_cards(self) -> int:
        """Retorna o total de cartas (mão + reserva)."""
        return len(self.hand) + len(self.reserve)
    
    def decrease_protection_counters(self):
        """Diminui os contadores de proteção de todas as cartas."""
        for card in self.hand:
            card.decrease_protection()
        for card in self.reserve:
            card.decrease_protection()
    
    def use_event(self) -> bool:
        """Usa um evento disponível. Retorna False se não houver eventos."""
        if self.events_available > 0:
            self.events_available -= 1
            return True
        return False
    
    def __str__(self) -> str:
        return f"{self.name} (Cartas: {len(self.hand)}, Pontos: {self.score})"
    
    def show_hand(self) -> str:
        """Retorna uma representação visual da mão do jogador."""
        if not self.hand:
            return f"{self.name}: [Mão Vazia]"
        
        cards_str = "\n".join([f"  {card}" for card in self.hand])
        return f"{self.name} - Mão ({len(self.hand)} cartas):\n{cards_str}"
    
    def show_stats(self) -> str:
        """Mostra estatísticas detalhadas do jogador."""
        return (f"=== {self.name} ===\n"
                f"Cartas na mão: {len(self.hand)}\n"
                f"Cartas na reserva: {len(self.reserve)}\n"
                f"Cartas ganhas: {len(self.won_cards)}\n"
                f"Pontuação: {self.score}\n"
                f"Eventos disponíveis: {self.events_available}")
