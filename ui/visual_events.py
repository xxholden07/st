"""
Animações visuais para eventos mitológicos.
"""
import tkinter as tk
from tkinter import ttk
import math
import random
from typing import Callable, Optional


class EventAnimation:
    """Classe base para animações de eventos."""
    
    def __init__(self, canvas: tk.Canvas, on_complete: Callable = None):
        self.canvas = canvas
        self.on_complete = on_complete
        self.animation_running = False
        self.animation_id = None
    
    def start(self):
        """Inicia a animação."""
        self.animation_running = True
        self.animate()
    
    def stop(self):
        """Para a animação."""
        self.animation_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
    
    def animate(self):
        """Método a ser sobrescrito."""
        pass
    
    def complete(self):
        """Finaliza a animação."""
        self.animation_running = False
        if self.on_complete:
            self.on_complete()


class RagnarokAnimation(EventAnimation):
    """Animação do Ragnarök - fogo e destruição."""
    
    def __init__(self, canvas: tk.Canvas, on_complete: Callable = None):
        super().__init__(canvas, on_complete)
        self.particles = []
        self.frame = 0
        self.max_frames = 120
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
    
    def start(self):
        """Inicia a animação do Ragnarök."""
        # Criar partículas de fogo
        for _ in range(100):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': self.height + random.randint(0, 100),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-8, -3),
                'size': random.randint(5, 20),
                'color': random.choice(['#ff4400', '#ff6600', '#ff8800', '#ffaa00', '#ffcc00'])
            })
        
        super().start()
    
    def animate(self):
        """Anima o Ragnarök."""
        if not self.animation_running or self.frame >= self.max_frames:
            self.canvas.delete("ragnarok")
            self.complete()
            return
        
        self.canvas.delete("ragnarok")
        
        # Fundo escurecendo
        alpha = min(150, self.frame * 2)
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill=f'#{alpha:02x}0000',
            tags="ragnarok"
        )
        
        # Atualizar e desenhar partículas
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1  # Gravidade leve
            
            # Redesenhar partícula
            if 0 < p['y'] < self.height:
                size = p['size'] * (1 - self.frame / self.max_frames)
                self.canvas.create_oval(
                    p['x'] - size, p['y'] - size,
                    p['x'] + size, p['y'] + size,
                    fill=p['color'], outline="",
                    tags="ragnarok"
                )
        
        # Texto do evento
        if 20 < self.frame < 100:
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text="⚡ RAGNARÖK ⚡",
                font=("Georgia", 48, "bold"),
                fill="#ff4400",
                tags="ragnarok"
            )
            self.canvas.create_text(
                self.width // 2, self.height // 2 + 60,
                text="O Crepúsculo dos Deuses",
                font=("Georgia", 20, "italic"),
                fill="#ffaa00",
                tags="ragnarok"
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(33, self.animate)


class OsirisJudgmentAnimation(EventAnimation):
    """Animação do Julgamento de Osíris - balança e coração."""
    
    def __init__(self, canvas: tk.Canvas, passed: bool, 
                 justice_value: int, on_complete: Callable = None):
        super().__init__(canvas, on_complete)
        self.passed = passed
        self.justice_value = justice_value
        self.frame = 0
        self.max_frames = 150
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
        self.scale_angle = 0
    
    def animate(self):
        """Anima o Julgamento de Osíris."""
        if not self.animation_running or self.frame >= self.max_frames:
            self.canvas.delete("osiris")
            self.complete()
            return
        
        self.canvas.delete("osiris")
        
        cx = self.width // 2
        cy = self.height // 2
        
        # Fundo místico
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#1a1a2e",
            tags="osiris"
        )
        
        # Desenhar balança
        self.draw_scale(cx, cy)
        
        # Texto
        self.canvas.create_text(
            cx, 80,
            text="⚖️ JULGAMENTO DE OSÍRIS ⚖️",
            font=("Georgia", 32, "bold"),
            fill="#ffd700",
            tags="osiris"
        )
        
        # Resultado (após frame 80)
        if self.frame > 80:
            if self.passed:
                result_text = "✨ PASSOU NO JULGAMENTO ✨"
                result_color = "#00ff88"
                sub_text = f"Coração puro (Justiça: {self.justice_value})"
            else:
                result_text = "💀 DEVORADO POR AMMIT 💀"
                result_color = "#ff4444"
                sub_text = f"Coração pesado (Justiça: {self.justice_value})"
            
            self.canvas.create_text(
                cx, self.height - 100,
                text=result_text,
                font=("Georgia", 24, "bold"),
                fill=result_color,
                tags="osiris"
            )
            self.canvas.create_text(
                cx, self.height - 60,
                text=sub_text,
                font=("Georgia", 14),
                fill="#cccccc",
                tags="osiris"
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(33, self.animate)
    
    def draw_scale(self, cx: int, cy: int):
        """Desenha a balança animada."""
        # Calcular ângulo da balança
        target_angle = -15 if self.passed else 15
        
        if self.frame < 60:
            # Balançando
            self.scale_angle = math.sin(self.frame * 0.2) * 20
        else:
            # Estabilizando
            progress = min(1, (self.frame - 60) / 30)
            self.scale_angle = self.scale_angle + (target_angle - self.scale_angle) * progress
        
        angle_rad = math.radians(self.scale_angle)
        
        # Pilar central
        self.canvas.create_rectangle(
            cx - 10, cy - 50, cx + 10, cy + 100,
            fill="#8b4513", outline="#654321",
            tags="osiris"
        )
        
        # Barra da balança
        bar_length = 150
        left_x = cx - bar_length * math.cos(angle_rad)
        left_y = cy - bar_length * math.sin(angle_rad)
        right_x = cx + bar_length * math.cos(angle_rad)
        right_y = cy + bar_length * math.sin(angle_rad)
        
        self.canvas.create_line(
            left_x, left_y, right_x, right_y,
            fill="#ffd700", width=5,
            tags="osiris"
        )
        
        # Prato esquerdo (coração)
        self.canvas.create_oval(
            left_x - 40, left_y + 20, left_x + 40, left_y + 60,
            fill="#8b0000", outline="#ffd700",
            tags="osiris"
        )
        self.canvas.create_text(
            left_x, left_y + 40,
            text="❤️",
            font=("Segoe UI Emoji", 20),
            tags="osiris"
        )
        self.canvas.create_text(
            left_x, left_y + 80,
            text="Coração",
            font=("Georgia", 10),
            fill="#cccccc",
            tags="osiris"
        )
        
        # Prato direito (pena)
        self.canvas.create_oval(
            right_x - 40, right_y + 20, right_x + 40, right_y + 60,
            fill="#2e4a2e", outline="#ffd700",
            tags="osiris"
        )
        self.canvas.create_text(
            right_x, right_y + 40,
            text="🪶",
            font=("Segoe UI Emoji", 20),
            tags="osiris"
        )
        self.canvas.create_text(
            right_x, right_y + 80,
            text="Pena de Maat",
            font=("Georgia", 10),
            fill="#cccccc",
            tags="osiris"
        )


class BifrostAnimation(EventAnimation):
    """Animação da Bifrost - ponte arco-íris."""
    
    def __init__(self, canvas: tk.Canvas, card_name: str, on_complete: Callable = None):
        super().__init__(canvas, on_complete)
        self.card_name = card_name
        self.frame = 0
        self.max_frames = 100
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
        self.rainbow_colors = ['#ff0000', '#ff7f00', '#ffff00', '#00ff00', 
                               '#0000ff', '#4b0082', '#9400d3']
    
    def animate(self):
        """Anima a Bifrost."""
        if not self.animation_running or self.frame >= self.max_frames:
            self.canvas.delete("bifrost")
            self.complete()
            return
        
        self.canvas.delete("bifrost")
        
        # Fundo celestial
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#0a0a2e",
            tags="bifrost"
        )
        
        # Desenhar estrelas
        random.seed(42)  # Seed fixa para estrelas consistentes
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline="",
                tags="bifrost"
            )
        
        # Desenhar ponte arco-íris
        progress = min(1, self.frame / 60)
        self.draw_rainbow_bridge(progress)
        
        # Texto
        self.canvas.create_text(
            self.width // 2, 60,
            text="🌈 BIFROST 🌈",
            font=("Georgia", 36, "bold"),
            fill="#ffffff",
            tags="bifrost"
        )
        
        # Carta invocada (após frame 50)
        if self.frame > 50:
            self.canvas.create_text(
                self.width // 2, self.height - 80,
                text=f"✨ {self.card_name} atravessa a ponte! ✨",
                font=("Georgia", 20),
                fill="#ffd700",
                tags="bifrost"
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(33, self.animate)
    
    def draw_rainbow_bridge(self, progress: float):
        """Desenha a ponte arco-íris."""
        start_x = 50
        end_x = self.width - 50
        current_end_x = start_x + (end_x - start_x) * progress
        
        cy = self.height // 2
        
        for i, color in enumerate(self.rainbow_colors):
            offset = (i - 3) * 8
            
            # Arco da ponte
            points = []
            for x in range(int(start_x), int(current_end_x), 5):
                # Função de arco
                t = (x - start_x) / (end_x - start_x)
                y = cy - math.sin(t * math.pi) * 150 + offset
                points.extend([x, y])
            
            if len(points) >= 4:
                self.canvas.create_line(
                    points,
                    fill=color, width=10,
                    smooth=True,
                    tags="bifrost"
                )


class MysteriesAnimation(EventAnimation):
    """Animação dos Mistérios de Ísis/Orfeu - aura mística."""
    
    def __init__(self, canvas: tk.Canvas, num_protected: int, on_complete: Callable = None):
        super().__init__(canvas, on_complete)
        self.num_protected = num_protected
        self.frame = 0
        self.max_frames = 100
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
        self.particles = []
    
    def start(self):
        """Inicia a animação."""
        # Criar partículas místicas
        for _ in range(60):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(50, 200)
            self.particles.append({
                'angle': angle,
                'radius': radius,
                'speed': random.uniform(0.02, 0.05),
                'size': random.randint(3, 8),
                'color': random.choice(['#00ff88', '#00ffcc', '#88ffcc', '#00ff44'])
            })
        
        super().start()
    
    def animate(self):
        """Anima os Mistérios."""
        if not self.animation_running or self.frame >= self.max_frames:
            self.canvas.delete("mysteries")
            self.complete()
            return
        
        self.canvas.delete("mysteries")
        
        cx = self.width // 2
        cy = self.height // 2
        
        # Fundo místico
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#0a1a1a",
            tags="mysteries"
        )
        
        # Círculo central
        pulse = 1 + 0.1 * math.sin(self.frame * 0.1)
        base_radius = 100 * pulse
        
        for i in range(3):
            radius = base_radius + i * 30
            alpha = 100 - i * 30
            self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill="", outline=f'#00{alpha + 50:02x}{alpha:02x}', width=3,
                tags="mysteries"
            )
        
        # Partículas orbitando
        for p in self.particles:
            p['angle'] += p['speed']
            x = cx + p['radius'] * math.cos(p['angle'])
            y = cy + p['radius'] * math.sin(p['angle']) * 0.6  # Elipse
            
            self.canvas.create_oval(
                x - p['size'], y - p['size'],
                x + p['size'], y + p['size'],
                fill=p['color'], outline="",
                tags="mysteries"
            )
        
        # Símbolo central
        self.canvas.create_text(
            cx, cy,
            text="🔮",
            font=("Segoe UI Emoji", 48),
            tags="mysteries"
        )
        
        # Texto
        self.canvas.create_text(
            cx, 80,
            text="🌙 MISTÉRIOS DE ÍSIS/ORFEU 🌙",
            font=("Georgia", 28, "bold"),
            fill="#00ff88",
            tags="mysteries"
        )
        
        if self.frame > 30:
            self.canvas.create_text(
                cx, self.height - 80,
                text=f"✨ {self.num_protected} carta(s) protegida(s) por 3 rodadas ✨",
                font=("Georgia", 18),
                fill="#88ffcc",
                tags="mysteries"
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(33, self.animate)


class BattleAnimation(EventAnimation):
    """Animação de batalha entre cartas."""
    
    def __init__(self, canvas: tk.Canvas, card1_name: str, card2_name: str,
                 attribute: str, value1: int, value2: int, 
                 winner: int, on_complete: Callable = None):
        super().__init__(canvas, on_complete)
        self.card1_name = card1_name
        self.card2_name = card2_name
        self.attribute = attribute
        self.value1 = value1
        self.value2 = value2
        self.winner = winner  # 1, 2, or 0 for tie
        self.frame = 0
        self.max_frames = 120
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
    
    def animate(self):
        """Anima a batalha."""
        if not self.animation_running or self.frame >= self.max_frames:
            self.canvas.delete("battle")
            self.complete()
            return
        
        self.canvas.delete("battle")
        
        cx = self.width // 2
        cy = self.height // 2
        
        # Fundo
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#1a1a2e",
            tags="battle"
        )
        
        # Cartas se aproximando
        progress = min(1, self.frame / 40)
        left_x = 100 + (cx - 200 - 100) * progress
        right_x = self.width - 100 - (self.width - 100 - cx - 200) * progress
        
        # Carta 1
        self.draw_battle_card(left_x, cy, self.card1_name, self.value1, 
                             self.winner == 1 and self.frame > 60)
        
        # Carta 2
        self.draw_battle_card(right_x, cy, self.card2_name, self.value2,
                             self.winner == 2 and self.frame > 60)
        
        # VS
        if self.frame < 60:
            self.canvas.create_text(
                cx, cy,
                text="⚔️",
                font=("Segoe UI Emoji", 48),
                tags="battle"
            )
        
        # Atributo
        attr_names = {
            "combat_power": "⚔️ COMBATE",
            "wisdom": "📚 SABEDORIA",
            "justice": "⚖️ JUSTIÇA",
            "eternity": "∞ ETERNIDADE"
        }
        self.canvas.create_text(
            cx, 60,
            text=attr_names.get(self.attribute, self.attribute),
            font=("Georgia", 24, "bold"),
            fill="#ffd700",
            tags="battle"
        )
        
        # Resultado
        if self.frame > 60:
            if self.winner == 1:
                result = f"🏆 {self.card1_name} VENCE! 🏆"
                color = "#00ff88"
            elif self.winner == 2:
                result = f"🏆 {self.card2_name} VENCE! 🏆"
                color = "#00ff88"
            else:
                result = "🤝 EMPATE! 🤝"
                color = "#ffff00"
            
            self.canvas.create_text(
                cx, self.height - 80,
                text=result,
                font=("Georgia", 28, "bold"),
                fill=color,
                tags="battle"
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(33, self.animate)
    
    def draw_battle_card(self, x: int, y: int, name: str, value: int, is_winner: bool):
        """Desenha uma carta simplificada na batalha."""
        w, h = 150, 200
        
        # Borda de vencedor
        if is_winner:
            for i in range(3):
                self.canvas.create_rectangle(
                    x - w//2 - 5 - i, y - h//2 - 5 - i,
                    x + w//2 + 5 + i, y + h//2 + 5 + i,
                    fill="", outline="#ffd700", width=2,
                    tags="battle"
                )
        
        # Carta
        self.canvas.create_rectangle(
            x - w//2, y - h//2, x + w//2, y + h//2,
            fill="#2d1b4e", outline="#9370db", width=2,
            tags="battle"
        )
        
        # Nome
        self.canvas.create_text(
            x, y - 40,
            text=name[:15],
            font=("Georgia", 14, "bold"),
            fill="#e6e6fa",
            tags="battle"
        )
        
        # Valor
        self.canvas.create_text(
            x, y + 20,
            text=str(value),
            font=("Georgia", 48, "bold"),
            fill="#ffd700",
            tags="battle"
        )
