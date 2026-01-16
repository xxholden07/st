# 🏛️ Super Trunfo Mitológico

Um jogo de cartas colecionáveis baseado em mitologias antigas, onde deuses de quatro panteões disputam a supremacia cósmica!

## 🎮 Características

### Estrutura do Baralho
- **32 cartas** organizadas em **8 grupos de 4** (1A-1D até 8A-8D)
- Cada carta representa uma divindade com atributos únicos

### Panteões
| Símbolo | Panteão | Característica | Bônus |
|---------|---------|----------------|-------|
| 🏛️ | Greco-Romano | Imortais do Olimpo | +5 Sabedoria, +5 Eternidade |
| 🏛️ | Egípcio | Mistérios do Nilo | +10 Eternidade, +5 Justiça |
| ⚡ | Nórdico | Guerreiros de Asgard | +10 Combate, -5 Sabedoria |
| 🌙 | Mesopotâmico | Ordem da Suméria | +10 Justiça, +5 Sabedoria |

### Atributos das Cartas
- ⚔️ **Poder de Combate**: Força em batalha (ex: Thor = 100)
- 📚 **Sabedoria**: Conhecimento (ex: Odin, Thoth = 100)
- ⚖️ **Justiça**: Retidão moral (ex: Maat = 100)
- ♾️ **Eternidade**: Imortalidade (Gregos = alta, Nórdicos = baixa)

### 🔄 Sistema de Sincretismo
Transforme suas cartas em equivalentes de outros panteões para ganhar bônus!

```
Zeus (Grego) → Júpiter (Romano) +10 Justiça
             → Amon-Rá (Egípcio) +15 Sabedoria
```

### ⚡ Eventos Mitológicos

| Evento | Efeito |
|--------|--------|
| **Ragnarök** | Destrói todas as cartas, redistribui novas |
| **Julgamento de Osíris** | Carta com Justiça < 50 é devorada por Ammit |
| **Bifrost** | Invoca carta da reserva (Midgard → Asgard) |
| **Mistérios de Ísis/Orfeu** | Protege cartas por 3 rodadas |

### ⭐ Super Trunfo
**Zeus** é o Super Trunfo e vence qualquer carta!

## 📁 Estrutura do Projeto

```
st/
├── main.py              # Ponto de entrada
├── models/
│   ├── card.py          # Classe Card e Attributes
│   └── events.py        # Eventos Mitológicos
├── game/
│   ├── player.py        # Classe Player
│   └── game_state.py    # Gerenciador do jogo
├── data/
│   └── deck_data.py     # Dados das 32 cartas
├── ui/
│   └── console_ui.py    # Interface de console
└── tests/
    ├── test_cards.py    # Testes de cartas
    └── test_events.py   # Testes de eventos
```

## 🚀 Como Executar

### Requisitos
- Python 3.10+

### Instalação

```bash
# Clone ou navegue até o diretório
cd st

# (Opcional) Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Execute o jogo
python main.py
```

### Executar Testes

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Rodar testes
python -m pytest tests/ -v
```

## 🎯 Como Jogar

1. **Inicie o jogo** e digite os nomes dos jogadores
2. **Escolha uma carta** da sua mão
3. **Selecione um atributo** para comparar
4. **Vença a rodada** se seu atributo for maior
5. **Use Sincretismo** para ganhar bônus em atributos
6. **Ative Eventos** para mudar o rumo da partida
7. **Vença** acumulando mais pontos ou ficando com todas as cartas

## 📊 Grupos de Cartas

| Grupo | Tema | Cartas |
|-------|------|--------|
| 1 | Deuses Supremos | Zeus⭐, Odin, Amon, Anu |
| 2 | Deuses da Guerra | Thor, Marte, Sekhmet, Nergal |
| 3 | Deuses da Sabedoria | Thoth, Minerva, Mímir, Nabu |
| 4 | Deuses da Justiça | Maat, Balder, Ishtar, Têmis |
| 5 | Deuses do Submundo | Osíris, Hel, Hades, Ereshkigal |
| 6 | Deuses do Sol | Rá, Apolo, Freyr, Shamash |
| 7 | Deuses da Fertilidade | Ísis, Freya, Deméter, Tammuz |
| 8 | Deuses Primordiais | Nun, Ymir, Caos, Tiamat |

## 🔮 Dicas Estratégicas

1. **Use o Sincretismo** para maximizar atributos antes de batalhas importantes
2. **Guarde Eventos** para momentos críticos
3. **Proteja cartas valiosas** com os Mistérios antes do Julgamento de Osíris
4. **Observe a Eternidade** dos deuses Nórdicos - são mortais no Ragnarök!
5. **O Super Trunfo (Zeus)** é imbatível, use com sabedoria

## 📜 Licença

Projeto educacional - uso livre para aprendizado.

---

*"Que os deuses guiem suas jogadas!"* ⚡🏛️🌙
