import pandas as pd

# Carregamento dos arquivos
df_tracks = pd.read_csv('../MusicMetrics/data/processed/tracks_limpo.csv')
df_artists = pd.read_csv('../MusicMetrics/data/processed/artists_limpo.csv')

print("=== DIAGNÓSTICO ===\n")

# 1. Verifica o formato dos IDs
print("📋 FORMATO DOS IDs:\n")
print("Primeiros 5 artist_id (tabela artists):")
print(df_artists['artist_id'].head(5).tolist())

print("\nPrimeiros 5 primary_artist_id (tabela tracks):")
print(df_tracks['primary_artist_id'].head(5).tolist())

# 2. Verifica quantos são nulos
print(f"\n❓ VALORES NULOS:\n")
print(f"primary_artist_id nulos: {df_tracks['primary_artist_id'].isnull().sum():,}")
print(f"artist_id nulos: {df_artists['artist_id'].isnull().sum():,}")

# 3. Verifica os tipos dos dados
print(f"\n🔢 TIPOS DE DADOS:\n")
print(f"Tipo de artist_id: {df_artists['artist_id'].dtype}")
print(f"Tipo de primary_artist_id: {df_tracks['primary_artist_id'].dtype}")

# 4. TESTE CRÍTICO: Verificar se há correspondência
print(f"\n🔍 TESTE DE CORRESPONDÊNCIA:\n")

# Pegar IDs únicos de cada tabela
artists_ids = set(df_artists['artist_id'].dropna().astype(str))
tracks_artists = set(df_tracks['primary_artist_id'].dropna().astype(str))

print(f"Total de artist_id únicos (artists): {len(artists_ids):,}")
print(f"Total de primary_artist_id únicos (tracks): {len(tracks_artists):,}")

# Quantos IDs de tracks existem em artists?
matching = tracks_artists.intersection(artists_ids)
print(f"\n✅ IDs que batem: {len(matching):,}")
print(f"❌ IDs que NÃO batem: {len(tracks_artists - matching):,}")

# Mostrar exemplos que NÃO batem
if len(tracks_artists - matching) > 0:
    print("\n📌 Exemplos de IDs que NÃO batem (primeiros 10):")
    for idx, id_val in enumerate(list(tracks_artists - matching)[:10]):
        print(f"  {idx+1}. {id_val}")