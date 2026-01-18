"""
Interface gráfica principal do jogo usando Tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
import random

from models.card import Card, Pantheon
from models.events import EventType, create_event
from game.game_state import GameState, GamePhase
from game.player import Player
from ui.visual_card import VisualCard, MiniCard, CardColors
from ui.visual_events import (
    RagnarokAnimation, OsirisJudgmentAnimation,
    BifrostAnimation, MysteriesAnimation, BattleAnimation
)
from ui.image_loader import get_image_loader
from data.deity_lore import get_deity_lore, PANTHEON_INTRODUCTIONS


class GameWindow(tk.Tk):
    """Janela principal do jogo."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Super Trunfo Mitológico")
        self.geometry("1200x800")
        self.configure(bg="#0a0a1a")
        self.minsize(1000, 700)
        
        self.game_state: Optional[GameState] = None
        self.selected_card: Optional[Card] = None
        self.selected_attribute: Optional[str] = None
        self.current_animation = None
        
        # Gerenciador de imagens
        self.image_loader = get_image_loader()
        self.arena_images = {}  # Mantém referências das imagens da arena
        
        # Estilo
        self.setup_styles()
        
        # Tela inicial
        self.show_main_menu()
    
    def setup_styles(self):
        """Configura estilos do ttk."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botões
        style.configure(
            'Game.TButton',
            font=('Georgia', 12),
            padding=10,
            background='#4a2c7a',
            foreground='white'
        )
        
        style.configure(
            'Event.TButton',
            font=('Georgia', 10),
            padding=5,
            background='#2a4a6a'
        )
        
        # Labels
        style.configure(
            'Title.TLabel',
            font=('Georgia', 24, 'bold'),
            background='#0a0a1a',
            foreground='#ffd700'
        )
        
        style.configure(
            'Info.TLabel',
            font=('Georgia', 12),
            background='#0a0a1a',
            foreground='#cccccc'
        )
    
    def clear_window(self):
        """Remove todos os widgets da janela."""
        for widget in self.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Exibe o menu principal."""
        self.clear_window()
        
        # Frame central
        center_frame = tk.Frame(self, bg="#0a0a1a")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = tk.Label(
            center_frame,
            text="SUPER TRUNFO MITOLÓGICO",
            font=("Georgia", 36, "bold"),
            bg="#0a0a1a",
            fg="#ffd700"
        )
        title_label.pack(pady=20)
        
        # Subtítulo
        subtitle = tk.Label(
            center_frame,
            text="Deuses de quatro panteões disputam a supremacia cósmica!",
            font=("Georgia", 14, "italic"),
            bg="#0a0a1a",
            fg="#cccccc"
        )
        subtitle.pack(pady=10)
        
        # Botões
        btn_frame = tk.Frame(center_frame, bg="#0a0a1a")
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="Novo Jogo",
            font=("Georgia", 16),
            bg="#4a2c7a",
            fg="white",
            width=20,
            command=self.show_player_setup
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Regras",
            font=("Georgia", 16),
            bg="#2a4a6a",
            fg="white",
            width=20,
            command=self.show_rules
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="🃏 Ver Cartas",
            font=("Georgia", 16),
            bg="#2a4a6a",
            fg="white",
            width=20,
            command=self.show_card_gallery
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Sair",
            font=("Georgia", 16),
            bg="#4a2a2a",
            fg="white",
            width=20,
            command=self.quit
        ).pack(pady=10)
    
    def show_player_setup(self):
        """Tela de configuração dos jogadores."""
        self.clear_window()
        
        center_frame = tk.Frame(self, bg="#0a0a1a")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            center_frame,
            text="⚙️ CONFIGURAÇÃO DO JOGO",
            font=("Georgia", 28, "bold"),
            bg="#0a0a1a",
            fg="#ffd700"
        ).pack(pady=20)
        
        # Jogador 1
        tk.Label(
            center_frame,
            text="Nome do Jogador 1:",
            font=("Georgia", 14),
            bg="#0a0a1a",
            fg="#cccccc"
        ).pack(pady=5)
        
        self.player1_entry = tk.Entry(
            center_frame,
            font=("Georgia", 14),
            width=30,
            bg="#2a2a4a",
            fg="white",
            insertbackground="white"
        )
        self.player1_entry.insert(0, "Jogador 1")
        self.player1_entry.pack(pady=5)
        
        # Jogador 2
        tk.Label(
            center_frame,
            text="Nome do Jogador 2:",
            font=("Georgia", 14),
            bg="#0a0a1a",
            fg="#cccccc"
        ).pack(pady=5)
        
        self.player2_entry = tk.Entry(
            center_frame,
            font=("Georgia", 14),
            width=30,
            bg="#2a2a4a",
            fg="white",
            insertbackground="white"
        )
        self.player2_entry.insert(0, "Jogador 2")
        self.player2_entry.pack(pady=5)
        
        # Botões
        btn_frame = tk.Frame(center_frame, bg="#0a0a1a")
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="Iniciar Jogo",
            font=("Georgia", 14),
            bg="#00aa44",
            fg="white",
            width=15,
            command=self.start_game
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="Voltar",
            font=("Georgia", 14),
            bg="#666666",
            fg="white",
            width=15,
            command=self.show_main_menu
        ).pack(side="left", padx=10)
    
    def start_game(self):
        """Inicia o jogo."""
        player1 = self.player1_entry.get() or "Jogador 1"
        player2 = self.player2_entry.get() or "Jogador 2"
        
        # Pré-carrega as imagens (opcional, melhora performance)
        print("Carregando sprites dos personagens...")
        self.image_loader.preload_arena()
        
        self.game_state = GameState()
        self.game_state.initialize_game([player1, player2])
        
        self.selected_card = None
        self.selected_attribute = None
        
        self.show_game_screen()
    
    def show_game_screen(self):
        """Tela principal do jogo."""
        self.clear_window()
        
        # Container principal
        self.main_container = tk.Frame(self, bg="#0a0a1a")
        self.main_container.pack(fill="both", expand=True)
        
        # Painel lateral - ações (criar primeiro para pack à direita)
        self.create_action_panel()
        
        # Layout principal (à esquerda)
        self.main_frame = tk.Frame(self.main_container, bg="#0a0a1a")
        self.main_frame.pack(side="left", fill="both", expand=True)
        
        # Área superior - informações
        self.create_info_bar()
        
        # Área central - jogo
        self.game_area = tk.Frame(self.main_frame, bg="#0a0a1a")
        self.game_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área do oponente (cartas viradas)
        self.create_opponent_area()
        
        # Área central (batalha e eventos)
        self.create_battle_area()
        
        # Área do jogador (mão)
        self.create_player_area()
        
        self.update_game_display()
    
    def create_info_bar(self):
        """Cria barra de informações."""
        info_bar = tk.Frame(self.main_frame, bg="#1a1a3a", height=60)
        info_bar.pack(fill="x", padx=10, pady=5)
        info_bar.pack_propagate(False)
        
        # Turno
        self.turn_label = tk.Label(
            info_bar,
            text="TURNO 1",
            font=("Georgia", 16, "bold"),
            bg="#1a1a3a",
            fg="#ffd700"
        )
        self.turn_label.pack(side="left", padx=20)
        
        # Jogador atual
        self.current_player_label = tk.Label(
            info_bar,
            text="Vez de: ---",
            font=("Georgia", 14),
            bg="#1a1a3a",
            fg="#88ff88"
        )
        self.current_player_label.pack(side="left", padx=20)
        
        # Placar
        self.score_label = tk.Label(
            info_bar,
            text="Placar: 0 x 0",
            font=("Georgia", 14),
            bg="#1a1a3a",
            fg="#cccccc"
        )
        self.score_label.pack(side="right", padx=20)
    
    def create_opponent_area(self):
        """Cria área do oponente."""
        opponent_frame = tk.Frame(self.game_area, bg="#0a0a1a", height=120)
        opponent_frame.pack(fill="x", pady=5)
        
        self.opponent_label = tk.Label(
            opponent_frame,
            text="Oponente",
            font=("Georgia", 12),
            bg="#0a0a1a",
            fg="#ff8888"
        )
        self.opponent_label.pack()
        
        self.opponent_cards_frame = tk.Frame(opponent_frame, bg="#0a0a1a")
        self.opponent_cards_frame.pack()
    
    def create_battle_area(self):
        """Cria área de batalha central."""
        self.battle_frame = tk.Frame(self.game_area, bg="#1a1a2a", height=350)
        self.battle_frame.pack(fill="x", pady=10)
        self.battle_frame.pack_propagate(False)
        
        # Canvas para animações e background
        self.battle_canvas = tk.Canvas(
            self.battle_frame,
            bg="#1a1a2a",
            highlightthickness=0
        )
        self.battle_canvas.pack(fill="both", expand=True)
        
        # Tenta carregar as camadas da arena
        self.load_arena_background()
        
        # Texto inicial
        self.battle_canvas.create_text(
            400, 150,
            text="Selecione uma carta e um atributo para batalhar!",
            font=("Georgia", 16),
            fill="#666666",
            tags="instruction"
        )
    
    def create_player_area(self):
        """Cria área do jogador."""
        player_frame = tk.Frame(self.game_area, bg="#0a0a1a")
        player_frame.pack(fill="x", pady=5)
        
        self.player_label = tk.Label(
            player_frame,
            text="Sua Mão",
            font=("Georgia", 12),
            bg="#0a0a1a",
            fg="#88ff88"
        )
        self.player_label.pack()
        
        self.player_cards_frame = tk.Frame(player_frame, bg="#0a0a1a")
        self.player_cards_frame.pack()
    
    def create_action_panel(self):
        """Cria painel de ações lateral."""
        self.action_panel = tk.Frame(self.main_container, bg="#1a1a3a", width=220)
        self.action_panel.pack(side="right", fill="y", padx=5, pady=5)
        self.action_panel.pack_propagate(False)
        
        # Título
        tk.Label(
            self.action_panel,
            text="ESCOLHA O ATRIBUTO",
            font=("Georgia", 11, "bold"),
            bg="#1a1a3a",
            fg="#ffd700"
        ).pack(pady=10)
        
        # Frame para os botões de atributos
        attr_frame = tk.Frame(self.action_panel, bg="#1a1a3a")
        attr_frame.pack(fill="x", padx=10)
        
        # Botões de atributos com cores (sem emojis)
        attrs = [
            ("combat_power", "COMBATE", "#ff6644"),
            ("wisdom", "SABEDORIA", "#4488ff"),
            ("justice", "JUSTIÇA", "#ffcc00"),
            ("eternity", "ETERNIDADE", "#aa44ff")
        ]
        
        self.attr_buttons = {}
        self.attr_colors = {}
        for attr_key, attr_name, color in attrs:
            self.attr_colors[attr_key] = color
            btn = tk.Button(
                attr_frame,
                text=attr_name,
                font=("Georgia", 11, "bold"),
                bg="#2a2a4a",
                fg="white",
                activebackground=color,
                activeforeground="white",
                width=18,
                height=2,
                cursor="hand2",
                command=lambda a=attr_key: self.select_attribute(a)
            )
            btn.pack(pady=5, fill="x")
            self.attr_buttons[attr_key] = btn
        
        # Label mostrando seleção atual
        self.selection_label = tk.Label(
            self.action_panel,
            text="Selecione carta e atributo",
            font=("Georgia", 9),
            bg="#1a1a3a",
            fg="#888888",
            wraplength=180
        )
        self.selection_label.pack(pady=10)
        
        # Separador
        tk.Frame(self.action_panel, bg="#3a3a5a", height=2).pack(fill="x", pady=10, padx=10)
        
        # Eventos
        tk.Label(
            self.action_panel,
            text="EVENTOS MITOLÓGICOS",
            font=("Georgia", 10, "bold"),
            bg="#1a1a3a",
            fg="#ffd700"
        ).pack(pady=5)
        
        self.events_label = tk.Label(
            self.action_panel,
            text="Disponíveis: 2",
            font=("Georgia", 9),
            bg="#1a1a3a",
            fg="#888888"
        )
        self.events_label.pack()
        
        event_frame = tk.Frame(self.action_panel, bg="#1a1a3a")
        event_frame.pack(fill="x", padx=10)
        
        events = [
            ("ragnarok", "Ragnarök"),
            ("osiris", "Julgamento"),
            ("bifrost", "Bifrost"),
            ("mysteries", "Mistérios")
        ]
        
        for event_key, event_name in events:
            tk.Button(
                event_frame,
                text=event_name,
                font=("Georgia", 9),
                bg="#2a4a4a",
                fg="white",
                width=16,
                cursor="hand2",
                command=lambda e=event_key: self.use_event(e)
            ).pack(pady=2)
        
        # Separador
        tk.Frame(self.action_panel, bg="#3a3a5a", height=2).pack(fill="x", pady=10, padx=10)
        
        # Botão de Sincretismo
        tk.Label(
            self.action_panel,
            text="SINCRETISMO",
            font=("Georgia", 10, "bold"),
            bg="#1a1a3a",
            fg="#ffd700"
        ).pack(pady=5)
        
        self.syncretism_button = tk.Button(
            self.action_panel,
            text="Transformar Carta",
            font=("Georgia", 10),
            bg="#5a3a7a",
            fg="white",
            width=16,
            cursor="hand2",
            command=self.show_syncretism_menu
        )
        self.syncretism_button.pack(pady=5)
        
        # Separador
        tk.Frame(self.action_panel, bg="#3a3a5a", height=2).pack(fill="x", pady=10, padx=10)
        
        # Botão de Biografia/Aprendizado
        tk.Label(
            self.action_panel,
            text="APRENDIZADO",
            font=("Georgia", 10, "bold"),
            bg="#1a1a3a",
            fg="#88ccff"
        ).pack(pady=5)
        
        self.lore_button = tk.Button(
            self.action_panel,
            text="Biografia do Deus",
            font=("Georgia", 10),
            bg="#2a5a7a",
            fg="white",
            width=16,
            cursor="hand2",
            command=self.show_deity_lore
        )
        self.lore_button.pack(pady=2)
        
        tk.Button(
            self.action_panel,
            text="Sobre os Panteões",
            font=("Georgia", 10),
            bg="#2a4a6a",
            fg="white",
            width=16,
            cursor="hand2",
            command=self.show_pantheon_guide
        ).pack(pady=2)
        
        # Separador
        tk.Frame(self.action_panel, bg="#3a3a5a", height=2).pack(fill="x", pady=10, padx=10)
        
        # Botão de batalha (único)
        self.battle_button = tk.Button(
            self.action_panel,
            text="BATALHAR!",
            font=("Georgia", 14, "bold"),
            bg="#444444",
            fg="#888888",
            width=16,
            height=2,
            state="disabled",
            cursor="arrow",
            command=self.execute_battle
        )
        self.battle_button.pack(pady=10)
        
        # Botão voltar ao menu (único)
        tk.Button(
            self.action_panel,
            text="Menu Principal",
            font=("Georgia", 10),
            bg="#444444",
            fg="white",
            width=16,
            command=self.show_main_menu
        ).pack(side="bottom", pady=10)
    
    def load_arena_background(self):
        """Carrega as camadas do background da arena."""
        try:
            # Obtém dimensões do canvas
            self.update_idletasks()
            canvas_width = self.battle_canvas.winfo_width()
            canvas_height = self.battle_canvas.winfo_height()
            
            # Usa dimensões padrão se ainda não estiverem disponíveis
            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 300
            
            # Carrega as três camadas (fundo, meio, frente)
            bg_img = self.image_loader.get_arena_layer("bg", canvas_width, canvas_height)
            mid_img = self.image_loader.get_arena_layer("mid", canvas_width, canvas_height)
            fg_img = self.image_loader.get_arena_layer("fg", canvas_width, canvas_height)
            
            # Mantém referências
            if bg_img:
                self.arena_images['bg'] = bg_img
                self.battle_canvas.create_image(
                    0, 0,
                    image=bg_img,
                    anchor="nw",
                    tags="arena_bg"
                )
            
            if mid_img:
                self.arena_images['mid'] = mid_img
                self.battle_canvas.create_image(
                    0, 0,
                    image=mid_img,
                    anchor="nw",
                    tags="arena_mid"
                )
            
            if fg_img:
                self.arena_images['fg'] = fg_img
                self.battle_canvas.create_image(
                    0, 0,
                    image=fg_img,
                    anchor="nw",
                    tags="arena_fg"
                )
            
            # Move o texto de instrução para frente
            self.battle_canvas.tag_raise("instruction")
            
        except Exception as e:
            print(f"Erro ao carregar background da arena: {e}")
    
    def update_game_display(self):
        """Atualiza toda a exibição do jogo."""
        if not self.game_state:
            return
        
        player = self.game_state.current_player
        opponent = self.game_state.get_opponent(player.id)
        
        # Atualizar labels
        self.turn_label.config(text=f"TURNO {self.game_state.turn_number}")
        self.current_player_label.config(text=f"Vez de: {player.name}")
        self.score_label.config(text=f"{player.name}: {player.score} | {opponent.name}: {opponent.score}")
        self.player_label.config(text=f"Mão de {player.name}")
        self.opponent_label.config(text=f"Cartas de {opponent.name}: {len(opponent.hand)}")
        self.events_label.config(text=f"Disponíveis: {player.events_available}")
        
        # Atualizar cartas do jogador
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        for card in player.hand:
            card_widget = self.create_clickable_card(card)
            card_widget.pack(side="left", padx=5)
        
        # Atualizar cartas do oponente (viradas - verso com imagem)
        for widget in self.opponent_cards_frame.winfo_children():
            widget.destroy()
        
        # Mantém referência das imagens do verso do oponente
        if not hasattr(self, 'opponent_back_images'):
            self.opponent_back_images = []
        self.opponent_back_images.clear()
        
        for card in opponent.hand:
            # Carrega a imagem do verso em tamanho mini
            back_img = self.image_loader.get_card_back(width=50, height=70)
            
            if back_img:
                # Usa a imagem do verso
                self.opponent_back_images.append(back_img)
                mini_back = tk.Label(
                    self.opponent_cards_frame,
                    image=back_img,
                    bg="#0a0a1a",
                    borderwidth=2,
                    relief="raised"
                )
            else:
                # Fallback: desenho simples se imagem não existir
                mini_back = tk.Canvas(
                    self.opponent_cards_frame,
                    width=50, height=70,
                    bg="#0a0a1a",
                    highlightthickness=2,
                    highlightbackground="#4a3a6a"
                )
                mini_back.create_rectangle(5, 5, 45, 65, fill="#1a1a2e", outline="#3a2a5a", width=2)
                mini_back.create_oval(15, 25, 35, 45, fill="", outline="#4a3a6a", width=2)
                mini_back.create_oval(20, 30, 30, 40, fill="#2a2a4a", outline="#5a4a7a", width=1)
                mini_back.create_text(25, 55, text="ST", font=("Georgia", 7, "bold"), fill="#5a4a7a")
            
            mini_back.pack(side="left", padx=2)
        
        # Verificar fim de jogo
        if self.game_state.current_phase == GamePhase.GAME_OVER:
            self.show_game_over()
    
    def create_clickable_card(self, card: Card) -> tk.Frame:
        """Cria uma carta clicável."""
        frame = tk.Frame(self.player_cards_frame, bg="#0a0a1a")
        
        visual_card = VisualCard(
            frame, card,
            width=140, height=200,
            highlight_attr=self.selected_attribute
        )
        visual_card.pack()
        
        # Indicador de seleção
        if self.selected_card and self.selected_card.card_id == card.card_id:
            visual_card.config(highlightthickness=3, highlightbackground="#00ff00")
        
        # Clique para selecionar
        visual_card.bind("<Button-1>", lambda e, c=card: self.select_card(c))
        
        return frame
    
    def select_card(self, card: Card):
        """Seleciona uma carta."""
        self.selected_card = card
        self.update_game_display()
        self.update_selection_label()
        self.check_battle_ready()
        
        # Mostrar carta grande na área de batalha
        self.show_selected_card()
    
    def show_selected_card(self):
        """Mostra a carta selecionada na área de batalha."""
        self.battle_canvas.delete("all")
        
        if self.selected_card:
            # Carta grande
            visual = VisualCard(
                self.battle_canvas,
                self.selected_card,
                width=200, height=300,
                highlight_attr=self.selected_attribute
            )
            self.battle_canvas.create_window(
                200, 175,
                window=visual
            )
            
            # Símbolo do deus e nome
            self.battle_canvas.create_text(
                550, 100,
                text=self.selected_card.current_name.upper(),
                font=("Georgia", 18, "bold"),
                fill="#ffd700"
            )
            
            self.battle_canvas.create_text(
                550, 125,
                text=self.selected_card.current_pantheon.value,
                font=("Georgia", 10, "italic"),
                fill="#888888"
            )
            
            if self.selected_attribute:
                attr_names = {
                    "combat_power": "Combate",
                    "wisdom": "Sabedoria",
                    "justice": "Justiça",
                    "eternity": "Eternidade"
                }
                self.battle_canvas.create_text(
                    550, 170,
                    text=f"Atributo: {attr_names.get(self.selected_attribute, '')}",
                    font=("Georgia", 14),
                    fill="#ffd700"
                )
                
                value = self.selected_card.current_attributes.get_attribute(self.selected_attribute)
                self.battle_canvas.create_text(
                    550, 210,
                    text=f"Valor: {value}",
                    font=("Georgia", 28, "bold"),
                    fill="#00ff88"
                )
            else:
                self.battle_canvas.create_text(
                    550, 175,
                    text="→ Escolha um atributo\n   no painel à direita",
                    font=("Georgia", 12),
                    fill="#666666",
                    justify="center"
                )
    
    def select_attribute(self, attribute: str):
        """Seleciona um atributo."""
        self.selected_attribute = attribute
        
        # Atualizar botões com cores temáticas
        for key, btn in self.attr_buttons.items():
            if key == attribute:
                btn.config(bg=self.attr_colors.get(key, "#00aa44"), fg="white")
            else:
                btn.config(bg="#2a2a4a", fg="white")
        
        self.update_selection_label()
        self.show_selected_card()
        self.check_battle_ready()
    
    def update_selection_label(self):
        """Atualiza o label de seleção."""
        if self.selected_card and self.selected_attribute:
            attr_names = {
                "combat_power": "Combate",
                "wisdom": "Sabedoria",
                "justice": "Justiça",
                "eternity": "Eternidade"
            }
            value = self.selected_card.current_attributes.get_attribute(self.selected_attribute)
            self.selection_label.config(
                text=f"{self.selected_card.current_name}\n{attr_names[self.selected_attribute]}: {value}",
                fg="#00ff88"
            )
        elif self.selected_card:
            self.selection_label.config(
                text=f"{self.selected_card.current_name}\nEscolha um atributo",
                fg="#ffcc00"
            )
        elif self.selected_attribute:
            attr_names = {
                "combat_power": "Combate",
                "wisdom": "Sabedoria",
                "justice": "Justiça",
                "eternity": "Eternidade"
            }
            self.selection_label.config(
                text=f"Escolha uma carta\n{attr_names[self.selected_attribute]}",
                fg="#ffcc00"
            )
        else:
            self.selection_label.config(
                text="Selecione carta e atributo",
                fg="#888888"
            )
    
    def check_battle_ready(self):
        """Verifica se pode batalhar."""
        if self.selected_card and self.selected_attribute:
            self.battle_button.config(state="normal", bg="#00aa44", fg="white", cursor="hand2")
        else:
            self.battle_button.config(state="disabled", bg="#444444", fg="#888888", cursor="arrow")
    
    def execute_battle(self):
        """Executa a batalha."""
        if not self.selected_card or not self.selected_attribute:
            return
        
        player = self.game_state.current_player
        opponent = self.game_state.get_opponent(player.id)
        
        # Oponente escolhe carta (primeira disponível)
        opponent_card = opponent.hand[0]
        
        # Valores
        player_value = self.selected_card.current_attributes.get_attribute(self.selected_attribute)
        opponent_value = opponent_card.current_attributes.get_attribute(self.selected_attribute)
        
        # Determinar vencedor
        result = self.selected_card.compare(opponent_card, self.selected_attribute)
        
        if result == 1:
            winner = 1
            player.win_card(self.selected_card)
            player.win_card(opponent_card)
            player.remove_card(self.selected_card)
            opponent.remove_card(opponent_card)
        elif result == -1:
            winner = 2
            opponent.win_card(self.selected_card)
            opponent.win_card(opponent_card)
            player.remove_card(self.selected_card)
            opponent.remove_card(opponent_card)
        else:
            winner = 0
        
        # Limpa canvas e anima arena
        self.battle_canvas.delete("all")
        self.animate_arena_battle()
        
        # Animação de batalha com imagens das cartas
        anim = BattleAnimation(
            self.battle_canvas,
            self.selected_card.current_name,
            opponent_card.current_name,
            self.selected_attribute,
            player_value,
            opponent_value,
            winner,
            on_complete=self.after_battle,
            card1_id=self.selected_card.card_id,
            card2_id=opponent_card.card_id
        )
        self.current_animation = anim
        self.battle_canvas.update_idletasks()
        anim.start()
    
    def animate_arena_battle(self):
        """Anima a arena durante a batalha."""
        # Recarrega o background com efeito de shake
        self.load_arena_background()
        
        # Adiciona efeito de flash
        self.battle_canvas.create_rectangle(
            0, 0, self.battle_canvas.winfo_width(), self.battle_canvas.winfo_height(),
            fill="white", stipple="gray50", tags="flash"
        )
        self.after(100, lambda: self.battle_canvas.delete("flash"))
        
        # Partículas de energia
        import random
        for _ in range(20):
            x = random.randint(50, 750)
            y = random.randint(50, 250)
            size = random.randint(2, 6)
            color = random.choice(["#ff8800", "#ffff00", "#ff0000", "#00ffff"])
            particle = self.battle_canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline="", tags="particle"
            )
            # Anima partícula
            self._animate_particle(particle, x, y, random.randint(-50, 50), random.randint(-50, 50))
    
    def _animate_particle(self, particle, x, y, dx, dy, step=0):
        """Anima uma partícula."""
        if step > 15:
            self.battle_canvas.delete(particle)
            return
        
        try:
            self.battle_canvas.move(particle, dx/15, dy/15)
            self.after(30, lambda: self._animate_particle(particle, x, y, dx, dy, step + 1))
        except:
            pass
    
    def after_battle(self):
        """Chamado após a animação de batalha."""
        self.current_animation = None
        self.selected_card = None
        self.selected_attribute = None
        
        # Resetar botões
        for btn in self.attr_buttons.values():
            btn.config(bg="#2a2a4a")
        
        self.game_state.end_turn()
        self.update_game_display()
    
    def show_syncretism_menu(self):
        """Mostra menu de sincretismo para transformar a carta selecionada."""
        if not self.selected_card:
            messagebox.showinfo("Sincretismo", "Selecione uma carta primeiro!")
            return
        
        # Verifica se a carta tem links de sincretismo
        if not self.selected_card.syncretism_links:
            messagebox.showinfo("Sincretismo", f"{self.selected_card.name} não possui transformações disponíveis.")
            return
        
        # Cria janela de sincretismo
        sync_window = tk.Toplevel(self)
        sync_window.title("Sincretismo Divino")
        sync_window.geometry("400x350")
        sync_window.configure(bg="#1a1a2e")
        sync_window.transient(self)
        sync_window.grab_set()
        
        # Título
        tk.Label(
            sync_window,
            text=f"Transformar {self.selected_card.current_name}",
            font=("Georgia", 16, "bold"),
            bg="#1a1a2e",
            fg="#ffd700"
        ).pack(pady=15)
        
        tk.Label(
            sync_window,
            text="Escolha uma forma alternativa:",
            font=("Georgia", 11),
            bg="#1a1a2e",
            fg="#cccccc"
        ).pack(pady=5)
        
        # Frame para opções
        options_frame = tk.Frame(sync_window, bg="#1a1a2e")
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Opção de voltar ao original
        if self.selected_card.current_name != self.selected_card.name:
            tk.Button(
                options_frame,
                text=f"Voltar para {self.selected_card.name} (Original)",
                font=("Georgia", 11),
                bg="#2a4a2a",
                fg="white",
                width=35,
                cursor="hand2",
                command=lambda: self._apply_syncretism(None, sync_window)
            ).pack(pady=5)
        
        # Opções de sincretismo
        for link in self.selected_card.syncretism_links:
            # Formata os bônus
            bonus_text = ", ".join([f"+{v} {k.replace('_', ' ').title()}" for k, v in link.attribute_bonus.items()])
            btn_text = f"{link.deity_name} ({link.pantheon.value})\n{bonus_text}"
            
            tk.Button(
                options_frame,
                text=btn_text,
                font=("Georgia", 10),
                bg="#3a3a5a",
                fg="white",
                width=35,
                height=2,
                cursor="hand2",
                command=lambda l=link: self._apply_syncretism(l, sync_window)
            ).pack(pady=5)
        
        # Botão cancelar
        tk.Button(
            sync_window,
            text="Cancelar",
            font=("Georgia", 10),
            bg="#4a2a2a",
            fg="white",
            width=15,
            command=sync_window.destroy
        ).pack(pady=15)
    
    def _apply_syncretism(self, link, window):
        """Aplica a transformação de sincretismo."""
        if link is None:
            # Volta ao original
            self.selected_card.reset_syncretism()
        else:
            # Aplica o sincretismo usando o panteão do link
            self.selected_card.activate_syncretism(link.pantheon)
        
        window.destroy()
        self.update_game_display()
        self.show_selected_card()
        messagebox.showinfo("Sincretismo", f"Carta transformada em {self.selected_card.current_name}!")
    
    def show_deity_lore(self):
        """Mostra a biografia e informações educativas do deus selecionado."""
        if not self.selected_card:
            messagebox.showinfo("Biografia", "Selecione uma carta primeiro!")
            return
        
        # Busca informações do deus
        lore = get_deity_lore(self.selected_card.current_name)
        
        if not lore:
            # Tenta buscar pelo nome original
            lore = get_deity_lore(self.selected_card.name)
        
        if not lore:
            messagebox.showinfo("Biografia", f"Informações sobre {self.selected_card.current_name} ainda não disponíveis.")
            return
        
        # Cria janela de biografia
        lore_window = tk.Toplevel(self)
        lore_window.title(f"Biografia: {lore.name}")
        lore_window.geometry("650x700")
        lore_window.configure(bg="#0a0a1a")
        lore_window.transient(self)
        lore_window.grab_set()
        
        # Frame principal com scroll
        main_frame = tk.Frame(lore_window, bg="#0a0a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas e scrollbar
        canvas = tk.Canvas(main_frame, bg="#0a0a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a1a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título principal
        tk.Label(
            scrollable_frame,
            text=lore.name.upper(),
            font=("Georgia", 24, "bold"),
            bg="#0a0a1a",
            fg="#ffd700"
        ).pack(pady=(0, 5))
        
        tk.Label(
            scrollable_frame,
            text=lore.title,
            font=("Georgia", 14, "italic"),
            bg="#0a0a1a",
            fg="#aaaaaa"
        ).pack(pady=(0, 15))
        
        # Domínio
        self._create_lore_section(scrollable_frame, "Domínio", lore.domain, "#88ccff")
        
        # Descrição
        self._create_lore_section(scrollable_frame, "Sobre", lore.description, "#ffffff")
        
        # Características
        self._create_lore_section(scrollable_frame, "Características", lore.characteristics, "#cccccc")
        
        # Relações
        self._create_lore_section(scrollable_frame, "Relações Divinas", lore.relations, "#ffcc88")
        
        # Equivalentes
        self._create_lore_section(scrollable_frame, "Equivalentes em Outros Panteões", lore.equivalent, "#88ff88")
        
        # Curiosidade
        curiosity_frame = tk.Frame(scrollable_frame, bg="#1a2a3a", padx=15, pady=10)
        curiosity_frame.pack(fill="x", pady=15)
        
        tk.Label(
            curiosity_frame,
            text="Você Sabia?",
            font=("Georgia", 12, "bold"),
            bg="#1a2a3a",
            fg="#ffdd44"
        ).pack(anchor="w")
        
        tk.Label(
            curiosity_frame,
            text=lore.curiosity,
            font=("Georgia", 11),
            bg="#1a2a3a",
            fg="#dddddd",
            wraplength=580,
            justify="left"
        ).pack(anchor="w", pady=5)
        
        # Pack do canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão fechar
        tk.Button(
            lore_window,
            text="Fechar",
            font=("Georgia", 12),
            bg="#3a3a5a",
            fg="white",
            width=15,
            command=lore_window.destroy
        ).pack(pady=15)
        
        # Bind scroll do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        lore_window.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))
    
    def _create_lore_section(self, parent, title: str, content: str, color: str):
        """Cria uma seção de informação na janela de lore."""
        section = tk.Frame(parent, bg="#0a0a1a")
        section.pack(fill="x", pady=8)
        
        tk.Label(
            section,
            text=title,
            font=("Georgia", 12, "bold"),
            bg="#0a0a1a",
            fg=color
        ).pack(anchor="w")
        
        tk.Label(
            section,
            text=content,
            font=("Georgia", 11),
            bg="#0a0a1a",
            fg="#cccccc",
            wraplength=580,
            justify="left"
        ).pack(anchor="w", pady=3)
    
    def show_pantheon_guide(self):
        """Mostra o guia introdutório dos panteões."""
        guide_window = tk.Toplevel(self)
        guide_window.title("Guia dos Panteões Mitológicos")
        guide_window.geometry("700x600")
        guide_window.configure(bg="#0a0a1a")
        guide_window.transient(self)
        guide_window.grab_set()
        
        # Título
        tk.Label(
            guide_window,
            text="GUIA DOS PANTEÕES MITOLÓGICOS",
            font=("Georgia", 18, "bold"),
            bg="#0a0a1a",
            fg="#ffd700"
        ).pack(pady=15)
        
        tk.Label(
            guide_window,
            text="Selecione um panteão para aprender sobre ele:",
            font=("Georgia", 11),
            bg="#0a0a1a",
            fg="#888888"
        ).pack(pady=5)
        
        # Frame para os botões de panteão
        button_frame = tk.Frame(guide_window, bg="#0a0a1a")
        button_frame.pack(pady=20)
        
        pantheon_colors = {
            "Egípcio": "#c9a227",
            "Nórdico": "#4a90d9",
            "Greco-Romano": "#9370db",
            "Mesopotâmico": "#cd853f"
        }
        
        # Text widget para mostrar o conteúdo
        content_frame = tk.Frame(guide_window, bg="#1a1a3a")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        content_text = tk.Text(
            content_frame,
            font=("Consolas", 10),
            bg="#1a1a3a",
            fg="#ffffff",
            wrap="word",
            padx=15,
            pady=15,
            state="disabled"
        )
        
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=content_text.yview)
        content_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        content_text.pack(side="left", fill="both", expand=True)
        
        def show_pantheon_info(pantheon_name: str):
            """Mostra as informações do panteão selecionado."""
            content_text.config(state="normal")
            content_text.delete(1.0, tk.END)
            
            intro = PANTHEON_INTRODUCTIONS.get(pantheon_name, "Informações não disponíveis.")
            content_text.insert(tk.END, intro)
            
            content_text.config(state="disabled")
        
        # Botões dos panteões
        for pantheon, color in pantheon_colors.items():
            tk.Button(
                button_frame,
                text=pantheon,
                font=("Georgia", 11, "bold"),
                bg=color,
                fg="white",
                width=14,
                cursor="hand2",
                command=lambda p=pantheon: show_pantheon_info(p)
            ).pack(side="left", padx=5)
        
        # Mostra o primeiro por padrão
        show_pantheon_info("Egípcio")
        
        # Botão fechar
        tk.Button(
            guide_window,
            text="Fechar",
            font=("Georgia", 12),
            bg="#3a3a5a",
            fg="white",
            width=15,
            command=guide_window.destroy
        ).pack(pady=15)

    def use_event(self, event_key: str):
        """Usa um evento mitológico."""
        player = self.game_state.current_player
        
        if player.events_available <= 0:
            messagebox.showwarning("Evento", "Você não tem mais eventos disponíveis!")
            return
        
        event_map = {
            "ragnarok": EventType.RAGNAROK,
            "osiris": EventType.OSIRIS_JUDGMENT,
            "bifrost": EventType.BIFROST,
            "mysteries": EventType.MYSTERIES
        }
        
        event_type = event_map.get(event_key)
        if not event_type:
            return
        
        event = create_event(event_type)
        
        # Verificar se pode ativar
        if not event.can_activate(self.game_state, player.id):
            messagebox.showinfo("Evento", "Condições não satisfeitas para ativar este evento.")
            return
        
        self.battle_canvas.delete("all")
        self.battle_canvas.update_idletasks()
        
        # Executar evento com animação
        if event_key == "ragnarok":
            result = event.execute(self.game_state, player.id)
            player.use_event()
            anim = RagnarokAnimation(
                self.battle_canvas,
                on_complete=lambda: self.show_event_result(result)
            )
        
        elif event_key == "osiris":
            result = event.execute(self.game_state, player.id)
            player.use_event()
            passed = "passou" in result.message.lower()
            justice = 50  # Default
            anim = OsirisJudgmentAnimation(
                self.battle_canvas,
                passed=passed,
                justice_value=justice,
                on_complete=lambda: self.show_event_result(result)
            )
        
        elif event_key == "bifrost":
            result = event.execute(self.game_state, player.id)
            player.use_event()
            card_name = result.affected_cards[0] if result.affected_cards else "Desconhecido"
            anim = BifrostAnimation(
                self.battle_canvas,
                card_name=card_name,
                on_complete=lambda: self.show_event_result(result)
            )
        
        elif event_key == "mysteries":
            result = event.execute(self.game_state, player.id)
            player.use_event()
            num_protected = len(result.affected_cards)
            anim = MysteriesAnimation(
                self.battle_canvas,
                num_protected=num_protected,
                on_complete=lambda: self.show_event_result(result)
            )
        
        self.current_animation = anim
        anim.start()
    
    def show_event_result(self, result):
        """Mostra resultado do evento."""
        self.current_animation = None
        messagebox.showinfo("Resultado do Evento", result.message)
        self.update_game_display()
    
    def show_game_over(self):
        """Mostra tela de fim de jogo."""
        winner = self.game_state.get_winner()
        
        self.battle_canvas.delete("all")
        
        self.battle_canvas.create_text(
            400, 100,
            text="🏆 FIM DE JOGO 🏆",
            font=("Georgia", 36, "bold"),
            fill="#ffd700"
        )
        
        self.battle_canvas.create_text(
            400, 180,
            text=f"Vencedor: {winner.name}!",
            font=("Georgia", 28),
            fill="#00ff88"
        )
        
        self.battle_canvas.create_text(
            400, 240,
            text=f"Pontuação: {winner.score}",
            font=("Georgia", 20),
            fill="#ffffff"
        )
        
        # Botão para voltar ao menu
        btn = tk.Button(
            self.battle_canvas,
            text="Voltar ao Menu",
            font=("Georgia", 14),
            bg="#4a2c7a",
            fg="white",
            command=self.show_main_menu
        )
        self.battle_canvas.create_window(400, 320, window=btn)
    
    def show_rules(self):
        """Mostra janela de regras."""
        rules_window = tk.Toplevel(self)
        rules_window.title("📜 Regras do Jogo")
        rules_window.geometry("600x500")
        rules_window.configure(bg="#1a1a2e")
        
        text = tk.Text(
            rules_window,
            font=("Georgia", 11),
            bg="#1a1a2e",
            fg="#cccccc",
            wrap="word",
            padx=20,
            pady=20
        )
        text.pack(fill="both", expand=True)
        
        rules = """
🎮 OBJETIVO
Ganhar todas as cartas dos oponentes ou ter mais pontos quando as cartas acabarem.

⚔️ ATRIBUTOS DAS CARTAS
• Poder de Combate - Força em batalha
• Sabedoria - Conhecimento e estratégia  
• Justiça - Retidão moral (importante no Julgamento de Osíris)
• Eternidade - Imortalidade (gregos = alta, nórdicos = baixa)

🔄 SINCRETISMO
Cartas podem ser transformadas em suas versões equivalentes de outros panteões para ganhar bônus de atributos!

Exemplo: Zeus → Júpiter (+10 Justiça) ou Amon-Rá (+15 Sabedoria)

⚡ EVENTOS MITOLÓGICOS

• Ragnarök - Destrói todas as cartas em jogo e redistribui novas

• Julgamento de Osíris - O coração da carta é pesado contra a Pena da Verdade. Se Justiça < 50, a carta é devorada por Ammit!

• Bifrost - A ponte arco-íris permite invocar uma carta da reserva

• Mistérios de Ísis/Orfeu - Protege suas cartas por 3 rodadas

⭐ SUPER TRUNFO
Zeus é o Super Trunfo e vence qualquer carta!

🏛️ PANTEÕES
• Egípcio - Bônus: +10 Eternidade, +5 Justiça
• Nórdico - Bônus: +10 Combate, -5 Sabedoria
• Greco-Romano - Bônus: +5 Sabedoria, +5 Eternidade
• Mesopotâmico - Bônus: +10 Justiça, +5 Sabedoria
        """
        
        text.insert("1.0", rules)
        text.config(state="disabled")
    
    def show_card_gallery(self):
        """Mostra galeria de todas as cartas."""
        from data.deck_data import create_deck
        
        gallery = tk.Toplevel(self)
        gallery.title("🃏 Galeria de Cartas")
        gallery.geometry("1000x700")
        gallery.configure(bg="#0a0a1a")
        
        # Canvas com scroll
        canvas = tk.Canvas(gallery, bg="#0a0a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(gallery, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a1a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar cartas
        deck = create_deck()
        row = 0
        col = 0
        
        for card in deck:
            frame = tk.Frame(scrollable_frame, bg="#0a0a1a")
            frame.grid(row=row, column=col, padx=10, pady=10)
            
            visual = VisualCard(frame, card, width=160, height=240)
            visual.pack()
            
            col += 1
            if col >= 5:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll com mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))


def run_visual_game():
    """Inicia o jogo visual."""
    app = GameWindow()
    app.mainloop()


if __name__ == "__main__":
    run_visual_game()
