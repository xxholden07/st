"""
Modelo de Carta - Define a estrutura de dados para as cartas do jogo.
32 cartas organizadas em 8 grupos de 4 (1A-1D até 8A-8D).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List


class Pantheon(Enum):
    """Panteões disponíveis no jogo."""
    EGYPTIAN = "Egípcio"
    NORSE = "Nórdico"
    GRECO_ROMAN = "Greco-Romano"
    MESOPOTAMIAN = "Mesopotâmico"


@dataclass
class Attributes:
    """Atributos numéricos da carta para comparação."""
    combat_power: int  # Poder de Combate (0-100)
    wisdom: int        # Sabedoria/Conhecimento (0-100)
    justice: int       # Justiça/Verdade (0-100)
    eternity: int      # Eternidade (0-100)
    
    def get_attribute(self, name: str) -> int:
        """Retorna o valor de um atributo pelo nome."""
        attr_map = {
            "combat_power": self.combat_power,
            "wisdom": self.wisdom,
            "justice": self.justice,
            "eternity": self.eternity
        }
        return attr_map.get(name, 0)
    
    def apply_bonus(self, bonus: Dict[str, int]) -> 'Attributes':
        """Aplica bônus aos atributos e retorna uma nova instância."""
        return Attributes(
            combat_power=min(100, self.combat_power + bonus.get("combat_power", 0)),
            wisdom=min(100, self.wisdom + bonus.get("wisdom", 0)),
            justice=min(100, self.justice + bonus.get("justice", 0)),
            eternity=min(100, self.eternity + bonus.get("eternity", 0))
        )


@dataclass
class SyncretismLink:
    """Define a equivalência de uma divindade em outro panteão."""
    deity_name: str
    pantheon: Pantheon
    attribute_bonus: Dict[str, int] = field(default_factory=dict)


@dataclass
class Card:
    """
    Representa uma carta do jogo.
    Cada carta contém uma divindade com seus atributos e possíveis sincretismos.
    """
    # Identificação
    card_id: str  # Ex: "1A", "2B", etc.
    group: int    # Grupo da carta (1-8)
    name: str     # Nome da divindade
    pantheon: Pantheon  # Panteão original
    
    # Atributos base
    base_attributes: Attributes
    
    # Sincretismo - equivalências em outros panteões
    syncretism_links: List[SyncretismLink] = field(default_factory=list)
    
    # Estado atual
    current_pantheon: Optional[Pantheon] = None
    is_super_trump: bool = False  # Super Trunfo
    is_destroyed: bool = False    # Destruída por evento
    is_protected: bool = False    # Protegida por Mistérios de Ísis/Orfeu
    protection_turns: int = 0     # Rodadas de proteção restantes
    
    def __post_init__(self):
        if self.current_pantheon is None:
            self.current_pantheon = self.pantheon
    
    @property
    def current_attributes(self) -> Attributes:
        """Retorna os atributos atuais considerando bônus de sincretismo."""
        if self.current_pantheon == self.pantheon:
            return self.base_attributes
        
        # Encontra o link de sincretismo ativo
        for link in self.syncretism_links:
            if link.pantheon == self.current_pantheon:
                return self.base_attributes.apply_bonus(link.attribute_bonus)
        
        return self.base_attributes
    
    @property
    def current_name(self) -> str:
        """Retorna o nome atual da divindade (considerando sincretismo)."""
        if self.current_pantheon == self.pantheon:
            return self.name
        
        for link in self.syncretism_links:
            if link.pantheon == self.current_pantheon:
                return link.deity_name
        
        return self.name
    
    def activate_syncretism(self, target_pantheon: Pantheon) -> bool:
        """
        Ativa o sincretismo para transformar a carta em sua versão equivalente.
        Retorna True se a transformação foi bem-sucedida.
        """
        if target_pantheon == self.pantheon:
            self.current_pantheon = self.pantheon
            return True
        
        for link in self.syncretism_links:
            if link.pantheon == target_pantheon:
                self.current_pantheon = target_pantheon
                return True
        
        return False
    
    def reset_syncretism(self):
        """Retorna a carta ao seu panteão original."""
        self.current_pantheon = self.pantheon
    
    def apply_protection(self, turns: int):
        """Aplica proteção dos Mistérios de Ísis/Orfeu."""
        self.is_protected = True
        self.protection_turns = turns
    
    def decrease_protection(self):
        """Diminui a contagem de proteção."""
        if self.protection_turns > 0:
            self.protection_turns -= 1
            if self.protection_turns == 0:
                self.is_protected = False
    
    def can_be_destroyed(self) -> bool:
        """Verifica se a carta pode ser destruída."""
        return not self.is_protected and not self.is_destroyed
    
    def destroy(self):
        """Marca a carta como destruída (Segunda Morte)."""
        if self.can_be_destroyed():
            self.is_destroyed = True
            return True
        return False
    
    def compare(self, other: 'Card', attribute: str) -> int:
        """
        Compara esta carta com outra usando o atributo especificado.
        Retorna: 1 se vencer, -1 se perder, 0 se empatar.
        """
        # Super Trunfo vence todas exceto outro Super Trunfo
        if self.is_super_trump and not other.is_super_trump:
            return 1
        if not self.is_super_trump and other.is_super_trump:
            return -1
        
        my_value = self.current_attributes.get_attribute(attribute)
        other_value = other.current_attributes.get_attribute(attribute)
        
        if my_value > other_value:
            return 1
        elif my_value < other_value:
            return -1
        return 0
    
    def __str__(self) -> str:
        return f"[{self.card_id}] {self.current_name} ({self.current_pantheon.value})"
    
    def __repr__(self) -> str:
        attrs = self.current_attributes
        return (f"Card({self.card_id}, {self.current_name}, "
                f"C:{attrs.combat_power} S:{attrs.wisdom} "
                f"J:{attrs.justice} E:{attrs.eternity})")
