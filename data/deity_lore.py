"""
Biografias e informações educativas sobre as divindades.
Sistema de aprendizado mitológico integrado ao jogo.
"""
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class DeityLore:
    """Informações educativas sobre uma divindade."""
    name: str
    title: str
    domain: str
    description: str
    characteristics: str
    relations: str
    equivalent: str  # Equivalente em outros panteões
    curiosity: str   # Curiosidade interessante


# Biografias organizadas por panteão
DEITY_LORE: Dict[str, DeityLore] = {
    # ═══════════════════════════════════════════════════════════
    # PANTEÃO EGÍPCIO
    # ═══════════════════════════════════════════════════════════
    
    "Amon": DeityLore(
        name="Amon",
        title="O Rei dos Deuses",
        domain="Céu, Criação, Realeza",
        description="Amon era o deus principal do panteão egípcio, cujo poder era tão central que foi sincretizado com o rei dos deuses greco-romanos. Seu nome significa 'O Oculto', representando o mistério da criação.",
        characteristics="Representado como um homem com coroa de duas plumas altas ou com cabeça de carneiro. Era considerado o protetor dos faraós e senhor de Tebas.",
        relations="Esposo de Mut; pai de Khonsu. Frequentemente fundido com Rá como Amon-Rá.",
        equivalent="Zeus (Greco-Romano), Júpiter (Romano)",
        curiosity="Amon era tão reverenciado que seu templo em Karnak é o maior complexo religioso já construído na história."
    ),
    
    "Rá": DeityLore(
        name="Rá",
        title="O Deus Sol",
        domain="Sol, Criação, Luz",
        description="Rá era o deus do sol e uma das divindades mais importantes do Egito Antigo. Acreditava-se que ele viajava pelo céu durante o dia em sua barca solar e atravessava o submundo à noite.",
        characteristics="Representado com cabeça de falcão coroada pelo disco solar. Era visto como o criador de todas as formas de vida.",
        relations="Pai de Shu e Tefnut; avô de Geb e Nut. Frequentemente fundido com Amon como Amon-Rá.",
        equivalent="Apolo (Greco-Romano), Shamash (Mesopotâmico)",
        curiosity="Os egípcios acreditavam que Rá nascia toda manhã e morria ao pôr do sol, renascendo eternamente."
    ),
    
    "Osíris": DeityLore(
        name="Osíris",
        title="Senhor do Submundo",
        domain="Morte, Ressurreição, Fertilidade",
        description="Osíris presidia o julgamento das almas no submundo, determinando o destino eterno de cada pessoa. Seu mito de morte e ressurreição simboliza os ciclos da natureza.",
        characteristics="Representado como um homem mumificado com pele verde ou preta, segurando o cajado e o mangual, símbolos da realeza.",
        relations="Esposo de Ísis; pai de Hórus; irmão de Set (seu assassino).",
        equivalent="Hades (Greco-Romano), Plutão (Romano), Ereshkigal (Mesopotâmico)",
        curiosity="O mito de Osíris é uma das mais antigas histórias de morte e ressurreição, influenciando religiões posteriores."
    ),
    
    "Ísis": DeityLore(
        name="Ísis",
        title="A Grande Mãe",
        domain="Magia, Maternidade, Cura",
        description="Ísis era a deusa mais poderosa do panteão egípcio, conhecida por sua magia incomparável. Ela concebeu o deus Hórus e era vista como a mãe divina de todos os faraós.",
        characteristics="Representada como uma mulher com o trono hieroglífico na cabeça ou com asas de abutre. Símbolo do amor maternal e da devoção.",
        relations="Esposa de Osíris; mãe de Hórus; irmã de Néftis e Set.",
        equivalent="Freya (Nórdico), Ishtar (Mesopotâmico)",
        curiosity="O culto de Ísis se espalhou por todo o Império Romano, sendo uma das últimas religiões pagãs a sobreviver."
    ),
    
    "Thoth": DeityLore(
        name="Thoth",
        title="O Escriba Divino",
        domain="Sabedoria, Escrita, Magia, Lua",
        description="Thoth era o deus da sabedoria, inventor da escrita hieroglífica e guardião do conhecimento sagrado. Era o escriba dos deuses e registrava o resultado do julgamento das almas.",
        characteristics="Representado com cabeça de íbis ou como um babuíno. Carregava uma paleta de escriba e era associado à lua.",
        relations="Consorte de Maat; conselheiro de Rá e Osíris.",
        equivalent="Hermes (Greco-Romano), Mercúrio (Romano), Nabu (Mesopotâmico)",
        curiosity="Os gregos identificaram Thoth com Hermes, criando a figura de Hermes Trismegisto, base do hermetismo."
    ),
    
    "Maat": DeityLore(
        name="Maat",
        title="A Personificação da Verdade",
        domain="Verdade, Justiça, Ordem Cósmica",
        description="Maat representava a ordem cósmica, a verdade e a justiça. No julgamento das almas, o coração do morto era pesado contra sua pena para determinar seu destino.",
        characteristics="Representada como uma mulher com uma pena de avestruz na cabeça. A pena era o símbolo da verdade.",
        relations="Filha de Rá; consorte de Thoth.",
        equivalent="Têmis (Greco-Romano), Themis (Grego)",
        curiosity="Os faraós juravam governar de acordo com Maat, garantindo harmonia entre o mundo dos deuses e dos homens."
    ),
    
    "Sekhmet": DeityLore(
        name="Sekhmet",
        title="A Poderosa",
        domain="Guerra, Cura, Destruição",
        description="Sekhmet era a feroz deusa da guerra com cabeça de leoa. Ela representava o poder destrutivo do sol e era tanto temida quanto reverenciada como protetora.",
        characteristics="Representada como uma mulher com cabeça de leoa, coroada pelo disco solar. Seu hálito criava o deserto.",
        relations="Esposa de Ptah; mãe de Nefertum. Vista como aspecto furioso de Hathor.",
        equivalent="Marte (Romano), Thor (Nórdico)",
        curiosity="Sacerdotes de Sekhmet eram também médicos, pois a deusa que trazia doenças também podia curá-las."
    ),
    
    "Nun": DeityLore(
        name="Nun",
        title="O Oceano Primordial",
        domain="Caos Primordial, Águas Primordiais",
        description="Nun era a personificação das águas primordiais do caos, que existiam antes da criação. De Nun emergiu o primeiro monte de terra e o deus criador.",
        characteristics="Representado como um homem barbudo nas águas ou simplesmente como o próprio oceano infinito. Conceito abstrato do caos aquático.",
        relations="Pai de todos os deuses através da criação; consorte de Naunet.",
        equivalent="Caos (Greco-Romano), Tiamat (Mesopotâmico), Ymir (Nórdico)",
        curiosity="Os egípcios acreditavam que Nun ainda existia nas bordas do universo, ameaçando retornar ao caos."
    ),
    
    # ═══════════════════════════════════════════════════════════
    # PANTEÃO NÓRDICO
    # ═══════════════════════════════════════════════════════════
    
    "Odin": DeityLore(
        name="Odin",
        title="Pai de Todos",
        domain="Sabedoria, Guerra, Morte, Poesia",
        description="Odin era o deus supremo do panteão nórdico, governando de seu trono Hlidskjalf em Asgard. Era um deus complexo, associado tanto à sabedoria quanto à guerra.",
        characteristics="Representado como um homem idoso de um olho só, vestindo manto e chapéu. Acompanhado pelos corvos Huginn e Muninn e pelos lobos Geri e Freki.",
        relations="Casado com Frigga; pai de Thor, Balder, Tyr e Vidar. Irmão de Vili e Vé.",
        equivalent="Zeus (Greco-Romano), Júpiter (Romano), Amon (Egípcio)",
        curiosity="Odin sacrificou um olho na fonte de Mímir em troca de sabedoria e ficou pendurado na árvore Yggdrasil por nove dias para aprender as runas."
    ),
    
    "Thor": DeityLore(
        name="Thor",
        title="O Deus do Trovão",
        domain="Trovão, Tempestades, Força, Proteção",
        description="Thor era o protetor da humanidade contra os gigantes e as forças do caos. Empunhando seu martelo mágico Mjölnir, ele era o mais popular dos deuses nórdicos entre o povo comum.",
        characteristics="Representado como um homem musculoso de barba ruiva, empunhando Mjölnir. Viajava em uma carruagem puxada por duas cabras.",
        relations="Filho de Odin e Jord (a Terra); casado com Sif; pai de Magni e Modi.",
        equivalent="Marte (Romano), Hércules (Greco-Romano)",
        curiosity="O dia 'Thursday' (quinta-feira em inglês) vem de 'Thor's Day' - o dia de Thor."
    ),
    
    "Freya": DeityLore(
        name="Freya",
        title="Senhora do Amor",
        domain="Amor, Fertilidade, Guerra, Magia",
        description="Freya era a deusa do amor e da fertilidade, mas também uma poderosa guerreira. Ela recebia metade dos guerreiros mortos em batalha em seu salão Sessrúmnir.",
        characteristics="Representada como uma bela mulher usando o colar Brísingamen. Viajava em uma carruagem puxada por gatos e possuía um manto de penas de falcão.",
        relations="Filha de Njord; irmã gêmea de Freyr. Casou-se com Óðr.",
        equivalent="Vênus (Romano), Afrodite (Greco-Romano), Ishtar (Mesopotâmico)",
        curiosity="Freya ensinou a magia seiðr aos deuses Aesir, uma forma de magia xamânica considerada feminina."
    ),
    
    "Balder": DeityLore(
        name="Balder",
        title="O Brilhante",
        domain="Luz, Pureza, Justiça, Paz",
        description="Balder era o deus mais amado de Asgard, conhecido por sua beleza, bondade e senso de justiça. Sua morte foi um dos eventos que desencadeou o Ragnarök.",
        characteristics="Representado como o mais belo dos deuses, irradiando luz. Sua presença trazia paz e alegria a todos.",
        relations="Filho de Odin e Frigga; irmão de Höðr (que o matou); casado com Nanna.",
        equivalent="Apolo (Greco-Romano)",
        curiosity="Frigga fez todos os seres jurarem não ferir Balder, exceto o visco, que Loki usou para causar sua morte."
    ),
    
    "Hel": DeityLore(
        name="Hel",
        title="Rainha dos Mortos",
        domain="Morte, Submundo",
        description="Hel governava Niflheim, o reino gelado dos mortos, onde recebiam aqueles que não morriam em batalha. Metade de seu corpo era vivo e belo, a outra metade era cadavérico.",
        characteristics="Representada com metade do corpo normal e metade em decomposição. Vivia em um salão chamado Éljúðnir (Miséria).",
        relations="Filha de Loki e da giganta Angrboda; irmã de Fenrir e Jörmungandr.",
        equivalent="Hades (Greco-Romano), Plutão (Romano), Ereshkigal (Mesopotâmico)",
        curiosity="Quando Balder morreu, Hel exigiu que todas as criaturas chorassem por ele para libertá-lo, mas Loki disfarçado se recusou."
    ),
    
    "Freyr": DeityLore(
        name="Freyr",
        title="Senhor da Prosperidade",
        domain="Sol, Fertilidade, Colheita, Paz",
        description="Freyr era o deus da fertilidade, do sol e da chuva, essencial para as colheitas abundantes. Era um dos deuses Vanir que passou a viver com os Aesir após a guerra entre eles.",
        characteristics="Representado como um homem bonito, frequentemente com um falo ereto simbolizando fertilidade. Possuía o javali dourado Gullinbursti.",
        relations="Filho de Njord; irmão gêmeo de Freya. Casou-se com a giganta Gerðr.",
        equivalent="Apolo (Greco-Romano), Shamash (Mesopotâmico)",
        curiosity="Freyr deu sua espada mágica por amor a Gerðr, o que o deixará desarmado no Ragnarök."
    ),
    
    "Mímir": DeityLore(
        name="Mímir",
        title="O Guardião da Sabedoria",
        domain="Sabedoria, Conhecimento, Memória",
        description="Mímir era o guardião da fonte da sabedoria localizada sob a raiz de Yggdrasil. Mesmo após sua morte, sua cabeça preservada continuou a aconselhar Odin.",
        characteristics="Originalmente um deus completo, depois conhecido apenas como uma cabeça falante preservada por Odin com ervas mágicas.",
        relations="Conselheiro de Odin; guardião da fonte sob Yggdrasil.",
        equivalent="Thoth (Egípcio), Minerva (Romano)",
        curiosity="Odin sacrificou seu olho na fonte de Mímir para beber de suas águas e obter sabedoria cósmica."
    ),
    
    "Ymir": DeityLore(
        name="Ymir",
        title="O Gigante Primordial",
        domain="Caos, Gelo, Criação",
        description="Ymir foi o primeiro ser a existir, um gigante de gelo nascido do encontro entre o fogo de Muspelheim e o gelo de Niflheim. Seu corpo foi usado para criar o mundo.",
        characteristics="Um gigante colossal de gelo e caos. De seu corpo, os deuses criaram a terra (carne), montanhas (ossos), céu (crânio) e nuvens (cérebro).",
        relations="Ancestral de todos os gigantes de gelo; morto por Odin, Vili e Vé.",
        equivalent="Caos (Greco-Romano), Tiamat (Mesopotâmico), Nun (Egípcio)",
        curiosity="O sangue de Ymir causou um dilúvio que matou quase todos os gigantes, exceto Bergelmir e sua família."
    ),
    
    # ═══════════════════════════════════════════════════════════
    # PANTEÃO GRECO-ROMANO
    # ═══════════════════════════════════════════════════════════
    
    "Zeus": DeityLore(
        name="Zeus",
        title="Rei dos Deuses",
        domain="Céu, Trovão, Justiça, Ordem",
        description="Zeus era o rei dos deuses olímpicos, governando do Monte Olimpo. Ele derrubou seu pai Cronos e dividiu o mundo com seus irmãos Poseidon e Hades.",
        characteristics="Representado como um homem maduro e majestoso com barba, segurando um raio. A águia e o carvalho eram seus símbolos sagrados.",
        relations="Filho de Cronos e Reia; casado com Hera; pai de Atena, Apolo, Ártemis, Ares, Hefesto, Hermes, Dioniso e muitos outros.",
        equivalent="Júpiter (Romano), Odin (Nórdico), Amon (Egípcio)",
        curiosity="Zeus foi salvo de ser engolido por Cronos quando Reia o substituiu por uma pedra enrolada em panos."
    ),
    
    "Marte": DeityLore(
        name="Marte",
        title="Deus da Guerra",
        domain="Guerra, Agricultura, Virilidade",
        description="Marte era muito mais reverenciado em Roma do que seu equivalente grego Ares. Ele representava não apenas a guerra, mas também a agricultura e a proteção do estado romano.",
        characteristics="Representado como um guerreiro em armadura completa, com capacete, escudo e lança. O lobo e o pica-pau eram seus animais sagrados.",
        relations="Filho de Júpiter e Juno; pai de Rômulo e Remo (fundadores de Roma).",
        equivalent="Ares (Grego), Thor (Nórdico), Sekhmet (Egípcio)",
        curiosity="O mês de março (March) foi nomeado em honra a Marte, pois era quando as campanhas militares romanas começavam."
    ),
    
    "Minerva": DeityLore(
        name="Minerva",
        title="Deusa da Sabedoria",
        domain="Sabedoria, Estratégia, Artes, Ofícios",
        description="Minerva era a deusa romana da sabedoria e das artes, patrona dos artesãos e estrategistas militares. Diferente de Marte, ela representava a guerra defensiva e estratégica.",
        characteristics="Representada como uma mulher guerreira com elmo, escudo com a cabeça da Górgona, e lança. A coruja era seu animal sagrado.",
        relations="Filha de Júpiter (nasceu de sua cabeça); virgem eterna.",
        equivalent="Atena (Grego), Thoth (Egípcio), Nabu (Mesopotâmico)",
        curiosity="Minerva fazia parte da Tríade Capitolina junto com Júpiter e Juno, os três deuses principais de Roma."
    ),
    
    "Hades": DeityLore(
        name="Hades",
        title="Senhor do Submundo",
        domain="Morte, Submundo, Riquezas",
        description="Hades governava o reino dos mortos, um lugar sombrio mas não necessariamente de tormento. Ele também era associado às riquezas minerais da terra.",
        characteristics="Representado como um homem sombrio com barba, segurando um cetro e às vezes o elmo da invisibilidade. Cérbero, o cão de três cabeças, guardava seu reino.",
        relations="Filho de Cronos e Reia; irmão de Zeus e Poseidon; casado com Perséfone.",
        equivalent="Plutão (Romano), Osíris (Egípcio), Hel (Nórdico)",
        curiosity="Os gregos evitavam dizer o nome de Hades por medo, preferindo chamá-lo de 'Plutão' (o rico)."
    ),
    
    "Apolo": DeityLore(
        name="Apolo",
        title="O Brilhante",
        domain="Sol, Música, Poesia, Profecia, Cura",
        description="Apolo era um dos deuses mais importantes e complexos do panteão grego, associado à luz, verdade, música e medicina. Seu oráculo em Delfos era o mais famoso do mundo antigo.",
        characteristics="Representado como um jovem belo e atlético, frequentemente com uma lira ou arco e flecha. O louro era sua planta sagrada.",
        relations="Filho de Zeus e Leto; irmão gêmeo de Ártemis.",
        equivalent="Rá (Egípcio), Freyr (Nórdico), Shamash (Mesopotâmico)",
        curiosity="A frase 'Conhece-te a ti mesmo' estava inscrita no Templo de Apolo em Delfos."
    ),
    
    "Têmis": DeityLore(
        name="Têmis",
        title="A Justiça Divina",
        domain="Justiça, Lei Divina, Ordem",
        description="Têmis era a personificação da justiça divina e da ordem natural. Ela presidia sobre as leis dos deuses e era conselheira de Zeus.",
        characteristics="Representada como uma mulher vendada segurando uma balança e uma espada. Simboliza a imparcialidade da justiça.",
        relations="Titânide, filha de Urano e Gaia; mãe das Horas e das Moiras com Zeus.",
        equivalent="Maat (Egípcio), Ishtar (Mesopotâmico como deusa da justiça)",
        curiosity="A imagem moderna da Justiça com olhos vendados e balança deriva diretamente de Têmis."
    ),
    
    "Caos": DeityLore(
        name="Caos",
        title="O Vazio Primordial",
        domain="Vazio, Origem, Potencialidade",
        description="Caos era o vazio primordial que existia antes de toda a criação. Não era um deus no sentido tradicional, mas a própria essência da qual tudo emergiu.",
        characteristics="Não possuía forma física, sendo a personificação do vazio e da escuridão primordial. Conceito abstrato de potencialidade infinita.",
        relations="Do Caos surgiram Gaia (Terra), Tártaro (Abismo), Eros (Amor) e Érebo (Escuridão).",
        equivalent="Nun (Egípcio), Tiamat (Mesopotâmico), Ymir (Nórdico)",
        curiosity="A palavra 'caos' em grego significa 'abismo' ou 'vazio', bem diferente do significado moderno de desordem."
    ),
    
    # ═══════════════════════════════════════════════════════════
    # PANTEÃO MESOPOTÂMICO
    # ═══════════════════════════════════════════════════════════
    
    "Anu": DeityLore(
        name="Anu",
        title="Rei do Céu",
        domain="Céu, Realeza Divina, Constelações",
        description="Anu era o deus supremo do panteão mesopotâmico, personificação do céu e fonte de toda autoridade divina. Seu nome significa literalmente 'céu' em sumério.",
        characteristics="Representado como uma figura majestosa com coroa de chifres, símbolo de divindade. A estrela de oito pontas era seu símbolo.",
        relations="Filho de Anshar e Kishar; pai de Enlil, Enki e Ishtar.",
        equivalent="Zeus (Greco-Romano), Odin (Nórdico), Amon (Egípcio)",
        curiosity="Anu raramente intervinha nos assuntos terrestres, delegando poder a seus filhos Enlil e Enki."
    ),
    
    "Ishtar": DeityLore(
        name="Ishtar",
        title="Rainha do Céu",
        domain="Amor, Guerra, Fertilidade, Justiça",
        description="Ishtar (conhecida como Inanna pelos sumérios) era a deusa mais importante e complexa da Mesopotâmia. Ela governava tanto o amor quanto a guerra, representando a dualidade da existência.",
        characteristics="Representada como uma mulher poderosa com leões e símbolos estelares. A estrela de oito pontas e o leão eram seus símbolos.",
        relations="Filha de Anu ou Sin; irmã de Ereshkigal; amante de Tammuz.",
        equivalent="Afrodite/Vênus (Greco-Romano), Freya (Nórdico)",
        curiosity="Ishtar desceu ao submundo para resgatar Tammuz, morrendo e renascendo - um dos mitos mais antigos de ressurreição."
    ),
    
    "Nergal": DeityLore(
        name="Nergal",
        title="Senhor da Destruição",
        domain="Guerra, Peste, Morte, Submundo",
        description="Nergal era o temível deus da guerra e das pragas, que conquistou o submundo e se tornou seu rei. Ele representava os aspectos mais destrutivos da existência.",
        characteristics="Representado como um guerreiro feroz, às vezes com cabeça de leão. Associado ao calor abrasador do sol do meio-dia.",
        relations="Filho de Enlil; esposo de Ereshkigal após conquistar o submundo.",
        equivalent="Marte/Ares (Greco-Romano), Sekhmet (Egípcio)",
        curiosity="Nergal invadiu o submundo com quatorze demônios, mas acabou se casando com Ereshkigal e tornando-se co-regente."
    ),
    
    "Nabu": DeityLore(
        name="Nabu",
        title="O Escriba Divino",
        domain="Sabedoria, Escrita, Profecias",
        description="Nabu era o deus da sabedoria e da escrita cuneiforme, guardião das tábuas do destino. Ele registrava os decretos dos deuses e os destinos dos mortais.",
        characteristics="Representado como um escriba com tábua de argila e estilete. O dragão-serpente era seu animal sagrado.",
        relations="Filho de Marduk e Zarpanitu; consorte de Tashmetu.",
        equivalent="Thoth (Egípcio), Hermes/Mercúrio (Greco-Romano)",
        curiosity="O nome 'Nabucodonosor' significa 'Nabu, protege meu herdeiro', mostrando a importância deste deus."
    ),
    
    "Shamash": DeityLore(
        name="Shamash",
        title="O Sol da Justiça",
        domain="Sol, Justiça, Verdade",
        description="Shamash era o deus do sol que via tudo o que acontecia na terra, tornando-se naturalmente o deus da justiça. O famoso Código de Hamurabi foi dado a ele por Shamash.",
        characteristics="Representado com raios saindo de seus ombros e segurando símbolos de justiça. Viajava pelo céu em uma carruagem.",
        relations="Filho de Sin (deus da lua); irmão de Ishtar; pai de Kittu (verdade) e Misharu (justiça).",
        equivalent="Apolo (Greco-Romano), Rá (Egípcio), Freyr (Nórdico)",
        curiosity="O Código de Hamurabi, uma das primeiras leis escritas, mostra Shamash entregando as leis ao rei."
    ),
    
    "Ereshkigal": DeityLore(
        name="Ereshkigal",
        title="Rainha do Submundo",
        domain="Submundo, Morte",
        description="Ereshkigal governava Irkalla, a terra dos mortos mesopotâmica. Diferente de Hades, seu reino era visto como um lugar de trevas e pó, onde os mortos existiam como sombras.",
        characteristics="Representada como uma mulher pálida e severa em seu trono de lápis-lazúli. Governava com mão de ferro sobre os mortos.",
        relations="Irmã de Ishtar; esposa de Nergal; mãe de Namtar (o destino).",
        equivalent="Hades/Plutão (Greco-Romano), Hel (Nórdico), Osíris (Egípcio)",
        curiosity="Quando Ishtar visitou o submundo, Ereshkigal a matou por ciúmes, mostrando a rivalidade entre as irmãs."
    ),
    
    "Tammuz": DeityLore(
        name="Tammuz",
        title="O Deus Moribundo",
        domain="Vegetação, Fertilidade, Ciclos",
        description="Tammuz (Dumuzi em sumério) era o deus da vegetação e pastor divino. Sua morte anual e ressurreição simbolizavam os ciclos das estações agrícolas.",
        characteristics="Representado como um jovem pastor belo. Sua descida ao submundo causava o inverno, e seu retorno trazia a primavera.",
        relations="Amante de Ishtar; passava metade do ano no submundo.",
        equivalent="Adônis (Greco-Romano), Osíris (Egípcio)",
        curiosity="O choro ritual por Tammuz era praticado até em Jerusalém, mencionado no livro de Ezequiel na Bíblia."
    ),
    
    "Tiamat": DeityLore(
        name="Tiamat",
        title="O Dragão do Caos",
        domain="Caos, Mar Primordial, Criação",
        description="Tiamat era a deusa primordial do oceano salgado, representando o caos antes da criação. Ela foi morta por Marduk, e seu corpo foi usado para criar o céu e a terra.",
        characteristics="Representada como um dragão ou serpente marinha colossal. Mãe dos primeiros deuses e também de monstros terríveis.",
        relations="Consorte de Apsu (águas doces); mãe dos primeiros deuses; avó de Marduk (seu assassino).",
        equivalent="Caos (Greco-Romano), Nun (Egípcio), Ymir (Nórdico)",
        curiosity="A batalha entre Marduk e Tiamat é o tema central do Enuma Elish, o mito de criação babilônico."
    ),
}


