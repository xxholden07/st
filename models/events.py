"""
Eventos Mitológicos - Cartas especiais que alteram o fluxo da partida.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .card import Card
    from game.game_state import GameState


class EventType(Enum):
    """Tipos de eventos mitológicos."""
    RAGNAROK = "Ragnarök"
    OSIRIS_JUDGMENT = "Julgamento de Osíris"
    BIFROST = "Bifrost"
    MYSTERIES = "Mistérios de Ísis/Orfeu"


@dataclass
class EventResult:
    """Resultado da execução de um evento."""
    success: bool
    message: str
    affected_cards: List[str] = None  # IDs das cartas afetadas
    
    def __post_init__(self):
        if self.affected_cards is None:
            self.affected_cards = []


class MythologicalEvent(ABC):
    """Classe base abstrata para eventos mitológicos."""
    
    def __init__(self, name: str, event_type: EventType, description: str):
        self.name = name
        self.event_type = event_type
        self.description = description
    
    @abstractmethod
    def execute(self, game_state: 'GameState', player_id: int) -> EventResult:
        """Executa o evento e retorna o resultado."""
        pass
    
    @abstractmethod
    def can_activate(self, game_state: 'GameState', player_id: int) -> bool:
        """Verifica se o evento pode ser ativado nas condições atuais."""
        pass


class RagnarokEvent(MythologicalEvent):
    """
    Evento Ragnarök - O Destino Final dos Deuses.
    Destrói todas as cartas em jogo, forçando um reinício com novas divindades.
    """
    
    def __init__(self):
        super().__init__(
            name="Ragnarök",
            event_type=EventType.RAGNAROK,
            description="O crepúsculo dos deuses. Todas as cartas em jogo são destruídas, "
                       "e novas divindades repovoam os reinos."
        )
    
    def can_activate(self, game_state: 'GameState', player_id: int) -> bool:
        """Pode ser ativado se houver cartas em jogo."""
        return len(game_state.cards_in_play) > 0
    
    def execute(self, game_state: 'GameState', player_id: int) -> EventResult:
        """Destrói todas as cartas em jogo e redistribui novas."""
        destroyed_cards = []
        
        # Destruir todas as cartas não protegidas
        for player in game_state.players:
            for card in player.hand:
                if card.can_be_destroyed():
                    card.destroy()
                    destroyed_cards.append(card.card_id)
        
        # Simula a redistribuição de novas cartas
        game_state.redistribute_cards()
        
        return EventResult(
            success=True,
            message=f"Ragnarök! {len(destroyed_cards)} cartas foram consumidas pelo destino. "
                   "Novas divindades emergem do caos primordial.",
            affected_cards=destroyed_cards
        )


class OsirisJudgmentEvent(MythologicalEvent):
    """
    Evento Julgamento de Osíris - A Segunda Morte.
    O coração da carta é pesado contra a Pena da Verdade (Maat).
    Se Justiça < 50, a carta é devorada por Ammit e removida permanentemente.
    """
    
    JUSTICE_THRESHOLD = 50  # Limiar de justiça para sobreviver
    
    def __init__(self):
        super().__init__(
            name="Julgamento de Osíris",
            event_type=EventType.OSIRIS_JUDGMENT,
            description="O coração é pesado contra a Pena da Verdade. "
                       "Aqueles sem justiça sofrem a Segunda Morte nas garras de Ammit."
        )
    
    def can_activate(self, game_state: 'GameState', player_id: int) -> bool:
        """Pode ser ativado contra um oponente que tenha cartas."""
        for player in game_state.players:
            if player.id != player_id and len(player.hand) > 0:
                return True
        return False
    
    def execute(self, game_state: 'GameState', player_id: int, 
                target_player_id: int = None, target_card_id: str = None) -> EventResult:
        """
        Julga uma carta específica ou uma carta aleatória do oponente.
        """
        # Encontrar oponente
        target_player = None
        for player in game_state.players:
            if target_player_id and player.id == target_player_id:
                target_player = player
                break
            elif player.id != player_id:
                target_player = player
                break
        
        if not target_player or len(target_player.hand) == 0:
            return EventResult(
                success=False,
                message="Não há cartas para julgar."
            )
        
        # Selecionar carta a ser julgada
        target_card = None
        if target_card_id:
            for card in target_player.hand:
                if card.card_id == target_card_id:
                    target_card = card
                    break
        
        if not target_card:
            target_card = random.choice(target_player.hand)
        
        # Verificar proteção
        if target_card.is_protected:
            return EventResult(
                success=False,
                message=f"{target_card.current_name} está protegida pelos Mistérios Sagrados."
            )
        
        # Realizar o julgamento
        justice_value = target_card.current_attributes.justice
        
        if justice_value < self.JUSTICE_THRESHOLD:
            target_card.destroy()
            target_player.remove_card(target_card)
            game_state.add_to_devoured(target_card)  # Removida permanentemente
            
            return EventResult(
                success=True,
                message=f"O coração de {target_card.current_name} foi mais pesado que a Pena. "
                       f"Ammit devorou a carta! (Justiça: {justice_value})",
                affected_cards=[target_card.card_id]
            )
        else:
            return EventResult(
                success=True,
                message=f"{target_card.current_name} passou no Julgamento! "
                       f"Seu coração era puro. (Justiça: {justice_value})"
            )


class BifrostEvent(MythologicalEvent):
    """
    Evento Bifrost - A Ponte Arco-Íris.
    Permite invocar uma carta de apoio do reino humano (reserva).
    """
    
    def __init__(self):
        super().__init__(
            name="Bifrost",
            event_type=EventType.BIFROST,
            description="A ponte arco-íris conecta Midgard a Asgard. "
                       "Invoque um aliado do reino dos mortais."
        )
    
    def can_activate(self, game_state: 'GameState', player_id: int) -> bool:
        """Pode ser ativado se o jogador tiver cartas na reserva."""
        player = game_state.get_player(player_id)
        return player and len(player.reserve) > 0
    
    def execute(self, game_state: 'GameState', player_id: int, 
                card_id: str = None) -> EventResult:
        """Traz uma carta da reserva para a mão."""
        player = game_state.get_player(player_id)
        
        if not player or len(player.reserve) == 0:
            return EventResult(
                success=False,
                message="Não há aliados em Midgard para invocar."
            )
        
        # Selecionar carta da reserva
        summoned_card = None
        if card_id:
            for card in player.reserve:
                if card.card_id == card_id:
                    summoned_card = card
                    break
        
        if not summoned_card:
            summoned_card = player.reserve[0]
        
        # Mover da reserva para a mão
        player.reserve.remove(summoned_card)
        player.hand.append(summoned_card)
        
        return EventResult(
            success=True,
            message=f"A Bifrost brilha! {summoned_card.current_name} atravessa a ponte "
                   f"de Midgard para Asgard!",
            affected_cards=[summoned_card.card_id]
        )


class MysteriesEvent(MythologicalEvent):
    """
    Evento Mistérios de Ísis/Orfeu - Purificação e Proteção.
    Protege cartas de serem destruídas por algumas rodadas.
    """
    
    PROTECTION_TURNS = 3  # Número de rodadas de proteção
    
    def __init__(self):
        super().__init__(
            name="Mistérios de Ísis/Orfeu",
            event_type=EventType.MYSTERIES,
            description="Os mistérios sagrados conferem purificação e proteção. "
                       "Suas cartas ficam imunes à destruição."
        )
    
    def can_activate(self, game_state: 'GameState', player_id: int) -> bool:
        """Pode ser ativado se o jogador tiver cartas desprotegidas."""
        player = game_state.get_player(player_id)
        if not player:
            return False
        
        for card in player.hand:
            if not card.is_protected:
                return True
        return False
    
    def execute(self, game_state: 'GameState', player_id: int,
                card_ids: List[str] = None) -> EventResult:
        """Aplica proteção às cartas especificadas ou a todas."""
        player = game_state.get_player(player_id)
        
        if not player:
            return EventResult(
                success=False,
                message="Jogador não encontrado."
            )
        
        protected_cards = []
        
        for card in player.hand:
            if card_ids is None or card.card_id in card_ids:
                if not card.is_protected:
                    card.apply_protection(self.PROTECTION_TURNS)
                    protected_cards.append(card.card_id)
        
        if not protected_cards:
            return EventResult(
                success=False,
                message="Nenhuma carta foi purificada."
            )
        
        return EventResult(
            success=True,
            message=f"Os Mistérios Sagrados envolvem suas divindades! "
                   f"{len(protected_cards)} carta(s) protegida(s) por {self.PROTECTION_TURNS} rodadas.",
            affected_cards=protected_cards
        )


# Registro de todos os eventos disponíveis
AVAILABLE_EVENTS = {
    EventType.RAGNAROK: RagnarokEvent,
    EventType.OSIRIS_JUDGMENT: OsirisJudgmentEvent,
    EventType.BIFROST: BifrostEvent,
    EventType.MYSTERIES: MysteriesEvent
}


def create_event(event_type: EventType) -> MythologicalEvent:
    """Factory para criar eventos."""
    event_class = AVAILABLE_EVENTS.get(event_type)
    if event_class:
        return event_class()
    raise ValueError(f"Tipo de evento desconhecido: {event_type}")
