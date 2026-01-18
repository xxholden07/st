"""
Sistema de Ranking Estilo Arcade.
Gerencia pontuações, recordes e tabela de líderes.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class RankingEntry:
    """Uma entrada no ranking."""
    name: str
    score: int
    wins: int
    battles: int
    pantheon_bonus: int  # Bônus por dominar panteões
    date: str
    
    @property
    def win_rate(self) -> float:
        """Taxa de vitória."""
        if self.battles == 0:
            return 0.0
        return (self.wins / self.battles) * 100
    
    @property
    def total_score(self) -> int:
        """Pontuação total com bônus."""
        return self.score + self.pantheon_bonus


class RankingSystem:
    """Sistema de ranking e recordes."""
    
    MAX_ENTRIES = 10  # Top 10
    RANKING_FILE = "ranking.json"
    
    # Títulos baseados na pontuação
    TITLES = [
        (10000, "DEUS SUPREMO", "#ffd700"),
        (7500, "DIVINDADE MAIOR", "#ff8800"),
        (5000, "SENHOR DOS PANTEÕES", "#ff4444"),
        (3500, "CAMPEÃO CELESTIAL", "#aa44ff"),
        (2500, "GUERREIRO DIVINO", "#4488ff"),
        (1500, "AVATAR SAGRADO", "#44ff88"),
        (1000, "INICIADO MÍTICO", "#88ffff"),
        (500, "APRENDIZ DOS DEUSES", "#ffffff"),
        (0, "MORTAL", "#888888"),
    ]
    
    # Pontuação por ações
    POINTS = {
        "victory": 100,           # Vitória em batalha
        "super_trump_win": 200,   # Vitória com Super Trunfo
        "syncretism_win": 150,    # Vitória usando sincretismo
        "event_used": 50,         # Usar evento mitológico
        "perfect_game": 500,      # Vencer sem perder nenhuma batalha
        "pantheon_dominated": 300, # Coletar todas cartas de um panteão
        "game_won": 1000,         # Vencer o jogo
        "cards_collected": 10,    # Por carta conquistada
    }
    
    def __init__(self):
        self.ranking_path = Path(__file__).parent / self.RANKING_FILE
        self.entries: List[RankingEntry] = []
        self.current_session_score = 0
        self.current_session_stats = {
            "wins": 0,
            "losses": 0,
            "battles": 0,
            "events_used": 0,
            "syncretisms": 0,
            "super_trump_wins": 0,
            "cards_won": 0,
            "pantheons_dominated": set(),
        }
        self.load_ranking()
    
    def load_ranking(self):
        """Carrega o ranking do arquivo."""
        try:
            if self.ranking_path.exists():
                with open(self.ranking_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [RankingEntry(**entry) for entry in data]
        except Exception as e:
            print(f"Erro ao carregar ranking: {e}")
            self.entries = []
    
    def save_ranking(self):
        """Salva o ranking no arquivo."""
        try:
            with open(self.ranking_path, 'w', encoding='utf-8') as f:
                data = [asdict(entry) for entry in self.entries]
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")
    
    def reset_session(self):
        """Reseta estatísticas da sessão atual."""
        self.current_session_score = 0
        self.current_session_stats = {
            "wins": 0,
            "losses": 0,
            "battles": 0,
            "events_used": 0,
            "syncretisms": 0,
            "super_trump_wins": 0,
            "cards_won": 0,
            "pantheons_dominated": set(),
        }
    
    def add_points(self, action: str, multiplier: int = 1) -> int:
        """Adiciona pontos por uma ação."""
        points = self.POINTS.get(action, 0) * multiplier
        self.current_session_score += points
        return points
    
    def record_battle_win(self, used_super_trump: bool = False, used_syncretism: bool = False):
        """Registra uma vitória em batalha."""
        self.current_session_stats["wins"] += 1
        self.current_session_stats["battles"] += 1
        self.current_session_stats["cards_won"] += 1
        
        points = self.add_points("victory")
        
        if used_super_trump:
            self.current_session_stats["super_trump_wins"] += 1
            points += self.add_points("super_trump_win")
        
        if used_syncretism:
            self.current_session_stats["syncretisms"] += 1
            points += self.add_points("syncretism_win")
        
        self.add_points("cards_collected")
        
        return points
    
    def record_battle_loss(self):
        """Registra uma derrota em batalha."""
        self.current_session_stats["losses"] += 1
        self.current_session_stats["battles"] += 1
    
    def record_event_used(self):
        """Registra uso de evento."""
        self.current_session_stats["events_used"] += 1
        return self.add_points("event_used")
    
    def record_pantheon_dominated(self, pantheon_name: str):
        """Registra domínio de um panteão."""
        if pantheon_name not in self.current_session_stats["pantheons_dominated"]:
            self.current_session_stats["pantheons_dominated"].add(pantheon_name)
            return self.add_points("pantheon_dominated")
        return 0
    
    def record_game_won(self) -> int:
        """Registra vitória no jogo."""
        points = self.add_points("game_won")
        
        # Bônus por jogo perfeito (sem derrotas)
        if self.current_session_stats["losses"] == 0:
            points += self.add_points("perfect_game")
        
        return points
    
    def get_title(self, score: int) -> tuple:
        """Retorna o título baseado na pontuação."""
        for min_score, title, color in self.TITLES:
            if score >= min_score:
                return title, color
        return "MORTAL", "#888888"
    
    def calculate_pantheon_bonus(self) -> int:
        """Calcula bônus por panteões dominados."""
        return len(self.current_session_stats["pantheons_dominated"]) * self.POINTS["pantheon_dominated"]
    
    def submit_score(self, player_name: str) -> tuple:
        """
        Submete a pontuação atual ao ranking.
        
        Returns:
            (position, is_new_record) - Posição no ranking e se é novo recorde
        """
        pantheon_bonus = self.calculate_pantheon_bonus()
        
        entry = RankingEntry(
            name=player_name[:10].upper(),  # Máximo 10 caracteres, estilo arcade
            score=self.current_session_score,
            wins=self.current_session_stats["wins"],
            battles=self.current_session_stats["battles"],
            pantheon_bonus=pantheon_bonus,
            date=datetime.now().strftime("%d/%m/%Y")
        )
        
        # Insere na posição correta
        inserted = False
        for i, existing in enumerate(self.entries):
            if entry.total_score > existing.total_score:
                self.entries.insert(i, entry)
                inserted = True
                break
        
        if not inserted:
            self.entries.append(entry)
        
        # Mantém apenas top 10
        self.entries = self.entries[:self.MAX_ENTRIES]
        
        # Verifica posição
        position = -1
        is_new_record = False
        for i, e in enumerate(self.entries):
            if e.name == entry.name and e.score == entry.score and e.date == entry.date:
                position = i + 1
                is_new_record = (position == 1)
                break
        
        self.save_ranking()
        return position, is_new_record
    
    def get_ranking(self) -> List[RankingEntry]:
        """Retorna o ranking atual."""
        return self.entries
    
    def is_high_score(self) -> bool:
        """Verifica se a pontuação atual entra no ranking."""
        if len(self.entries) < self.MAX_ENTRIES:
            return True
        return self.current_session_score > self.entries[-1].total_score
    
    def get_session_summary(self) -> Dict:
        """Retorna resumo da sessão atual."""
        title, color = self.get_title(self.current_session_score)
        return {
            "score": self.current_session_score,
            "wins": self.current_session_stats["wins"],
            "losses": self.current_session_stats["losses"],
            "battles": self.current_session_stats["battles"],
            "win_rate": (self.current_session_stats["wins"] / max(1, self.current_session_stats["battles"])) * 100,
            "events_used": self.current_session_stats["events_used"],
            "syncretisms": self.current_session_stats["syncretisms"],
            "pantheons_dominated": len(self.current_session_stats["pantheons_dominated"]),
            "pantheon_bonus": self.calculate_pantheon_bonus(),
            "title": title,
            "title_color": color,
            "is_high_score": self.is_high_score(),
        }


# Instância global do sistema de ranking
_ranking_system = None


def get_ranking_system() -> RankingSystem:
    """Retorna a instância singleton do RankingSystem."""
    global _ranking_system
    if _ranking_system is None:
        _ranking_system = RankingSystem()
    return _ranking_system
