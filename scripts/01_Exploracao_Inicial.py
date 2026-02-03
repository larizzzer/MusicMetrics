"""
MusicMetrics - Exploração Inicial dos Dados
Analisa os arquivos CSV do Kaggle para entender estrutura e qualidade dos dados
"""

import pandas as pd
import numpy as np
import os

# Caminho para a pasta onde estão os CSVs do Kaggle
DATA_PATH = '../MusicMetrics/data/raw/'

# Nomes dos arquivos
TRACKS_FILE = 'tracks.csv'
ARTISTS_FILE = 'artists.csv'


def analyze_csv(filepath, filename):
    """Analisa um arquivo CSV e mostra informações gerais"""
    print("=" * 80)
    print(f"📊 ANALISANDO: {filename}")
    print("=" * 80)
    
    try:
        # Ler o arquivo
        df = pd.read_csv(filepath)
        
        # Informações básicas
        print(f"\n✅ Arquivo carregado com sucesso!")
        print(f"📏 Dimensões: {df.shape[0]:,} linhas x {df.shape[1]} colunas")
        print(f"💾 Tamanho em memória: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Mostrar colunas
        print(f"\n📋 Colunas ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col} ({df[col].dtype})")
        
        # Primeiras linhas
        print(f"\n👀 Primeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Valores nulos
        print(f"\n❓ Valores Nulos:")
        null_counts = df.isnull().sum()
        null_percent = (null_counts / len(df) * 100).round(2)
        
        if null_counts.sum() == 0:
            print("  ✅ Nenhum valor nulo encontrado!")
        else:
            null_df = pd.DataFrame({
                'Coluna': null_counts.index,
                'Nulos': null_counts.values,
                'Percentual': null_percent.values
            })
            null_df = null_df[null_df['Nulos'] > 0].sort_values('Nulos', ascending=False)
            print(null_df.to_string(index=False))
        
        # Duplicatas
        duplicates = df.duplicated().sum()
        print(f"\n🔄 Duplicatas: {duplicates:,} linhas ({duplicates/len(df)*100:.2f}%)")
        
        # Estatísticas de colunas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n📈 Estatísticas de Colunas Numéricas:")
            print(df[numeric_cols].describe().to_string())
        
        # Valores únicos de colunas categóricas (se não forem muitos)
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print(f"\n🏷️ Valores Únicos (Colunas de Texto):")
            for col in categorical_cols[:5]:  # Mostrar apenas as primeiras 5
                unique_count = df[col].nunique()
                print(f"  {col}: {unique_count:,} valores únicos")
                if unique_count <= 10:
                    print(f"    Valores: {df[col].unique()[:10].tolist()}")
        
        print("\n" + "=" * 80)
        return df
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return None

def analyze_tracks(df_tracks):
    """Análises específicas do arquivo tracks.csv"""
    print("\n" + "=" * 80)
    print("🎵 ANÁLISES ESPECÍFICAS - TRACKS")
    print("=" * 80)
    
    # Análise temporal
    if 'release_date' in df_tracks.columns:
        print("\n📅 Análise Temporal:")
        df_tracks['year'] = pd.to_datetime(df_tracks['release_date'], errors='coerce').dt.year
        year_counts = df_tracks['year'].value_counts().sort_index()
        
        print(f"  Ano mais antigo: {year_counts.index.min()}")
        print(f"  Ano mais recente: {year_counts.index.max()}")
        print(f"  Anos com mais músicas:")
        print(year_counts.nlargest(5).to_string())
    
    # Análise de popularidade
    if 'popularity' in df_tracks.columns:
        print("\n⭐ Análise de Popularidade:")
        print(f"  Média: {df_tracks['popularity'].mean():.2f}")
        print(f"  Mediana: {df_tracks['popularity'].median():.2f}")
        print(f"  Músicas com popularidade 0: {(df_tracks['popularity'] == 0).sum():,}")
        print(f"  Músicas com popularidade > 80: {(df_tracks['popularity'] > 80).sum():,}")
    
    # Análise de audio features
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'speechiness', 'liveness']
    
    existing_features = [f for f in audio_features if f in df_tracks.columns]
    
    if existing_features:
        print("\n🎚️ Audio Features - Médias:")
        for feature in existing_features:
            mean_val = df_tracks[feature].mean()
            print(f"  {feature.capitalize()}: {mean_val:.3f}")
    
    # Análise de músicas explícitas
    if 'explicit' in df_tracks.columns:
        print("\n🔞 Conteúdo Explícito:")
        explicit_count = df_tracks['explicit'].sum() if df_tracks['explicit'].dtype == bool else (df_tracks['explicit'] == 1).sum()
        print(f"  Músicas explícitas: {explicit_count:,} ({explicit_count/len(df_tracks)*100:.2f}%)")
    
    # Análise de duração
    if 'duration_ms' in df_tracks.columns:
        print("\n⏱️ Duração das Músicas:")
        df_tracks['duration_min'] = df_tracks['duration_ms'] / 60000
        print(f"  Média: {df_tracks['duration_min'].mean():.2f} minutos")
        print(f"  Mediana: {df_tracks['duration_min'].median():.2f} minutos")
        print(f"  Mais curta: {df_tracks['duration_min'].min():.2f} minutos")
        print(f"  Mais longa: {df_tracks['duration_min'].max():.2f} minutos")

def analyze_artists(df_artists):
    """Análises específicas do arquivo artists.csv"""
    print("\n" + "=" * 80)
    print("🎤 ANÁLISES ESPECÍFICAS - ARTISTS")
    print("=" * 80)
    
    # Top artistas por popularidade
    if 'popularity' in df_artists.columns:
        print("\n⭐ Top 10 Artistas Mais Populares:")
        top_artists = df_artists.nlargest(10, 'popularity')[['name', 'popularity', 'followers']]
        print(top_artists.to_string(index=False))
    
    # Análise de seguidores
    if 'followers' in df_artists.columns:
        print("\n👥 Análise de Seguidores:")
        print(f"  Média: {df_artists['followers'].mean():,.0f}")
        print(f"  Mediana: {df_artists['followers'].median():,.0f}")
        print(f"  Artista com mais seguidores: {df_artists['followers'].max():,.0f}")
    
    # Análise de gêneros
    if 'genres' in df_artists.columns:
        print("\n🎼 Análise de Gêneros:")
        # Contar artistas sem gênero
        no_genre = df_artists['genres'].isna().sum()
        print(f"  Artistas sem gênero definido: {no_genre:,} ({no_genre/len(df_artists)*100:.2f}%)")

def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("🎵 MUSICMETRICS - EXPLORAÇÃO INICIAL DOS DADOS")
    print("=" * 80)
    
    # Verificar se a pasta existe
    if not os.path.exists(DATA_PATH):
        print(f"\n❌ ERRO: Pasta não encontrada: {DATA_PATH}")
        print(f"   Crie a pasta ou altere o caminho no script (variável DATA_PATH)")
        return
    
    # Analisar tracks.csv
    tracks_path = os.path.join(DATA_PATH, TRACKS_FILE)
    if os.path.exists(tracks_path):
        df_tracks = analyze_csv(tracks_path, TRACKS_FILE)
        if df_tracks is not None:
            analyze_tracks(df_tracks)
    else:
        print(f"\n⚠️ Arquivo não encontrado: {tracks_path}")
    
    # Analisar artists.csv
    artists_path = os.path.join(DATA_PATH, ARTISTS_FILE)
    if os.path.exists(artists_path):
        df_artists = analyze_csv(artists_path, ARTISTS_FILE)
        if df_artists is not None:
            analyze_artists(df_artists)
    else:
        print(f"\n⚠️ Arquivo não encontrado: {artists_path}")
    
    print("\n" + "=" * 80)
    print("✅ EXPLORAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print("\n💡 Próximos passos:")
    print("   1. Revise os dados identificados")
    print("   2. Execute o script de limpeza (03_clean_and_transform.py)")
    print("   3. Carregue os dados no MySQL (04_load_to_mysql.py)")

if __name__ == "__main__":
    main()
