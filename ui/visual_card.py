"""
Componentes visuais das cartas usando Tkinter.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from models.card import Card, Pantheon


class CardColors:
    """Cores temáticas para cada panteão."""
    
    PANTHEON_COLORS = {
        Pantheon.EGYPTIAN: {
            "bg": "#1a1a2e",
            "fg": "#ffd700",
            "accent": "#c9a227",
            "border": "#b8860b",
            "gradient_top": "#2d2d5a",
            "gradient_bottom": "#1a1a2e"
        },
        Pantheon.NORSE: {
            "bg": "#1e3a5f",
            "fg": "#87ceeb",
            "accent": "#4a90d9",
            "border": "#5f9ea0",
            "gradient_top": "#2e5a8f",
            "gradient_bottom": "#1e3a5f"
        },
        Pantheon.GRECO_ROMAN: {
            "bg": "#2d1b4e",
            "fg": "#e6e6fa",
            "accent": "#9370db",
            "border": "#8b668b",
            "gradient_top": "#4a2c7a",
            "gradient_bottom": "#2d1b4e"
        },
        Pantheon.MESOPOTAMIAN: {
            "bg": "#3d2b1f",
            "fg": "#daa520",
            "accent": "#cd853f",
            "border": "#8b4513",
            "gradient_top": "#5a4030",
            "gradient_bottom": "#3d2b1f"
        }
    }
    
    SUPER_TRUMP_GLOW = "#ffd700"
    PROTECTED_GLOW = "#00ff88"
    DESTROYED_OVERLAY = "#ff0000"


# Símbolos/Ilustrações dos deuses usando emojis
DEITY_SYMBOLS = {
    # Grupo 1 - Deuses Supremos
    "Zeus": "⚡👑",
    "Odin": "👁️🦅",
    "Amon": "☀️🐏",
    "Anu": "⭐🌌",
    # Grupo 2 - Deuses da Guerra
    "Thor": "🔨⚡",
    "Marte": "⚔️🛡️",
    "Sekhmet": "🦁🔥",
    "Nergal": "💀⚔️",
    # Grupo 3 - Deuses da Sabedoria
    "Thoth": "📚🐦",
    "Minerva": "🦉📖",
    "Mímir": "👁️💧",
    "Nabu": "📜✍️",
    # Grupo 4 - Deuses da Justiça
    "Maat": "🪶⚖️",
    "Balder": "☀️✨",
    "Ishtar": "⭐💫",
    "Têmis": "⚖️📜",
    # Grupo 5 - Deuses do Submundo
    "Osíris": "☥👑",
    "Hel": "💀❄️",
    "Hades": "💀🔱",
    "Ereshkigal": "🌑💀",
    # Grupo 6 - Deuses do Sol
    "Rá": "☀️🦅",
    "Apolo": "☀️🎵",
    "Freyr": "🌾☀️",
    "Shamash": "☀️⚖️",
    # Grupo 7 - Deuses da Fertilidade
    "Ísis": "🌙✨",
    "Freya": "💕🐱",
    "Deméter": "🌾🌻",
    "Tammuz": "🌿🐑",
    # Grupo 8 - Deuses Primordiais
    "Nun": "🌊🌀",
    "Ymir": "❄️👹",
    "Caos": "🌀⬛",
    "Tiamat": "🐉🌊"
}


class VisualCard(tk.Canvas):
    """Widget visual para representar uma carta."""
    
    # Símbolos dos panteões
    PANTHEON_SYMBOLS = {
        Pantheon.EGYPTIAN: "𓂀",      # Olho de Hórus
        Pantheon.NORSE: "ᚦ",          # Runa Thor
        Pantheon.GRECO_ROMAN: "Ω",    # Omega
        Pantheon.MESOPOTAMIAN: "☽"    # Lua crescente
    }
    
    # Símbolos dos atributos
    ATTR_SYMBOLS = {
        "combat_power": "⚔️",
        "wisdom": "📚",
        "justice": "⚖️",
        "eternity": "∞"
    }
    
    def __init__(self, parent, card: Card, width: int = 200, height: int = 300, 
                 show_back: bool = False, highlight_attr: str = None):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg="#1a1a1a")
        
        self.card = card
        self.card_width = width
        self.card_height = height
        self.show_back = show_back
        self.highlight_attr = highlight_attr
        self.animation_id = None
        
        self.draw_card()
    
    def get_colors(self) -> dict:
        """Retorna as cores do panteão atual."""
        return CardColors.PANTHEON_COLORS.get(
            self.card.current_pantheon, 
            CardColors.PANTHEON_COLORS[Pantheon.GRECO_ROMAN]
        )
    
    def draw_card(self):
        """Desenha a carta completa."""
        self.delete("all")
        
        if self.show_back:
            self.draw_card_back()
        else:
            self.draw_card_front()
    
    def draw_card_back(self):
        """Desenha o verso da carta."""
        # Fundo
        self.create_rectangle(
            5, 5, self.card_width - 5, self.card_height - 5,
            fill="#2a2a4a", outline="#4a4a6a", width=3
        )
        
        # Padrão decorativo
        for i in range(5, self.card_height - 5, 20):
            self.create_line(
                10, i, self.card_width - 10, i,
                fill="#3a3a5a", width=1
            )
        
        # Símbolo central
        self.create_text(
            self.card_width // 2, self.card_height // 2,
            text="🏛️",
            font=("Segoe UI Emoji", 48)
        )
        
        # Texto
        self.create_text(
            self.card_width // 2, self.card_height // 2 + 60,
            text="MITOLOGIA",
            font=("Georgia", 14, "bold"),
            fill="#6a6a8a"
        )
    
    def draw_card_front(self):
        """Desenha a frente da carta."""
        colors = self.get_colors()
        
        # Borda externa (glow para Super Trunfo ou protegida)
        if self.card.is_super_trump:
            self.draw_glow_border(CardColors.SUPER_TRUMP_GLOW)
        elif self.card.is_protected:
            self.draw_glow_border(CardColors.PROTECTED_GLOW)
        
        # Fundo principal com gradiente simulado
        self.create_rectangle(
            8, 8, self.card_width - 8, self.card_height // 3,
            fill=colors["gradient_top"], outline=""
        )
        self.create_rectangle(
            8, self.card_height // 3, self.card_width - 8, self.card_height - 8,
            fill=colors["bg"], outline=""
        )
        
        # Borda principal
        self.create_rectangle(
            5, 5, self.card_width - 5, self.card_height - 5,
            fill="", outline=colors["border"], width=3
        )
        
        # Área do ID e grupo
        self.draw_card_id(colors)
        
        # Nome da divindade
        self.draw_deity_name(colors)
        
        # Símbolo do panteão
        self.draw_pantheon_symbol(colors)
        
        # Linha divisória decorativa
        self.create_line(
            20, 120, self.card_width - 20, 120,
            fill=colors["accent"], width=2
        )
        
        # Atributos
        self.draw_attributes(colors)
        
        # Indicadores especiais
        self.draw_special_indicators(colors)
        
        # Overlay se destruída
        if self.card.is_destroyed:
            self.draw_destroyed_overlay()
    
    def draw_glow_border(self, color: str):
        """Desenha borda brilhante."""
        for i in range(3):
            alpha = 80 - i * 20
            self.create_rectangle(
                2 + i, 2 + i, 
                self.card_width - 2 - i, self.card_height - 2 - i,
                fill="", outline=color, width=2
            )
    
    def draw_card_id(self, colors: dict):
        """Desenha o ID da carta."""
        # Fundo do ID
        self.create_oval(
            10, 10, 50, 50,
            fill=colors["accent"], outline=colors["border"], width=2
        )
        
        # Texto do ID
        self.create_text(
            30, 30,
            text=self.card.card_id,
            font=("Georgia", 14, "bold"),
            fill=colors["bg"]
        )
    
    def draw_deity_name(self, colors: dict):
        """Desenha o nome e ilustração da divindade."""
        # Ilustração do deus (símbolo emoji)
        symbol = DEITY_SYMBOLS.get(self.card.name, "🏛️")
        
        # Círculo decorativo para o símbolo
        cx = self.card_width // 2
        cy = 55
        radius = min(25, self.card_width // 8)
        
        # Fundo circular
        self.create_oval(
            cx - radius - 3, cy - radius - 3,
            cx + radius + 3, cy + radius + 3,
            fill="", outline=colors["accent"], width=2
        )
        self.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill=colors["bg"], outline=colors["border"], width=1
        )
        
        # Símbolo do deus
        font_size = max(12, min(18, self.card_width // 12))
        self.create_text(
            cx, cy,
            text=symbol,
            font=("Segoe UI Emoji", font_size)
        )
        
        # Nome da divindade
        name = self.card.current_name
        font_size = 14 if len(name) < 10 else 11
        if self.card_width < 150:
            font_size = max(8, font_size - 3)
        
        self.create_text(
            self.card_width // 2, 90,
            text=name.upper(),
            font=("Georgia", font_size, "bold"),
            fill=colors["fg"]
        )
        
        # Panteão
        pantheon_size = 9 if self.card_width >= 150 else 7
        self.create_text(
            self.card_width // 2, 107,
            text=self.card.current_pantheon.value,
            font=("Georgia", pantheon_size, "italic"),
            fill=colors["accent"]
        )
    
    def draw_pantheon_symbol(self, colors: dict):
        """Desenha o símbolo do panteão."""
        symbol = self.PANTHEON_SYMBOLS.get(self.card.current_pantheon, "⚡")
        
        self.create_text(
            self.card_width - 35, 30,
            text=symbol,
            font=("Segoe UI Symbol", 24),
            fill=colors["fg"]
        )
    
    def draw_attributes(self, colors: dict):
        """Desenha os atributos da carta."""
        attrs = self.card.current_attributes
        attr_data = [
            ("combat_power", "COMBATE", attrs.combat_power),
            ("wisdom", "SABEDORIA", attrs.wisdom),
            ("justice", "JUSTIÇA", attrs.justice),
            ("eternity", "ETERNIDADE", attrs.eternity)
        ]
        
        y_start = 140
        y_spacing = 38
        
        for i, (key, label, value) in enumerate(attr_data):
            y = y_start + i * y_spacing
            
            # Destacar atributo selecionado
            is_highlighted = self.highlight_attr == key
            
            if is_highlighted:
                self.create_rectangle(
                    15, y - 12, self.card_width - 15, y + 18,
                    fill=colors["accent"], outline=""
                )
            
            # Símbolo do atributo
            symbol = self.ATTR_SYMBOLS.get(key, "•")
            self.create_text(
                30, y,
                text=symbol,
                font=("Segoe UI Emoji", 12)
            )
            
            # Nome do atributo
            text_color = colors["bg"] if is_highlighted else colors["fg"]
            self.create_text(
                55, y,
                text=label,
                font=("Georgia", 9),
                fill=text_color,
                anchor="w"
            )
            
            # Barra de valor
            bar_width = 60
            bar_height = 10
            bar_x = self.card_width - 80
            
            # Fundo da barra
            self.create_rectangle(
                bar_x, y - 5, bar_x + bar_width, y + 5,
                fill="#333333", outline=colors["border"]
            )
            
            # Preenchimento da barra
            fill_width = (value / 100) * bar_width
            bar_color = self._get_value_color(value)
            self.create_rectangle(
                bar_x, y - 5, bar_x + fill_width, y + 5,
                fill=bar_color, outline=""
            )
            
            # Valor numérico
            self.create_text(
                self.card_width - 20, y,
                text=str(value),
                font=("Georgia", 10, "bold"),
                fill=text_color
            )
    
    def _get_value_color(self, value: int) -> str:
        """Retorna cor baseada no valor do atributo."""
        if value >= 90:
            return "#00ff88"
        elif value >= 70:
            return "#88ff00"
        elif value >= 50:
            return "#ffff00"
        elif value >= 30:
            return "#ff8800"
        else:
            return "#ff4444"
    
    def draw_special_indicators(self, colors: dict):
        """Desenha indicadores especiais."""
        y = self.card_height - 25
        
        # Super Trunfo
        if self.card.is_super_trump:
            self.create_text(
                self.card_width // 2, y,
                text="⭐ SUPER TRUNFO ⭐",
                font=("Georgia", 10, "bold"),
                fill="#ffd700"
            )
        
        # Proteção
        elif self.card.is_protected:
            self.create_text(
                self.card_width // 2, y,
                text=f"🛡️ Protegida ({self.card.protection_turns})",
                font=("Georgia", 9),
                fill="#00ff88"
            )
    
    def draw_destroyed_overlay(self):
        """Desenha overlay de carta destruída."""
        # Overlay semi-transparente vermelho (simulado com linhas)
        for i in range(0, self.card_height, 4):
            self.create_line(
                0, i, self.card_width, i,
                fill="#440000", width=2
            )
        
        # X vermelho
        self.create_line(
            20, 20, self.card_width - 20, self.card_height - 20,
            fill="#ff0000", width=5
        )
        self.create_line(
            self.card_width - 20, 20, 20, self.card_height - 20,
            fill="#ff0000", width=5
        )
        
        # Texto
        self.create_text(
            self.card_width // 2, self.card_height // 2,
            text="DEVORADA",
            font=("Georgia", 16, "bold"),
            fill="#ff0000"
        )
    
    def update_card(self, card: Card = None, highlight_attr: str = None):
        """Atualiza a visualização da carta."""
        if card:
            self.card = card
        self.highlight_attr = highlight_attr
        self.draw_card()
    
    def flip_card(self):
        """Vira a carta (mostra/esconde)."""
        self.show_back = not self.show_back
        self.draw_card()


class MiniCard(tk.Canvas):
    """Versão menor da carta para exibição em listas."""
    
    def __init__(self, parent, card: Card, width: int = 120, height: int = 40):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg="#1a1a1a")
        
        self.card = card
        self.card_width = width
        self.card_height = height
        
        self.draw_mini_card()
    
    def draw_mini_card(self):
        """Desenha a mini carta."""
        self.delete("all")
        
        colors = CardColors.PANTHEON_COLORS.get(
            self.card.current_pantheon,
            CardColors.PANTHEON_COLORS[Pantheon.GRECO_ROMAN]
        )
        
        # Fundo
        self.create_rectangle(
            2, 2, self.card_width - 2, self.card_height - 2,
            fill=colors["bg"], outline=colors["border"], width=1
        )
        
        # ID
        self.create_text(
            15, self.card_height // 2,
            text=self.card.card_id,
            font=("Georgia", 9, "bold"),
            fill=colors["accent"]
        )
        
        # Nome
        name = self.card.current_name[:12]
        self.create_text(
            70, self.card_height // 2,
            text=name,
            font=("Georgia", 9),
            fill=colors["fg"]
        )
        
        # Indicadores
        if self.card.is_super_trump:
            self.create_text(
                self.card_width - 12, self.card_height // 2,
                text="⭐",
                font=("Segoe UI Emoji", 10)
            )
        elif self.card.is_protected:
            self.create_text(
                self.card_width - 12, self.card_height // 2,
                text="🛡️",
                font=("Segoe UI Emoji", 10)
            )