def get_deity_lore(deity_name: str) -> Optional[DeityLore]:
    """
    Retorna as informações sobre uma divindade.
    
    Args:
        deity_name: Nome da divindade
        
    Returns:
        DeityLore ou None se não encontrar
    """
    # Busca direta
    if deity_name in DEITY_LORE:
        return DEITY_LORE[deity_name]
    
    # Busca ignorando acentos e case
    normalized_search = _normalize_name(deity_name)
    for name, lore in DEITY_LORE.items():
        if _normalize_name(name) == normalized_search:
            return lore
    
    return None


def _normalize_name(name: str) -> str:
    """Remove acentos e normaliza o nome para comparação."""
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
    }
    result = name.lower()
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


# Introdução aos panteões para o menu de ajuda
PANTHEON_INTRODUCTIONS = {
    "Egípcio": """
╔══════════════════════════════════════════════════════════════╗
║              O PANTEÃO EGÍPCIO: DEUSES DO NILO               ║
╚══════════════════════════════════════════════════════════════╝

As divindades do Egito Antigo governavam todos os aspectos da 
existência, desde a concepção do universo até o julgamento da 
alma após a morte.

O Egito desenvolveu uma das mais complexas teologias do mundo 
antigo, onde deuses podiam se fundir (como Amon-Rá), manifestar 
diferentes aspectos, e governar domínios sobrepostos.

Conceitos-chave:
• Maat - A ordem cósmica e a verdade
• Ka e Ba - Aspectos da alma
• O julgamento de Osíris - Destino após a morte
• Sincretismo - Fusão de divindades
""",
    
    "Nórdico": """
╔══════════════════════════════════════════════════════════════╗
║          O PANTEÃO NÓRDICO: LENDAS DA ERA VIKING             ║
╚══════════════════════════════════════════════════════════════╝

A mitologia nórdica narra as lendas dos povos vikings, 
explicando desde a origem da humanidade até o apocalipse 
final conhecido como Ragnarök.

Uma característica marcante deste panteão é que seus deuses 
não são eternos. Eles enfrentam um destino inevitável em uma 
batalha apocalíptica onde muitos morrerão.

Conceitos-chave:
• Yggdrasil - A árvore do mundo
• Aesir e Vanir - As duas famílias de deuses
• Valhalla - Salão dos guerreiros mortos
• Ragnarök - O crepúsculo dos deuses
""",
    
    "Greco-Romano": """
╔══════════════════════════════════════════════════════════════╗
║         O PANTEÃO GRECO-ROMANO: DEUSES DO OLIMPO             ║
╚══════════════════════════════════════════════════════════════╝

A mitologia greco-romana foi profundamente influente, 
moldando a arte, literatura e pensamento ocidental por 
milênios.

Os romanos adaptaram os mitos gregos para refletir seus 
próprios valores, dando ênfase a questões políticas e morais 
que justificavam a glória de Roma.

Conceitos-chave:
• Monte Olimpo - Morada dos deuses
• Os Doze Olímpicos - Principais deuses
• Titãs - A geração anterior aos deuses
• Heróis - Semideuses e mortais excepcionais
""",
    
    "Mesopotâmico": """
╔══════════════════════════════════════════════════════════════╗
║          O PANTEÃO MESOPOTÂMICO: MITOS PRIMORDIAIS           ║
╚══════════════════════════════════════════════════════════════╝

Localizada entre os rios Tigre e Eufrates, a Mesopotâmia é 
o lar da religião mais antiga de que se tem registro escrito.

Um elemento central era o culto à figura feminina, 
frequentemente adorada como a "Deusa Primordial", vista como 
criadora e provedora de toda vida.

Conceitos-chave:
• Enuma Elish - O mito da criação
• Tábuas do Destino - Decretos divinos
• Ziggurats - Templos em degraus
• A Deusa Mãe - Poder criador feminino
"""
}
