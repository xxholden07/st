"""
Interface de Console para o jogo de cartas mitológicas.
"""
import os
import sys
from typing import Optional

from game.game_state import GameState, GamePhase
from game.player import Player
from models.card import Card, Pantheon
from models.events import (
    EventType, create_event, 
    RagnarokEvent, OsirisJudgmentEvent, BifrostEvent, MysteriesEvent
)


class ConsoleUI:
    """Interface de usuário via console."""
    
    ATTRIBUTE_NAMES = {
        "combat_power": "⚔️  Poder de Combate",
        "wisdom": "📚 Sabedoria",
        "justice": "⚖️  Justiça",
        "eternity": "♾️  Eternidade"
    }
    
    PANTHEON_SYMBOLS = {
        Pantheon.EGYPTIAN: "🏛️ ",
        Pantheon.NORSE: "⚡",
        Pantheon.GRECO_ROMAN: "🏛️ ",
        Pantheon.MESOPOTAMIAN: "🌙"
    }
    
    def __init__(self):
        self.game_state: Optional[GameState] = None
    
    def clear_screen(self):
        """Limpa a tela do console."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, text: str):
        """Imprime um cabeçalho formatado."""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_card(self, card: Card, detailed: bool = True):
        """Imprime uma carta formatada."""
        symbol = self.PANTHEON_SYMBOLS.get(card.current_pantheon, "")
        attrs = card.current_attributes
        
        print(f"\n┌{'─' * 40}┐")
        print(f"│ [{card.card_id}] {card.current_name:<30} │")
        print(f"│ {symbol} {card.current_pantheon.value:<33} │")
        
        if card.is_super_trump:
            print(f"│ ⭐ SUPER TRUNFO ⭐{'':>20} │")
        
        if detailed:
            print(f"├{'─' * 40}┤")
            print(f"│ ⚔️  Combate:    {attrs.combat_power:>3}{'':>20} │")
            print(f"│ 📚 Sabedoria:  {attrs.wisdom:>3}{'':>20} │")
            print(f"│ ⚖️  Justiça:    {attrs.justice:>3}{'':>20} │")
            print(f"│ ♾️  Eternidade: {attrs.eternity:>3}{'':>20} │")
        
        if card.is_protected:
            print(f"│ 🛡️  Protegida ({card.protection_turns} turnos){'':>15} │")
        
        print(f"└{'─' * 40}┘")
    
    def print_hand(self, player: Player):
        """Mostra a mão do jogador."""
        self.print_header(f"Mão de {player.name}")
        
        if not player.hand:
            print("  [Mão vazia]")
            return
        
        for i, card in enumerate(player.hand, 1):
            symbol = self.PANTHEON_SYMBOLS.get(card.current_pantheon, "")
            trump = "⭐" if card.is_super_trump else "  "
            protected = "🛡️ " if card.is_protected else "  "
            attrs = card.current_attributes
            
            print(f"  {i}. {trump}{protected}[{card.card_id}] {card.current_name} "
                  f"({symbol}{card.current_pantheon.value})")
            print(f"      C:{attrs.combat_power} S:{attrs.wisdom} "
                  f"J:{attrs.justice} E:{attrs.eternity}")
    
    def get_player_input(self, prompt: str, valid_options: list = None) -> str:
        """Obtém entrada do jogador com validação."""
        while True:
            try:
                choice = input(f"\n{prompt}: ").strip()
                
                if valid_options and choice not in valid_options:
                    print(f"Opção inválida. Escolha entre: {', '.join(valid_options)}")
                    continue
                
                return choice
            except KeyboardInterrupt:
                print("\n\nJogo encerrado pelo usuário.")
                sys.exit(0)
    
    def show_main_menu(self) -> str:
        """Exibe o menu principal."""
        self.clear_screen()
        self.print_header("🏛️  SUPER TRUNFO MITOLÓGICO 🏛️ ")
        print("""
    Bem-vindo ao mundo dos deuses!
    
    1. Novo Jogo (2 Jogadores)
    2. Ver Regras
    3. Ver Panteões
    4. Sair
        """)
        return self.get_player_input("Escolha uma opção", ["1", "2", "3", "4"])
    
    def show_rules(self):
        """Exibe as regras do jogo."""
        self.clear_screen()
        self.print_header("📜 REGRAS DO JOGO")
        print("""
    OBJETIVO:
    Ganhar todas as cartas dos oponentes ou ter mais pontos
    quando as cartas acabarem.
    
    ATRIBUTOS DAS CARTAS:
    • Poder de Combate - Força em batalha
    • Sabedoria - Conhecimento e estratégia
    • Justiça - Retidão moral (importante no Julgamento de Osíris)
    • Eternidade - Imortalidade (gregos = alta, nórdicos = baixa)
    
    SINCRETISMO:
    Cartas podem ser transformadas em suas versões equivalentes
    de outros panteões para ganhar bônus de atributos!
    
    EVENTOS MITOLÓGICOS:
    • Ragnarök - Destrói todas as cartas em jogo
    • Julgamento de Osíris - Cartas com baixa Justiça são devoradas
    • Bifrost - Invoca uma carta da reserva
    • Mistérios de Ísis/Orfeu - Protege cartas por 3 turnos
    
    SUPER TRUNFO:
    Zeus é o Super Trunfo e vence qualquer carta!
        """)
        input("\nPressione ENTER para voltar...")
    
    def show_pantheons(self):
        """Exibe informações sobre os panteões."""
        self.clear_screen()
        self.print_header("🌍 OS PANTEÕES")
        print("""
    🏛️  GRECO-ROMANO
    Os deuses do Olimpo, imortais e eternos.
    Bônus: +5 Sabedoria, +5 Eternidade
    
    🏛️  EGÍPCIO  
    Os misteriosos deuses do Nilo.
    Bônus: +10 Eternidade, +5 Justiça
    
    ⚡ NÓRDICO
    Os guerreiros de Asgard, mortais no Ragnarök.
    Bônus: +10 Combate, -5 Sabedoria
    
    🌙 MESOPOTÂMICO
    Os antigos deuses da Suméria e Babilônia.
    Bônus: +10 Justiça, +5 Sabedoria
        """)
        input("\nPressione ENTER para voltar...")
    
    def setup_game(self) -> GameState:
        """Configura um novo jogo."""
        self.clear_screen()
        self.print_header("⚙️  CONFIGURAÇÃO DO JOGO")
        
        print("\nDigite os nomes dos jogadores:")
        player1 = input("Jogador 1: ").strip() or "Jogador 1"
        player2 = input("Jogador 2: ").strip() or "Jogador 2"
        
        self.game_state = GameState()
        self.game_state.initialize_game([player1, player2])
        
        print(f"\n✨ Jogo iniciado!")
        print(f"   {player1} vs {player2}")
        print(f"   Cartas distribuídas: {len(self.game_state.players[0].hand)} cada")
        
        input("\nPressione ENTER para começar...")
        return self.game_state
    
    def play_turn(self):
        """Executa um turno do jogo."""
        self.clear_screen()
        
        player = self.game_state.current_player
        opponent = self.game_state.get_opponent(player.id)
        
        self.print_header(f"🎮 TURNO {self.game_state.turn_number} - {player.name}")
        print(f"\nPontuação: {player.name}: {player.score} | {opponent.name}: {opponent.score}")
        print(f"Cartas: {player.name}: {len(player.hand)} | {opponent.name}: {len(opponent.hand)}")
        
        # Mostrar mão do jogador
        self.print_hand(player)
        
        # Menu de ações
        print("\n--- AÇÕES ---")
        print("1. Escolher carta e atributo para batalha")
        print("2. Ativar Sincretismo em uma carta")
        print("3. Usar Evento Mitológico")
        print("4. Ver carta em detalhes")
        
        action = self.get_player_input("Escolha uma ação", ["1", "2", "3", "4"])
        
        if action == "1":
            self.battle_phase(player, opponent)
        elif action == "2":
            self.syncretism_phase(player)
        elif action == "3":
            self.event_phase(player)
        elif action == "4":
            self.view_card_detail(player)
    
    def battle_phase(self, player: Player, opponent: Player):
        """Fase de batalha."""
        # Escolher carta
        print("\nEscolha uma carta para jogar (número):")
        for i, card in enumerate(player.hand, 1):
            print(f"  {i}. {card}")
        
        card_choice = int(self.get_player_input(
            "Carta", 
            [str(i) for i in range(1, len(player.hand) + 1)]
        )) - 1
        
        player_card = player.hand[card_choice]
        
        # Escolher atributo
        print("\nEscolha o atributo para comparar:")
        attrs = ["combat_power", "wisdom", "justice", "eternity"]
        for i, attr in enumerate(attrs, 1):
            value = player_card.current_attributes.get_attribute(attr)
            print(f"  {i}. {self.ATTRIBUTE_NAMES[attr]}: {value}")
        
        attr_choice = int(self.get_player_input(
            "Atributo",
            ["1", "2", "3", "4"]
        )) - 1
        
        chosen_attr = attrs[attr_choice]
        
        # Oponente escolhe carta automaticamente (ou pode ser jogador 2)
        # Para simplicidade, oponente escolhe a primeira carta
        opponent_card = opponent.hand[0]
        
        # Resolver batalha
        print(f"\n⚔️  BATALHA: {self.ATTRIBUTE_NAMES[chosen_attr]} ⚔️ ")
        print(f"\n{player.name}:")
        self.print_card(player_card)
        
        print(f"\n{opponent.name}:")
        self.print_card(opponent_card)
        
        result = player_card.compare(opponent_card, chosen_attr)
        
        player_value = player_card.current_attributes.get_attribute(chosen_attr)
        opponent_value = opponent_card.current_attributes.get_attribute(chosen_attr)
        
        print(f"\n{player.name}: {player_value} vs {opponent.name}: {opponent_value}")
        
        if result == 1:
            print(f"\n🏆 {player.name} VENCE!")
            player.win_card(player_card)
            player.win_card(opponent_card)
            player.remove_card(player_card)
            opponent.remove_card(opponent_card)
        elif result == -1:
            print(f"\n🏆 {opponent.name} VENCE!")
            opponent.win_card(player_card)
            opponent.win_card(opponent_card)
            player.remove_card(player_card)
            opponent.remove_card(opponent_card)
        else:
            print("\n🤝 EMPATE! Cartas retornam às mãos.")
        
        input("\nPressione ENTER para continuar...")
        self.game_state.end_turn()
    
    def syncretism_phase(self, player: Player):
        """Fase de sincretismo - transformar carta."""
        print("\nEscolha uma carta para transformar:")
        for i, card in enumerate(player.hand, 1):
            links = [f"{l.deity_name} ({l.pantheon.value})" 
                    for l in card.syncretism_links]
            links_str = ", ".join(links) if links else "Sem sincretismo"
            print(f"  {i}. {card} -> {links_str}")
        
        card_idx = int(self.get_player_input(
            "Carta",
            [str(i) for i in range(1, len(player.hand) + 1)]
        )) - 1
        
        card = player.hand[card_idx]
        
        if not card.syncretism_links:
            print("Esta carta não possui sincretismos disponíveis.")
            input("\nPressione ENTER...")
            return
        
        print(f"\nTransformar {card.current_name} em:")
        print(f"  0. {card.name} (Original)")
        for i, link in enumerate(card.syncretism_links, 1):
            bonus_str = ", ".join([f"{k}: +{v}" for k, v in link.attribute_bonus.items()])
            print(f"  {i}. {link.deity_name} ({link.pantheon.value}) - Bônus: {bonus_str}")
        
        choice = int(self.get_player_input(
            "Escolha",
            [str(i) for i in range(len(card.syncretism_links) + 1)]
        ))
        
        if choice == 0:
            card.reset_syncretism()
            print(f"\n✨ {card.name} retorna à sua forma original!")
        else:
            link = card.syncretism_links[choice - 1]
            card.activate_syncretism(link.pantheon)
            print(f"\n✨ {card.name} se transforma em {link.deity_name}!")
        
        self.print_card(card)
        input("\nPressione ENTER para continuar...")
    
    def event_phase(self, player: Player):
        """Fase de eventos mitológicos."""
        print(f"\nEventos disponíveis: {player.events_available}")
        
        if player.events_available <= 0:
            print("Você não tem mais eventos disponíveis nesta partida.")
            input("\nPressione ENTER...")
            return
        
        print("\nEscolha um evento:")
        print("  1. ⚡ Ragnarök - Destrói todas as cartas")
        print("  2. ⚖️  Julgamento de Osíris - Julga carta do oponente")
        print("  3. 🌈 Bifrost - Invoca carta da reserva")
        print("  4. 🔮 Mistérios de Ísis/Orfeu - Protege suas cartas")
        print("  0. Voltar")
        
        choice = self.get_player_input("Evento", ["0", "1", "2", "3", "4"])
        
        if choice == "0":
            return
        
        event_map = {
            "1": EventType.RAGNAROK,
            "2": EventType.OSIRIS_JUDGMENT,
            "3": EventType.BIFROST,
            "4": EventType.MYSTERIES
        }
        
        event = create_event(event_map[choice])
        result = self.game_state.execute_event(event, player.id)
        
        print(f"\n{result.message}")
        
        if result.affected_cards:
            print(f"Cartas afetadas: {', '.join(result.affected_cards)}")
        
        input("\nPressione ENTER para continuar...")
    
    def view_card_detail(self, player: Player):
        """Mostra detalhes de uma carta."""
        print("\nEscolha uma carta para ver detalhes:")
        for i, card in enumerate(player.hand, 1):
            print(f"  {i}. {card}")
        
        card_idx = int(self.get_player_input(
            "Carta",
            [str(i) for i in range(1, len(player.hand) + 1)]
        )) - 1
        
        self.print_card(player.hand[card_idx], detailed=True)
        
        # Mostrar sincretismos
        card = player.hand[card_idx]
        if card.syncretism_links:
            print("\n🔄 SINCRETISMOS DISPONÍVEIS:")
            for link in card.syncretism_links:
                bonus = ", ".join([f"{k}: +{v}" for k, v in link.attribute_bonus.items()])
                print(f"   → {link.deity_name} ({link.pantheon.value}): {bonus}")
        
        input("\nPressione ENTER para voltar...")
    
    def show_game_over(self):
        """Mostra a tela de fim de jogo."""
        self.clear_screen()
        winner = self.game_state.get_winner()
        
        self.print_header("🏆 FIM DE JOGO 🏆")
        
        print("\n📊 PLACAR FINAL:")
        for player in self.game_state.players:
            status = "👑 VENCEDOR!" if player == winner else ""
            print(f"   {player.name}: {player.score} pontos {status}")
        
        print(f"\n🎉 Parabéns, {winner.name}! 🎉")
        
        print("\n📜 HISTÓRICO DE EVENTOS:")
        for event in self.game_state.event_history[-10:]:
            print(f"   • {event}")
        
        input("\nPressione ENTER para voltar ao menu...")
    
    def run(self):
        """Loop principal do jogo."""
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.setup_game()
                
                while self.game_state.current_phase != GamePhase.GAME_OVER:
                    self.play_turn()
                
                self.show_game_over()
                
            elif choice == "2":
                self.show_rules()
                
            elif choice == "3":
                self.show_pantheons()
                
            elif choice == "4":
                print("\n👋 Até a próxima, mortal!")
                break
