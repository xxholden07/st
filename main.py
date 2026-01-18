#!/usr/bin/env python3
"""
Super Trunfo Mitológico
=======================
Um jogo de cartas colecionáveis baseado em mitologias antigas.

Características:
- 32 cartas divididas em 8 grupos de 4
- 4 panteões: Egípcio, Nórdico, Greco-Romano e Mesopotâmico
- Sistema de Sincretismo para alternar entre mitologias
- Eventos Mitológicos que alteram o fluxo do jogo

Autor: Super Trunfo Dev Team
Versão: 2.0.0
"""

import sys
import os

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Função principal - inicia o jogo."""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          SUPER TRUNFO MITOLÓGICO                             ║
    ║                                                              ║
    ║     Os deuses de quatro panteões ancestrais                  ║
    ║     disputam a supremacia cósmica!                           ║
    ║                                                              ║
    ║     Egípcio   |   Nórdico                                    ║
    ║     Greco-Romano   |   Mesopotâmico                          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("Escolha o modo de jogo:")
    print("  1. Interface Gráfica (Tkinter)")
    print("  2. Interface Console")
    
    try:
        choice = input("\nOpção (1/2): ").strip()
    except KeyboardInterrupt:
        print("\nAté logo!")
        return
    
    if choice == "1":
        try:
            from ui.visual_ui import run_visual_game
            run_visual_game()
        except ImportError as e:
            print(f"\nErro ao carregar interface gráfica: {e}")
            print("Iniciando interface de console...")
            from ui.console_ui import ConsoleUI
            ui = ConsoleUI()
            ui.run()
    else:
        from ui.console_ui import ConsoleUI
        ui = ConsoleUI()
        ui.run()


if __name__ == "__main__":
    main()
