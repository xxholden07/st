"""
Componentes visuais das cartas usando Tkinter.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from models.card import Card, Pantheon
from ui.image_loader import get_image_loader


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
        self.image_loader = get_image_loader()
        self.card_image_ref = None  # Para manter referência da imagem
        
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
        """Desenha o verso da carta usando a imagem verso.png."""
        # Tenta carregar a imagem do verso
        back_img = self.image_loader.get_card_back(
            width=self.card_width,
            height=self.card_height
        )
        
        if back_img:
            # Usa a imagem do verso
            self.card_back_ref = back_img  # Mantém referência
            self.create_image(
                self.card_width // 2,
                self.card_height // 2,
                image=back_img,
                anchor="center"
            )
        else:
            # Fallback: desenho geométrico se imagem não existir
            self.create_rectangle(
                0, 0, self.card_width, self.card_height,
                fill="#0a0a1a", outline="#3a2a5a", width=4
            )
            
            cx = self.card_width // 2
            cy = self.card_height // 2
            
            # Círculos concêntricos
            for r in [60, 50, 40, 30]:
                self.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill="", outline="#4a3a6a", width=2
                )
            
            self.create_text(
                cx, cy - 80,
                text="SUPER TRUNFO",
                font=("Georgia", 12, "bold"),
                fill="#6a5a8a"
            )
            self.create_text(
                cx, cy + 80,
                text="MITOLÓGICO",
                font=("Georgia", 12, "bold"),
                fill="#6a5a8a"
            )
    
    def draw_card_front(self):
        """Desenha a frente da carta."""
        colors = self.get_colors()
        
        # Fundo
        self.create_rectangle(
            0, 0, self.card_width, self.card_height,
            fill=colors["bg"], outline=""
        )
        
        # Imagem do personagem - usa imagem sincretizada se ativo
        img_width = self.card_width - 10
        img_height = int(self.card_height * 0.65)
        
        # Verifica se sincretismo está ativo (panteão diferente do original)
        if self.card.current_pantheon != self.card.pantheon:
            # Usa a imagem baseada no nome atual (sincretizado)
            current_name = self.card.current_name
            pantheon_name = self.card.current_pantheon.value if self.card.current_pantheon else None
            card_img = self.image_loader.get_card_image_by_name(
                current_name,
                width=img_width,
                height=img_height,
                pantheon_name=pantheon_name
            )
            # Se não encontrar imagem do sincretismo, usa a original com overlay
            if not card_img:
                card_img = self.image_loader.get_card_image(
                    self.card.card_id,
                    width=img_width,
                    height=img_height
                )
        else:
            # Imagem normal (sem sincretismo)
            card_img = self.image_loader.get_card_image(
                self.card.card_id, 
                width=img_width,
                height=img_height
            )
        
        if card_img:
            self.card_image_ref = card_img
            self.create_image(
                self.card_width // 2, 5,
                image=card_img,
                anchor="n"
            )
        
        # Área de informações na parte inferior
        info_y = int(self.card_height * 0.65)
        self.create_rectangle(
            0, info_y, self.card_width, self.card_height,
            fill=colors["bg"], outline=""
        )
        
        # Borda externa (glow para Super Trunfo ou protegida)
        if self.card.is_super_trump:
            self.draw_glow_border(CardColors.SUPER_TRUMP_GLOW)
        elif self.card.is_protected:
            self.draw_glow_border(CardColors.PROTECTED_GLOW)
        
        # Borda principal
        self.create_rectangle(
            2, 2, self.card_width - 2, self.card_height - 2,
            fill="", outline=colors["border"], width=3
        )
        
        # ID no canto
        self.draw_card_id(colors)
        
        # Nome e atributos
        self.draw_deity_info(colors, info_y)
        
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
        # Fundo do ID com transparência simulada
        self.create_rectangle(
            5, 5, 45, 35,
            fill="#000000", outline=colors["border"], width=2
        )
        
        # Texto do ID
        self.create_text(
            25, 20,
            text=self.card.card_id,
            font=("Georgia", 12, "bold"),
            fill=colors["fg"]
        )
    
    def draw_deity_info(self, colors: dict, start_y: int):
        """Desenha informações da divindade na parte inferior."""
        # Nome da divindade
        name = self.card.current_name
        font_size = 13 if len(name) < 10 else 10
        
        self.create_text(
            self.card_width // 2, start_y + 10,
            text=name.upper(),
            font=("Georgia", font_size, "bold"),
            fill=colors["fg"]
        )
        
        # Panteão
        self.create_text(
            self.card_width // 2, start_y + 28,
            text=self.card.current_pantheon.value,
            font=("Georgia", 8, "italic"),
            fill=colors["accent"]
        )
        
        # Atributos compactos
        attrs = self.card.current_attributes
        attr_y = start_y + 45
        attr_labels = [("CMB", attrs.combat_power), ("SAB", attrs.wisdom),
                       ("JUS", attrs.justice), ("ETR", attrs.eternity)]
        
        for i, (label, value) in enumerate(attr_labels):
            x = 15 + i * (self.card_width - 30) // 4
            
            # Destaque se selecionado
            attr_keys = ["combat_power", "wisdom", "justice", "eternity"]
            if self.highlight_attr == attr_keys[i]:
                self.create_rectangle(
                    x - 18, attr_y - 8, x + 28, attr_y + 18,
                    fill=colors["accent"], outline=""
                )
            
            self.create_text(
                x, attr_y,
                text=label,
                font=("Georgia", 7),
                fill=colors["accent"]
            )
            self.create_text(
                x, attr_y + 12,
                text=str(value),
                font=("Georgia", 9, "bold"),
                fill=self._get_value_color(value)
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
        y = self.card_height - 12
        
        # Super Trunfo
        if self.card.is_super_trump:
            self.create_text(
                self.card_width // 2, y,
                text="SUPER TRUNFO",
                font=("Georgia", 8, "bold"),
                fill="#ffd700"
            )
        
        # Proteção
        elif self.card.is_protected:
            self.create_text(
                self.card_width // 2, y,
                text=f"PROTEGIDA ({self.card.protection_turns})",
                font=("Georgia", 7),
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
