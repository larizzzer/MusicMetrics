"""
MusicMetrics - Limpeza e Transformação dos Dados
Limpa, transforma e prepara os dados para carga no MySQL
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import re

# ============================================

# Caminhos
RAW_DATA_PATH = '../MusicMetrics/data/raw/'
PROCESSED_DATA_PATH = '../MusicMetrics/data/processed/'

# Nomes dos arquivos de entrada
TRACKS_FILE = 'tracks.csv'
ARTISTS_FILE = 'artists.csv'

# Nomes dos arquivos de saída (processados)
OUTPUT_TRACKS = 'tracks_limpo.csv'
OUTPUT_ARTISTS = 'artists_limpo.csv'
OUTPUT_AUDIO_FEATURES = 'audios_limpos.csv'

# ============================================

def load_data():
    """Carrega os dados brutos"""
    print("📂 Carregando dados...")
    
    tracks_path = os.path.join(RAW_DATA_PATH, TRACKS_FILE)
    artists_path = os.path.join(RAW_DATA_PATH, ARTISTS_FILE)
    
    df_tracks = pd.read_csv(tracks_path)
    df_artists = pd.read_csv(artists_path)
    
    print(f"✅ Tracks carregadas: {len(df_tracks):,} linhas")
    print(f"✅ Artistas carregados: {len(df_artists):,} linhas")
    
    return df_tracks, df_artists

def clean_tracks(df_tracks):
    """Limpa e transforma o dataset de tracks"""
    print("\n🧹 Limpando dados de tracks...")
    
    df = df_tracks.copy()
    original_count = len(df)
    
    # 1. Remover duplicatas baseado no id
    print("  🔄 Removendo duplicatas...")
    df = df.drop_duplicates(subset=['id'], keep='first')
    duplicates_removed = original_count - len(df)
    if duplicates_removed > 0:
        print(f"    Removidas {duplicates_removed:,} duplicatas")
    
    # 2. Tratar valores nulos no ID (crítico)
    null_ids = df['id'].isnull().sum()
    if null_ids > 0:
        print(f"    ⚠️ Removendo {null_ids:,} linhas sem ID")
        df = df[df['id'].notnull()]
    
    # 3. Tratar valores nulos em name
    null_names = df['name'].isnull().sum()
    if null_names > 0:
        print(f"    ⚠️ Preenchendo {null_names:,} nomes vazios com 'Unknown'")
        df['name'] = df['name'].fillna('Unknown Track')
    
    # 4. Limpar e padronizar nomes de músicas
    print("  ✨ Padronizando nomes de músicas...")
    df['name'] = df['name'].str.strip()
    df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)
    
    # 5. Processar datas
    print("  📅 Processando datas...")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # Extrair ano
    df['release_year'] = df['release_date'].dt.year
    
    # Preencher anos nulos com a mediana
    if df['release_year'].isnull().sum() > 0:
        median_year = df['release_year'].median()
        df['release_year'] = df['release_year'].fillna(median_year)
    
    # 6. Converter explicit para boolean
    if df['explicit'].dtype != bool:
        df['explicit'] = df['explicit'].astype(bool)
    
    # 7. Tratar valores nulos em popularity
    if df['popularity'].isnull().sum() > 0:
        print(f"    Preenchendo {df['popularity'].isnull().sum():,} valores nulos em popularity com 0")
        df['popularity'] = df['popularity'].fillna(0)
    
    # 8. Converter duration_ms para minutos (adicionar coluna)
    if 'duration_ms' in df.columns:
        df['duration_min'] = (df['duration_ms'] / 60000).round(2)
    
    # 9. Limpar artistas (remover caracteres especiais extras)
    if 'artists' in df.columns:
        df['artists'] = df['artists'].fillna('Unknown Artist')
        df['artists'] = df['artists'].str.strip()
    
    # 10. Processar id_artists (pode vir como lista em formato string)
    if 'id_artists' in df.columns:
        print("  🔧 Processando IDs de artistas...")
        df['id_artists'] = df['id_artists'].fillna('')
    
        def limpar_artist_id(x):
            """Remove colchetes, aspas e pega apenas o primeiro ID"""
            if pd.isna(x) or x == '':
                return None
        
            # Converter para string
            x = str(x)

            # Remover colchetes externos: "['abc']" -> "'abc'"
            x = x.strip().strip('[]')
        
            # Remover aspas: "'abc'" -> "abc"
            x = x.strip().strip("'\"")
        
            # Se tiver múltiplos IDs separados por vírgula, pegar só o primeiro
            if ',' in x:
                x = x.split(',')[0].strip().strip("'\"")
        
            # Limpar novamente para garantir
            x = x.strip().strip("'\"")
        
            return x if x else None
    
        df['primary_artist_id'] = df['id_artists'].apply(limpar_artist_id)
    
        # Verificar quantos ficaram nulos
        null_count = df['primary_artist_id'].isnull().sum()
        print(f"    ✅ IDs processados")
        print(f"    ⚠️ {null_count:,} músicas sem artista válido")
    
        # Mostrar exemplos de antes e depois (primeiras 5 linhas)
        print("\n  📋 Exemplos de transformação:")
        for i in range(min(5, len(df))):
            original = df['id_artists'].iloc[i]
            limpo = df['primary_artist_id'].iloc[i]
            print(f"    Antes: {original}")
            print(f"    Depois: {limpo}\n")
    
    print(f"✅ Limpeza concluída: {len(df):,} linhas mantidas")
    
    return df

def clean_artists(df_artists):
    """Limpa e transforma o dataset de artists"""
    print("\n🧹 Limpando dados de artistas...")
    
    df = df_artists.copy()
    original_count = len(df)
    
    # 1. Remover duplicatas baseado no id
    print("  🔄 Removendo duplicatas...")
    df = df.drop_duplicates(subset=['id'], keep='first')
    duplicates_removed = original_count - len(df)
    if duplicates_removed > 0:
        print(f"    Removidas {duplicates_removed:,} duplicatas")
    
    # 2. Tratar valores nulos no ID
    null_ids = df['id'].isnull().sum()
    if null_ids > 0:
        print(f"    ⚠️ Removendo {null_ids:,} linhas sem ID")
        df = df[df['id'].notnull()]
    
    # 3. Tratar valores nulos em name
    null_names = df['name'].isnull().sum()
    if null_names > 0:
        print(f"    ⚠️ Preenchendo {null_names:,} nomes vazios")
        df['name'] = df['name'].fillna('Unknown Artist')
    
    # 4. Limpar nomes
    df['name'] = df['name'].str.strip()
    df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)
    
    # 5. Tratar popularity
    if df['popularity'].isnull().sum() > 0:
        print(f"    Preenchendo {df['popularity'].isnull().sum():,} valores nulos em popularity com 0")
        df['popularity'] = df['popularity'].fillna(0)
    
    # 6. Tratar followers
    if 'followers' in df.columns:
        if df['followers'].isnull().sum() > 0:
            print(f"    Preenchendo {df['followers'].isnull().sum():,} valores nulos em followers com 0")
            df['followers'] = df['followers'].fillna(0)
        df['followers'] = df['followers'].astype(int)
    
    # 7. Tratar genres (pode vir como string de lista)
    if 'genres' in df.columns:
        df['genres'] = df['genres'].fillna('[]')
        # Se vier como string de lista, limpar
        df['genres'] = df['genres'].apply(lambda x: x.strip('[]').replace("'", "") if isinstance(x, str) else x)
    
    print(f"✅ Limpeza concluída: {len(df):,} linhas mantidas")
    
    return df

def extract_audio_features(df_tracks):
    """Extrai audio features em um DataFrame separado"""
    print("\n🎵 Extraindo audio features...")
    
    audio_feature_cols = [
        'id', 'danceability', 'energy', 'key', 'loudness', 'mode',
        'speechiness', 'acousticness', 'instrumentalness', 'liveness',
        'valence', 'tempo', 'time_signature'
    ]
    
    # Verificar quais colunas existem
    existing_cols = [col for col in audio_feature_cols if col in df_tracks.columns]
    
    if len(existing_cols) <= 1:  # Só tem o ID
        print("  ⚠️ Nenhuma audio feature encontrada!")
        return None
    
    df_features = df_tracks[existing_cols].copy()
    
    # Renomear 'id' para 'track_id'
    df_features = df_features.rename(columns={'id': 'track_id'})
    
    # Tratar valores nulos (substituir pela mediana)
    for col in df_features.columns:
        if col != 'track_id' and df_features[col].isnull().sum() > 0:
            median_val = df_features[col].median()
            df_features[col] = df_features[col].fillna(median_val)
    
    print(f"✅ Audio features extraídas: {len(df_features):,} linhas")
    
    return df_features

def prepare_for_mysql(df_tracks, df_artists):
    """Prepara os dados para estrutura do MySQL"""
    print("\n🗄️ Preparando dados para MySQL...")
    
    # Para tracks: manter apenas colunas relevantes
    tracks_cols = ['id', 'name', 'popularity', 'duration_ms', 'explicit', 
                   'artists', 'primary_artist_id', 'release_date', 'release_year']
    
    existing_track_cols = [col for col in tracks_cols if col in df_tracks.columns]
    df_tracks_mysql = df_tracks[existing_track_cols].copy()
    
    # Renomear colunas para padrão do MySQL
    df_tracks_mysql = df_tracks_mysql.rename(columns={
        'id': 'track_id',
        'name': 'track_name',
        'popularity': 'track_popularity',
        'artists': 'artist_name'
    })
    
    # Para artists: manter colunas relevantes
    artists_cols = ['id', 'name', 'popularity', 'followers', 'genres']
    existing_artist_cols = [col for col in artists_cols if col in df_artists.columns]
    df_artists_mysql = df_artists[existing_artist_cols].copy()
    
    # Renomear colunas
    df_artists_mysql = df_artists_mysql.rename(columns={
        'id': 'artist_id',
        'name': 'artist_name',
        'popularity': 'artist_popularity',
        'followers': 'artist_followers',
        'genres': 'artist_genres'
    })
    
    print(f"✅ Dados preparados para MySQL")
    
    return df_tracks_mysql, df_artists_mysql

def save_processed_data(df_tracks, df_artists, df_features):
    """Salva os dados processados"""
    print("\n💾 Salvando dados processados...")
    
    # Criar diretório se não existir
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # Salvar tracks
    tracks_output = os.path.join(PROCESSED_DATA_PATH, OUTPUT_TRACKS)
    df_tracks.to_csv(tracks_output, index=False, encoding='utf-8-sig')
    print(f"  ✅ {OUTPUT_TRACKS} salvo ({len(df_tracks):,} linhas)")
    
    # Salvar artists
    artists_output = os.path.join(PROCESSED_DATA_PATH, OUTPUT_ARTISTS)
    df_artists.to_csv(artists_output, index=False, encoding='utf-8-sig')
    print(f"  ✅ {OUTPUT_ARTISTS} salvo ({len(df_artists):,} linhas)")
    
    # Salvar audio features (se existir)
    if df_features is not None:
        features_output = os.path.join(PROCESSED_DATA_PATH, OUTPUT_AUDIO_FEATURES)
        df_features.to_csv(features_output, index=False, encoding='utf-8-sig')
        print(f"  ✅ {OUTPUT_AUDIO_FEATURES} salvo ({len(df_features):,} linhas)")

def generate_report(df_tracks, df_artists):
    """Gera relatório de qualidade dos dados"""
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO DE QUALIDADE DOS DADOS")
    print("=" * 80)
    
    print("\n🎵 TRACKS:")
    print(f"  Total de músicas: {len(df_tracks):,}")
    print(f"  Período: {df_tracks['release_year'].min():.0f} - {df_tracks['release_year'].max():.0f}")
    print(f"  Popularidade média: {df_tracks['track_popularity'].mean():.2f}")
    print(f"  Músicas explícitas: {df_tracks['explicit'].sum():,} ({df_tracks['explicit'].sum()/len(df_tracks)*100:.2f}%)")
    
    print("\n🎤 ARTISTS:")
    print(f"  Total de artistas: {len(df_artists):,}")
    print(f"  Popularidade média: {df_artists['artist_popularity'].mean():.2f}")
    if 'artist_followers' in df_artists.columns:
        print(f"  Seguidores médios: {df_artists['artist_followers'].mean():,.0f}")
    
    print("\n" + "=" * 80)

def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("🎵 MUSICMETRICS - LIMPEZA E TRANSFORMAÇÃO")
    print("=" * 80)
    
    # 1. Carregar dados
    df_tracks, df_artists = load_data()
    
    # 2. Limpar tracks
    df_tracks_clean = clean_tracks(df_tracks)
    
    # 3. Limpar artists
    df_artists_clean = clean_artists(df_artists)
    
    # 4. Extrair audio features
    df_features = extract_audio_features(df_tracks_clean)
    
    # 5. Preparar para MySQL
    df_tracks_mysql, df_artists_mysql = prepare_for_mysql(df_tracks_clean, df_artists_clean)
    
    # 6. Salvar dados processados
    save_processed_data(df_tracks_mysql, df_artists_mysql, df_features)
    
    # 7. Gerar relatório
    generate_report(df_tracks_mysql, df_artists_mysql)
    
    print("\n✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"\n📂 Arquivos salvos em: {PROCESSED_DATA_PATH}")
    print("\n💡 Próximo passo: Execute 04_load_to_mysql.py para carregar no banco de dados")

if __name__ == "__main__":
    main()
