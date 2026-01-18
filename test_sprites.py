"""
Script de teste para verificar o carregamento dos sprites.
"""
from pathlib import Path

def test_sprites():
    base_path = Path(__file__).parent / "personagens"
    
    print("=" * 60)
    print("TESTE DE CARREGAMENTO DE SPRITES")
    print("=" * 60)
    
    # Verifica o diretório base
    print(f"\n📁 Diretório base: {base_path}")
    print(f"   Existe: {base_path.exists()}")
    
    # Testa cartas de cada grupo
    print("\n🃏 TESTANDO CARTAS DOS PERSONAGENS:")
    card_ids = ["1A", "1B", "2A", "3A", "4A", "5A", "6A", "7A", "8A"]
    
    for card_id in card_ids:
        group = card_id[0]
        group_dir = base_path / f"st_card_arts_group{group}"
        
        if group_dir.exists():
            files = list(group_dir.iterdir())
            card_file = None
            
            for file in files:
                if file.name.startswith(card_id):
                    card_file = file
                    break
            
            if card_file:
                print(f"   ✓ {card_id}: {card_file.name}")
            else:
                print(f"   ✗ {card_id}: Arquivo não encontrado")
        else:
            print(f"   ✗ {card_id}: Diretório {group_dir.name} não existe")
    
    # Testa arena
    print("\n🏛️ TESTANDO CAMADAS DA ARENA:")
    arena_dir = base_path / "arena_layers"
    
    if arena_dir.exists():
        for layer in ["bg", "mid", "fg"]:
            layer_file = arena_dir / f"layer_{layer}.png"
            if layer_file.exists():
                print(f"   ✓ layer_{layer}.png: {layer_file.stat().st_size / 1024:.1f} KB")
            else:
                print(f"   ✗ layer_{layer}.png: Não encontrado")
    else:
        print(f"   ✗ Diretório arena_layers não existe")
    
    # Lista todos os arquivos disponíveis
    print("\n📋 ARQUIVOS DISPONÍVEIS:")
    for i in range(1, 9):
        group_dir = base_path / f"st_card_arts_group{i}"
        if group_dir.exists():
            files = sorted([f.name for f in group_dir.iterdir() if f.suffix == ".png"])
            print(f"\n   Grupo {i}:")
            for f in files:
                print(f"      - {f}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)

if __name__ == "__main__":
    test_sprites()
