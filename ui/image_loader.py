"""
Sistema de carregamento e gerenciamento de sprites.
"""
import os
from pathlib import Path
from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk
from typing import Optional, Dict, Tuple


class ImageLoader:
    """Gerenciador de carregamento e cache de imagens."""
    
    # Mapeamento de nomes de deuses sincretizados para card_ids equivalentes
    SYNCRETISM_IMAGE_MAP = {
        # === Sincretismos (deuses transformados) ===
        # Zeus sincretismos
        "Amon-Rá": "1C",  # Usa imagem de Amon
        "Júpiter": "1A",  # Usa mesma imagem (Zeus)
        "Enlil": "1D",    # Usa imagem de Anu (similar Mesopotâmico)
        
        # Odin sincretismos
        "Mercúrio": "6B",  # Usa Apolo (mensageiro dos deuses)
        
        # Amon sincretismos
        "Urano": "8C",     # Usa Caos (primordial)
        
        # Thor sincretismos
        "Hércules": "2B",  # Usa Marte (guerreiro)
        "Set": "2C",       # Usa Sekhmet (guerra egípcia)
        
        # Marte sincretismos
        "Ares": "2A",      # Usa Thor (guerreiro)
        "Montu": "2C",     # Usa Sekhmet (guerra egípcia)
        
        # Sekhmet sincretismos
        "Belona": "2B",    # Usa Marte (deusa da guerra)
        
        # Nergal sincretismos
        "Plutão": "5C",    # Usa Hades (submundo)
        
        # Thoth sincretismos
        "Hermes": "6B",    # Usa Apolo (mensageiro)
        
        # Minerva sincretismos
        "Atena": "3B",     # Usa mesma imagem
        "Neith": "4A",     # Usa Maat (egípcia)
        
        # Maat sincretismos
        "Diké": "4D",      # Usa Têmis (justiça)
        "Dike": "4D",
        
        # Balder sincretismos
        "Helios": "6A",    # Usa Rá (sol)
        "Hélio": "6A",
        
        # Ishtar sincretismos
        "Afrodite": "7B",  # Usa Freya (amor)
        
        # Têmis sincretismos
        "Iustitia": "4A",  # Usa Maat (justiça)
        
        # Osíris sincretismos
        "Dis Pater": "5C", # Usa Hades
        
        # Hel sincretismos
        "Proserpina": "5A", # Usa Osíris
        "Prosérpina": "5A",
        
        # Hades sincretismos
        "Mot": "5D",       # Usa Ereshkigal
        
        # Rá sincretismos
        "Sol Invictus": "6B", # Usa Apolo
        
        # Apolo sincretismos
        "Khepri": "6A",    # Usa Rá
        
        # Freyr sincretismos
        "Saturno": "8B",   # Usa Ymir (primordial nórdico)
        
        # Shamash sincretismos
        "Hyperion": "6A",  # Usa Rá
        "Hipérion": "6A",
        
        # Ísis sincretismos
        "Inanna": "4C",    # Usa Ishtar
        
        # Freya sincretismos
        "Hathor": "7A",    # Usa Ísis
        
        # Deméter sincretismos
        "Nisaba": "7D",    # Usa Tammuz
        
        # Tammuz sincretismos
        "Adônis": "7C",    # Usa Deméter
        "Adonis": "7C",
        
        # Nun sincretismos
        "Nereu": "8D",     # Usa Tiamat
        
        # Ymir sincretismos
        "Kur": "8D",       # Usa Tiamat
        
        # Caos sincretismos
        "Apsu": "8A",      # Usa Nun
        
        # Tiamat sincretismos
        "Équidna": "8C",   # Usa Caos
        "Equidna": "8C",
        
        # === Deuses originais (carta base) ===
        "Zeus": "1A",
        "Odin": "1B", 
        "Amon": "1C",
        "Anu": "1D",
        "Thor": "2A",
        "Marte": "2B",
        "Sekhmet": "2C",
        "Nergal": "2D",
        "Thoth": "3A",
        "Minerva": "3B",
        "Mímir": "3C",
        "Mimir": "3C",
        "Nabu": "3D",
        "Maat": "4A",
        "Balder": "4B",
        "Ishtar": "4C",
        "Têmis": "4D",
        "Themis": "4D",
        "Osíris": "5A",
        "Osiris": "5A",
        "Hel": "5B",
        "Hades": "5C",
        "Ereshkigal": "5D",
        "Rá": "6A",
        "Ra": "6A",
        "Apolo": "6B",
        "Freyr": "6C",
        "Shamash": "6D",
        "Ísis": "7A",
        "Isis": "7A",
        "Freya": "7B",
        "Deméter": "7C",
        "Demeter": "7C",
        "Tammuz": "7D",
        "Nun": "8A",
        "Ymir": "8B",
        "Caos": "8C",
        "Chaos": "8C",
        "Tiamat": "8D",
    }
    
    # Cores de overlay por panteão para sincretismo
    PANTHEON_OVERLAY = {
        "Egípcio": (255, 215, 0, 40),      # Dourado
        "Nórdico": (135, 206, 235, 40),    # Azul gelo
        "Greco-Romano": (230, 230, 250, 40), # Lavanda
        "Mesopotâmico": (218, 165, 32, 40),  # Marrom dourado
    }
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "personagens"
        self.card_cache: Dict[str, ImageTk.PhotoImage] = {}
        self.arena_cache: Dict[str, ImageTk.PhotoImage] = {}
        
    def get_card_image(self, card_id: str, width: int = 180, height: int = 220) -> Optional[ImageTk.PhotoImage]:
        """
        Carrega a imagem de uma carta pelo ID.
        
        Args:
            card_id: ID da carta (ex: "1A", "2B")
            width: Largura desejada
            height: Altura desejada
            
        Returns:
            ImageTk.PhotoImage ou None se não encontrar
        """
        cache_key = f"{card_id}_{width}x{height}"
        
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]
        
        # Determina o grupo e busca a imagem
        group = card_id[0]
        image_path = self.base_path / f"st_card_arts_group{group}" / f"{card_id}_*.png"
        
        # Procura o arquivo
        group_dir = self.base_path / f"st_card_arts_group{group}"
        if not group_dir.exists():
            return None
            
        for file in group_dir.iterdir():
            if file.name.startswith(card_id):
                try:
                    # Carrega e redimensiona a imagem
                    img = Image.open(file)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.card_cache[cache_key] = photo
                    return photo
                except Exception as e:
                    print(f"Erro ao carregar imagem {file}: {e}")
                    return None
        
        return None
    
    def get_card_image_by_name(self, deity_name: str, width: int = 180, height: int = 220, 
                                pantheon_name: str = None) -> Optional[ImageTk.PhotoImage]:
        """
        Carrega a imagem de uma carta pelo nome do deus (para sincretismo).
        
        Args:
            deity_name: Nome da divindade (ex: "Zeus", "Amon-Rá")
            width: Largura desejada
            height: Altura desejada
            pantheon_name: Nome do panteão para aplicar overlay de cor
            
        Returns:
            ImageTk.PhotoImage ou None se não encontrar
        """
        # Busca o card_id correspondente ao nome
        card_id = self.SYNCRETISM_IMAGE_MAP.get(deity_name)
        
        if not card_id:
            # Tenta buscar ignorando acentos
            for name, cid in self.SYNCRETISM_IMAGE_MAP.items():
                if self._normalize_name(name) == self._normalize_name(deity_name):
                    card_id = cid
                    break
        
        if not card_id:
            return None
        
        # Chave de cache inclui panteão para diferenciar versões sincretizadas
        cache_key = f"sync_{deity_name}_{pantheon_name}_{width}x{height}"
        
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]
        
        # Carrega a imagem base
        group = card_id[0]
        group_dir = self.base_path / f"st_card_arts_group{group}"
        
        if not group_dir.exists():
            return None
            
        for file in group_dir.iterdir():
            if file.name.startswith(card_id):
                try:
                    img = Image.open(file)
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    # Aplica overlay de cor do panteão se especificado
                    if pantheon_name and pantheon_name in self.PANTHEON_OVERLAY:
                        img = self._apply_pantheon_overlay(img, pantheon_name)
                    
                    photo = ImageTk.PhotoImage(img)
                    self.card_cache[cache_key] = photo
                    return photo
                except Exception as e:
                    print(f"Erro ao carregar imagem {file}: {e}")
                    return None
        
        return None
    
    def _normalize_name(self, name: str) -> str:
        """Remove acentos e normaliza o nome para comparação."""
        replacements = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i',
            'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u',
            'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A',
            'É': 'E', 'È': 'E', 'Ê': 'E',
            'Í': 'I', 'Ì': 'I', 'Î': 'I',
            'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U',
        }
        result = name.lower()
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result
    
    def _apply_pantheon_overlay(self, img: Image.Image, pantheon_name: str) -> Image.Image:
        """Aplica um overlay de cor baseado no panteão."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        overlay_color = self.PANTHEON_OVERLAY.get(pantheon_name, (255, 255, 255, 30))
        
        # Cria uma camada de overlay
        overlay = Image.new('RGBA', img.size, overlay_color)
        
        # Combina com a imagem original
        result = Image.alpha_composite(img, overlay)
        
        # Aumenta levemente a saturação para destacar
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(1.15)
        
        return result
    
    def get_card_back(self, width: int = 200, height: int = 300) -> Optional[ImageTk.PhotoImage]:
        """
        Carrega a imagem do verso da carta.
        
        Args:
            width: Largura desejada
            height: Altura desejada
            
        Returns:
            ImageTk.PhotoImage ou None se não encontrar
        """
        cache_key = f"card_back_{width}x{height}"
        
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]
        
        image_path = self.base_path / "verso.png"
        
        if not image_path.exists():
            return None
        
        try:
            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.card_cache[cache_key] = photo
            return photo
        except Exception as e:
            print(f"Erro ao carregar verso da carta {image_path}: {e}")
            return None
    
    def get_arena_layer(self, layer_name: str, width: int = 1200, height: int = 300) -> Optional[ImageTk.PhotoImage]:
        """
        Carrega uma camada da arena.
        
        Args:
            layer_name: Nome da camada ("bg", "mid", "fg")
            width: Largura desejada
            height: Altura desejada
            
        Returns:
            ImageTk.PhotoImage ou None se não encontrar
        """
        cache_key = f"{layer_name}_{width}x{height}"
        
        if cache_key in self.arena_cache:
            return self.arena_cache[cache_key]
        
        image_path = self.base_path / "arena_layers" / f"layer_{layer_name}.png"
        
        if not image_path.exists():
            return None
        
        try:
            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.arena_cache[cache_key] = photo
            return photo
        except Exception as e:
            print(f"Erro ao carregar camada da arena {image_path}: {e}")
            return None
    
    def preload_all_cards(self):
        """Pré-carrega todas as imagens das cartas."""
        for group in range(1, 9):
            group_dir = self.base_path / f"st_card_arts_group{group}"
            if group_dir.exists():
                for file in group_dir.iterdir():
                    if file.suffix == ".png":
                        card_id = file.stem.split("_")[0]
                        self.get_card_image(card_id)
    
    def preload_arena(self):
        """Pré-carrega todas as camadas da arena."""
        for layer in ["bg", "mid", "fg"]:
            self.get_arena_layer(layer)
    
    def clear_cache(self):
        """Limpa o cache de imagens."""
        self.card_cache.clear()
        self.arena_cache.clear()


# Instância global do carregador
_image_loader = None


def get_image_loader() -> ImageLoader:
    """Retorna a instância singleton do ImageLoader."""
    global _image_loader
    if _image_loader is None:
        _image_loader = ImageLoader()
    return _image_loader
