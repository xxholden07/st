"""
Dados do Baralho - 32 cartas organizadas em 8 grupos de 4.
Cada grupo representa uma categoria temática de divindades.
"""
from models.card import Card, Attributes, Pantheon, SyncretismLink


def create_deck() -> list[Card]:
    """
    Cria o baralho completo com 32 cartas.
    Grupos:
        1 - Deuses Supremos (Céu/Trovão)
        2 - Deuses da Guerra
        3 - Deuses da Sabedoria
        4 - Deuses da Justiça/Ordem
        5 - Deuses do Submundo
        6 - Deuses do Sol/Luz
        7 - Deuses da Fertilidade/Natureza
        8 - Deuses Primordiais/Caos
    """
    deck = []
    
    # ============================================
    # GRUPO 1: Deuses Supremos (Céu/Trovão)
    # ============================================
    
    # 1A - Zeus (Greco-Romano) - SUPER TRUNFO
    zeus = Card(
        card_id="1A",
        group=1,
        name="Zeus",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=95,
            wisdom=85,
            justice=80,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Júpiter", Pantheon.GRECO_ROMAN, {"justice": 10}),
            SyncretismLink("Amon-Rá", Pantheon.EGYPTIAN, {"wisdom": 15}),
            SyncretismLink("Enlil", Pantheon.MESOPOTAMIAN, {"combat_power": 5})
        ],
        is_super_trump=True
    )
    deck.append(zeus)
    
    # 1B - Odin (Nórdico)
    odin = Card(
        card_id="1B",
        group=1,
        name="Odin",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=85,
            wisdom=100,  # Sacrificou olho por sabedoria
            justice=75,
            eternity=60   # Morre no Ragnarök
        ),
        syncretism_links=[
            SyncretismLink("Mercúrio", Pantheon.GRECO_ROMAN, {"wisdom": 5}),
            SyncretismLink("Thoth", Pantheon.EGYPTIAN, {"wisdom": 10})
        ]
    )
    deck.append(odin)
    
    # 1C - Amon (Egípcio)
    amon = Card(
        card_id="1C",
        group=1,
        name="Amon",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=80,
            wisdom=90,
            justice=85,
            eternity=95
        ),
        syncretism_links=[
            SyncretismLink("Zeus", Pantheon.GRECO_ROMAN, {"combat_power": 10}),
            SyncretismLink("Anu", Pantheon.MESOPOTAMIAN, {"eternity": 5})
        ]
    )
    deck.append(amon)
    
    # 1D - Anu (Mesopotâmico)
    anu = Card(
        card_id="1D",
        group=1,
        name="Anu",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=75,
            wisdom=85,
            justice=90,
            eternity=90
        ),
        syncretism_links=[
            SyncretismLink("Urano", Pantheon.GRECO_ROMAN, {"eternity": 10})
        ]
    )
    deck.append(anu)
    
    # ============================================
    # GRUPO 2: Deuses da Guerra
    # ============================================
    
    # 2A - Thor (Nórdico)
    thor = Card(
        card_id="2A",
        group=2,
        name="Thor",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=100,  # O Indomável
            wisdom=50,
            justice=70,
            eternity=55   # Morre no Ragnarök
        ),
        syncretism_links=[
            SyncretismLink("Hércules", Pantheon.GRECO_ROMAN, {"combat_power": 5}),
            SyncretismLink("Set", Pantheon.EGYPTIAN, {"combat_power": 10})
        ]
    )
    deck.append(thor)
    
    # 2B - Marte/Ares (Greco-Romano)
    marte = Card(
        card_id="2B",
        group=2,
        name="Marte",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=95,
            wisdom=40,
            justice=45,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Ares", Pantheon.GRECO_ROMAN, {"combat_power": 5}),
            SyncretismLink("Montu", Pantheon.EGYPTIAN, {"justice": 10})
        ]
    )
    deck.append(marte)
    
    # 2C - Sekhmet (Egípcio)
    sekhmet = Card(
        card_id="2C",
        group=2,
        name="Sekhmet",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=90,
            wisdom=55,
            justice=60,
            eternity=90
        ),
        syncretism_links=[
            SyncretismLink("Belona", Pantheon.GRECO_ROMAN, {"combat_power": 5})
        ]
    )
    deck.append(sekhmet)
    
    # 2D - Nergal (Mesopotâmico)
    nergal = Card(
        card_id="2D",
        group=2,
        name="Nergal",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=88,
            wisdom=50,
            justice=40,
            eternity=85
        ),
        syncretism_links=[
            SyncretismLink("Plutão", Pantheon.GRECO_ROMAN, {"justice": 5})
        ]
    )
    deck.append(nergal)
    
    # ============================================
    # GRUPO 3: Deuses da Sabedoria
    # ============================================
    
    # 3A - Thoth (Egípcio) - Inventor da Escrita
    thoth = Card(
        card_id="3A",
        group=3,
        name="Thoth",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=45,
            wisdom=100,  # Inventor da escrita
            justice=90,
            eternity=95
        ),
        syncretism_links=[
            SyncretismLink("Hermes", Pantheon.GRECO_ROMAN, {"combat_power": 10}),
            SyncretismLink("Nabu", Pantheon.MESOPOTAMIAN, {"wisdom": 5})
        ]
    )
    deck.append(thoth)
    
    # 3B - Minerva/Atena (Greco-Romano)
    minerva = Card(
        card_id="3B",
        group=3,
        name="Minerva",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=75,
            wisdom=95,
            justice=85,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Atena", Pantheon.GRECO_ROMAN, {"wisdom": 5}),
            SyncretismLink("Neith", Pantheon.EGYPTIAN, {"combat_power": 10})
        ]
    )
    deck.append(minerva)
    
    # 3C - Mímir (Nórdico) - Guardião da Fonte da Sabedoria
    mimir = Card(
        card_id="3C",
        group=3,
        name="Mímir",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=30,
            wisdom=98,
            justice=80,
            eternity=70
        ),
        syncretism_links=[]
    )
    deck.append(mimir)
    
    # 3D - Nabu (Mesopotâmico)
    nabu = Card(
        card_id="3D",
        group=3,
        name="Nabu",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=40,
            wisdom=92,
            justice=85,
            eternity=88
        ),
        syncretism_links=[
            SyncretismLink("Mercúrio", Pantheon.GRECO_ROMAN, {"wisdom": 5})
        ]
    )
    deck.append(nabu)
    
    # ============================================
    # GRUPO 4: Deuses da Justiça/Ordem
    # ============================================
    
    # 4A - Maat (Egípcio) - Pena da Verdade
    maat = Card(
        card_id="4A",
        group=4,
        name="Maat",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=30,
            wisdom=85,
            justice=100,  # Essencial para Julgamento
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Themis", Pantheon.GRECO_ROMAN, {"justice": 5})
        ]
    )
    deck.append(maat)
    
    # 4B - Balder (Nórdico) - O Justo
    balder = Card(
        card_id="4B",
        group=4,
        name="Balder",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=60,
            wisdom=80,
            justice=95,
            eternity=50  # Morto por Loki
        ),
        syncretism_links=[
            SyncretismLink("Apolo", Pantheon.GRECO_ROMAN, {"wisdom": 10})
        ]
    )
    deck.append(balder)
    
    # 4C - Ishtar (Mesopotâmico)
    ishtar = Card(
        card_id="4C",
        group=4,
        name="Ishtar",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=70,
            wisdom=75,
            justice=90,
            eternity=92
        ),
        syncretism_links=[
            SyncretismLink("Afrodite", Pantheon.GRECO_ROMAN, {"wisdom": 5}),
            SyncretismLink("Hathor", Pantheon.EGYPTIAN, {"justice": 5})
        ]
    )
    deck.append(ishtar)
    
    # 4D - Têmis (Greco-Romano)
    temis = Card(
        card_id="4D",
        group=4,
        name="Têmis",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=35,
            wisdom=88,
            justice=98,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Maat", Pantheon.EGYPTIAN, {"justice": 5})
        ]
    )
    deck.append(temis)
    
    # ============================================
    # GRUPO 5: Deuses do Submundo
    # ============================================
    
    # 5A - Osíris (Egípcio) - Juiz dos Mortos
    osiris = Card(
        card_id="5A",
        group=5,
        name="Osíris",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=55,
            wisdom=85,
            justice=95,
            eternity=100  # Senhor da Vida Após a Morte
        ),
        syncretism_links=[
            SyncretismLink("Plutão", Pantheon.GRECO_ROMAN, {"combat_power": 10}),
            SyncretismLink("Dionísio", Pantheon.GRECO_ROMAN, {"wisdom": 10})
        ]
    )
    deck.append(osiris)
    
    # 5B - Hel (Nórdico)
    hel = Card(
        card_id="5B",
        group=5,
        name="Hel",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=65,
            wisdom=70,
            justice=60,
            eternity=80
        ),
        syncretism_links=[
            SyncretismLink("Perséfone", Pantheon.GRECO_ROMAN, {"wisdom": 10})
        ]
    )
    deck.append(hel)
    
    # 5C - Hades/Plutão (Greco-Romano)
    hades = Card(
        card_id="5C",
        group=5,
        name="Hades",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=80,
            wisdom=75,
            justice=70,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Plutão", Pantheon.GRECO_ROMAN, {"justice": 10}),
            SyncretismLink("Osíris", Pantheon.EGYPTIAN, {"justice": 15})
        ]
    )
    deck.append(hades)
    
    # 5D - Ereshkigal (Mesopotâmico)
    ereshkigal = Card(
        card_id="5D",
        group=5,
        name="Ereshkigal",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=70,
            wisdom=72,
            justice=65,
            eternity=88
        ),
        syncretism_links=[
            SyncretismLink("Perséfone", Pantheon.GRECO_ROMAN, {"wisdom": 5})
        ]
    )
    deck.append(ereshkigal)
    
    # ============================================
    # GRUPO 6: Deuses do Sol/Luz
    # ============================================
    
    # 6A - Rá (Egípcio)
    ra = Card(
        card_id="6A",
        group=6,
        name="Rá",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=85,
            wisdom=90,
            justice=88,
            eternity=98
        ),
        syncretism_links=[
            SyncretismLink("Apolo", Pantheon.GRECO_ROMAN, {"wisdom": 10}),
            SyncretismLink("Shamash", Pantheon.MESOPOTAMIAN, {"justice": 5})
        ]
    )
    deck.append(ra)
    
    # 6B - Apolo (Greco-Romano)
    apolo = Card(
        card_id="6B",
        group=6,
        name="Apolo",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=78,
            wisdom=92,
            justice=85,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Rá", Pantheon.EGYPTIAN, {"combat_power": 5}),
            SyncretismLink("Shamash", Pantheon.MESOPOTAMIAN, {"justice": 10})
        ]
    )
    deck.append(apolo)
    
    # 6C - Freyr (Nórdico)
    freyr = Card(
        card_id="6C",
        group=6,
        name="Freyr",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=72,
            wisdom=68,
            justice=75,
            eternity=55
        ),
        syncretism_links=[]
    )
    deck.append(freyr)
    
    # 6D - Shamash (Mesopotâmico)
    shamash = Card(
        card_id="6D",
        group=6,
        name="Shamash",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=75,
            wisdom=85,
            justice=92,  # Deus da Justiça
            eternity=90
        ),
        syncretism_links=[
            SyncretismLink("Apolo", Pantheon.GRECO_ROMAN, {"wisdom": 5})
        ]
    )
    deck.append(shamash)
    
    # ============================================
    # GRUPO 7: Deuses da Fertilidade/Natureza
    # ============================================
    
    # 7A - Ísis (Egípcio)
    isis = Card(
        card_id="7A",
        group=7,
        name="Ísis",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=60,
            wisdom=95,
            justice=85,
            eternity=95
        ),
        syncretism_links=[
            SyncretismLink("Deméter", Pantheon.GRECO_ROMAN, {"wisdom": 5}),
            SyncretismLink("Inanna", Pantheon.MESOPOTAMIAN, {"combat_power": 10})
        ]
    )
    deck.append(isis)
    
    # 7B - Freya (Nórdico)
    freya = Card(
        card_id="7B",
        group=7,
        name="Freya",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=70,
            wisdom=80,
            justice=75,
            eternity=60
        ),
        syncretism_links=[
            SyncretismLink("Afrodite", Pantheon.GRECO_ROMAN, {"wisdom": 10})
        ]
    )
    deck.append(freya)
    
    # 7C - Deméter/Ceres (Greco-Romano)
    demeter = Card(
        card_id="7C",
        group=7,
        name="Deméter",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=50,
            wisdom=82,
            justice=80,
            eternity=100
        ),
        syncretism_links=[
            SyncretismLink("Ceres", Pantheon.GRECO_ROMAN, {"justice": 5}),
            SyncretismLink("Ísis", Pantheon.EGYPTIAN, {"wisdom": 10})
        ]
    )
    deck.append(demeter)
    
    # 7D - Tammuz (Mesopotâmico)
    tammuz = Card(
        card_id="7D",
        group=7,
        name="Tammuz",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=45,
            wisdom=70,
            justice=72,
            eternity=75  # Ciclo de morte e renascimento
        ),
        syncretism_links=[
            SyncretismLink("Adônis", Pantheon.GRECO_ROMAN, {"wisdom": 5})
        ]
    )
    deck.append(tammuz)
    
    # ============================================
    # GRUPO 8: Deuses Primordiais/Caos
    # ============================================
    
    # 8A - Nun (Egípcio) - Águas Primordiais
    nun = Card(
        card_id="8A",
        group=8,
        name="Nun",
        pantheon=Pantheon.EGYPTIAN,
        base_attributes=Attributes(
            combat_power=40,
            wisdom=80,
            justice=70,
            eternity=100  # Primordial
        ),
        syncretism_links=[
            SyncretismLink("Caos", Pantheon.GRECO_ROMAN, {"eternity": 5})
        ]
    )
    deck.append(nun)
    
    # 8B - Ymir (Nórdico) - Gigante Primordial
    ymir = Card(
        card_id="8B",
        group=8,
        name="Ymir",
        pantheon=Pantheon.NORSE,
        base_attributes=Attributes(
            combat_power=90,
            wisdom=50,
            justice=30,
            eternity=40  # Morto por Odin
        ),
        syncretism_links=[]
    )
    deck.append(ymir)
    
    # 8C - Caos (Greco-Romano)
    caos = Card(
        card_id="8C",
        group=8,
        name="Caos",
        pantheon=Pantheon.GRECO_ROMAN,
        base_attributes=Attributes(
            combat_power=50,
            wisdom=60,
            justice=50,
            eternity=100  # O Primeiro
        ),
        syncretism_links=[
            SyncretismLink("Nun", Pantheon.EGYPTIAN, {"wisdom": 10}),
            SyncretismLink("Tiamat", Pantheon.MESOPOTAMIAN, {"combat_power": 20})
        ]
    )
    deck.append(caos)
    
    # 8D - Tiamat (Mesopotâmico) - Dragão Primordial
    tiamat = Card(
        card_id="8D",
        group=8,
        name="Tiamat",
        pantheon=Pantheon.MESOPOTAMIAN,
        base_attributes=Attributes(
            combat_power=92,
            wisdom=65,
            justice=35,
            eternity=85  # Morta por Marduk
        ),
        syncretism_links=[
            SyncretismLink("Tifão", Pantheon.GRECO_ROMAN, {"combat_power": 5})
        ]
    )
    deck.append(tiamat)
    
    return deck


# Bônus por Panteão (para sincretismo)
PANTHEON_BONUSES = {
    Pantheon.GRECO_ROMAN: {
        "description": "Filosofia e Arte",
        "wisdom": 5,
        "eternity": 5
    },
    Pantheon.EGYPTIAN: {
        "description": "Mistérios e Eternidade",
        "eternity": 10,
        "justice": 5
    },
    Pantheon.NORSE: {
        "description": "Coragem e Batalha",
        "combat_power": 10,
        "wisdom": -5
    },
    Pantheon.MESOPOTAMIAN: {
        "description": "Ordem e Civilização",
        "justice": 10,
        "wisdom": 5
    }
}


# Descrições dos grupos para referência
GROUP_DESCRIPTIONS = {
    1: "Deuses Supremos (Céu/Trovão)",
    2: "Deuses da Guerra",
    3: "Deuses da Sabedoria",
    4: "Deuses da Justiça/Ordem",
    5: "Deuses do Submundo",
    6: "Deuses do Sol/Luz",
    7: "Deuses da Fertilidade/Natureza",
    8: "Deuses Primordiais/Caos"
}
