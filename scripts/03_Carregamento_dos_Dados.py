"""
MusicMetrics - Carga de Dados no MySQL
Carrega os dados limpos e processados no banco de dados MySQL
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# ============================================

# Caminhos dos arquivos processados
PROCESSED_DATA_PATH = '../MusicMetrics/data/processed/'
TRACKS_FILE = 'tracks_limpo.csv'
ARTISTS_FILE = 'artists_limpo.csv'
AUDIO_FEATURES_FILE = 'audios_limpos.csv'

# Configurações do banco
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE', 'MusicMetrics'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

# ============================================

def connect_to_mysql():
    """Conecta ao banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print(f"✅ Conectado ao MySQL: {DB_CONFIG['database']}")
            return connection
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def load_csv(filepath):
    """Carrega arquivo CSV"""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Arquivo carregado: {os.path.basename(filepath)} ({len(df):,} linhas)")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar {filepath}: {e}")
        return None

def load_artists(connection, df_artists):
    """Carrega dados de artistas na tabela dim_artists"""
    print("\n🎤 Carregando artistas...")
    
    cursor = connection.cursor()
    
    # SQL para inserir ou atualizar artistas
    insert_query = """
        INSERT INTO dim_artists (artist_id, artist_name, genres, followers, popularity)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            artist_name = VALUES(artist_name),
            genres = VALUES(genres),
            followers = VALUES(followers),
            popularity = VALUES(popularity),
            updated_at = CURRENT_TIMESTAMP
    """
    
    # Preparar dados
    records = []
    for _, row in df_artists.iterrows():
        records.append((
            str(row['artist_id']),
            str(row['artist_name']),
            str(row.get('artist_genres', '')),
            int(row.get('artist_followers', 0)),
            int(row.get('artist_popularity', 0))
        ))
    
    try:
        # Inserir em lotes
        batch_size = 500
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            total_inserted += len(batch)
            print(f"  📊 Progresso: {total_inserted:,}/{len(records):,} artistas", end='\r')
        
        print(f"\n  ✅ {len(records):,} artistas carregados")
        return True
    except Error as e:
        print(f"\n  ❌ Erro ao carregar artistas: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def load_tracks(connection, df_tracks):
    """Carrega dados de tracks na tabela dim_tracks"""
    print("\n🎵 Carregando músicas...")
    
    cursor = connection.cursor()
    
    # SQL para inserir ou atualizar tracks
    insert_query = """
        INSERT INTO dim_tracks (
            track_id, track_name, artist_id, album_id,
            duration_ms, explicit, popularity, release_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            track_name = VALUES(track_name),
            artist_id = VALUES(artist_id),
            duration_ms = VALUES(duration_ms),
            explicit = VALUES(explicit),
            popularity = VALUES(popularity),
            release_date = VALUES(release_date),
            updated_at = CURRENT_TIMESTAMP
    """
    
    # NOVO: Buscar todos os artist_ids válidos que existem no banco
    print("  🔍 Verificando artistas válidos no banco...")
    cursor.execute("SELECT artist_id FROM dim_artists")
    valid_artist_ids = set(row[0] for row in cursor.fetchall())
    print(f"  ✅ {len(valid_artist_ids):,} artistas válidos encontrados")
    
    # Preparar dados
    records = []
    skipped = 0
    errors = 0
    
    for _, row in df_tracks.iterrows():
        try:
            # Processar data de lançamento
            release_date = None
            if pd.notna(row.get('release_date')):
                try:
                    release_date = pd.to_datetime(row['release_date']).date()
                except:
                    release_date = None
            
            # Pegar artist_id
            artist_id = str(row.get('primary_artist_id', '')) if pd.notna(row.get('primary_artist_id')) else None
            
            # NOVO: Verificar se o artist_id existe antes de inserir
            if artist_id and artist_id not in valid_artist_ids:
                skipped += 1
                continue  # Pular esta música
            
<<<<<<< Updated upstream
            records.append((
                str(row['track_id']),
                str(row['track_name'])[:255],
                artist_id,  # Pode ser None se não tiver artista
=======
            # NOVO: Limitar track_name a 255 caracteres
            track_name = str(row['track_name'])
            if len(track_name) > 255:
                track_name = track_name[:255]
            
            records.append((
                str(row['track_id']),
                track_name,  # Já limitado a 255 caracteres
                artist_id,
>>>>>>> Stashed changes
                None,  # album_id (não temos no dataset)
                int(row.get('duration_ms', 0)),
                bool(row.get('explicit', False)),
                int(row.get('track_popularity', 0)),
                release_date
            ))
        except Exception as e:
            errors += 1
            if errors <= 5:  # Mostrar apenas os primeiros 5 erros
                print(f"\n  ⚠️ Erro ao processar linha: {e}")
    
    if skipped > 0:
        print(f"  ⚠️ {skipped:,} músicas puladas (artista não encontrado)")
    
    if skipped > 0:
        print(f"  ⚠️ {skipped:,} músicas puladas (artista não encontrado)")
    
    if errors > 5:
        print(f"  ⚠️ Total de erros ao processar: {errors}")
    
    try:
<<<<<<< Updated upstream
        # Inserir em lotes
=======
        # Inserir em lotes menores para evitar timeout
>>>>>>> Stashed changes
        batch_size = 500
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            total_inserted += len(batch)
            print(f"  📊 Progresso: {total_inserted:,}/{len(records):,} músicas", end='\r')
        
        print(f"\n  ✅ {len(records):,} músicas carregadas")
        return True
    except Error as e:
        print(f"\n  ❌ Erro ao carregar músicas: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def load_audio_features(connection, df_features):
    """Carrega audio features na tabela dim_audio_features"""
    print("\n🎚️ Carregando audio features...")
    
    cursor = connection.cursor()
    
    # SQL para inserir ou atualizar audio features
    insert_query = """
        INSERT INTO dim_audio_features (
            track_id, danceability, energy, key_value, loudness, mode_value,
            speechiness, acousticness, instrumentalness, liveness, valence,
            tempo, time_signature
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            danceability = VALUES(danceability),
            energy = VALUES(energy),
            key_value = VALUES(key_value),
            loudness = VALUES(loudness),
            mode_value = VALUES(mode_value),
            speechiness = VALUES(speechiness),
            acousticness = VALUES(acousticness),
            instrumentalness = VALUES(instrumentalness),
            liveness = VALUES(liveness),
            valence = VALUES(valence),
            tempo = VALUES(tempo),
            time_signature = VALUES(time_signature),
            updated_at = CURRENT_TIMESTAMP
    """
    
    # NOVO: Buscar track_ids válidos
    print("  🔍 Verificando músicas válidas no banco...")
    cursor.execute("SELECT track_id FROM dim_tracks")
    valid_track_ids = set(row[0] for row in cursor.fetchall())
    print(f"  ✅ {len(valid_track_ids):,} músicas válidas encontradas")
    
    # Preparar dados
    records = []
    skipped = 0
    
    for _, row in df_features.iterrows():
        track_id = str(row['track_id'])
        
        # Verificar se a música existe no banco
        if track_id not in valid_track_ids:
            skipped += 1
            continue
        
        records.append((
            track_id,
            float(row.get('danceability', 0)),
            float(row.get('energy', 0)),
            int(row.get('key', 0)),
            float(row.get('loudness', 0)),
            int(row.get('mode', 0)),
            float(row.get('speechiness', 0)),
            float(row.get('acousticness', 0)),
            float(row.get('instrumentalness', 0)),
            float(row.get('liveness', 0)),
            float(row.get('valence', 0)),
            float(row.get('tempo', 0)),
            int(row.get('time_signature', 4))
        ))
    
    if skipped > 0:
        print(f"  ⚠️ {skipped:,} audio features puladas (música não encontrada)")
    
    try:
        # Inserir em lotes
        batch_size = 500
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            cursor.executemany(insert_query, batch)
            connection.commit()
            total_inserted += len(batch)
            print(f"  📊 Progresso: {total_inserted:,}/{len(records):,} features", end='\r')
        
        print(f"\n  ✅ {len(records):,} audio features carregadas")
        return True
    except Error as e:
        print(f"\n  ❌ Erro ao carregar audio features: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def verify_load(connection):
    """Verifica a carga dos dados"""
    print("\n" + "=" * 80)
    print("📊 VERIFICAÇÃO DA CARGA")
    print("=" * 80)
    
    cursor = connection.cursor()
    
    queries = [
        ("Artistas", "SELECT COUNT(*) FROM dim_artists"),
        ("Músicas", "SELECT COUNT(*) FROM dim_tracks"),
        ("Audio Features", "SELECT COUNT(*) FROM dim_audio_features"),
    ]
    
    for name, query in queries:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"  {name}: {count:,} registros")
    
    cursor.close()
    print("=" * 80)

def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("🎵 MUSICMETRICS - CARGA DE DADOS NO MYSQL")
    print("=" * 80)
    
    # Verificar se arquivos processados existem
    tracks_path = os.path.join(PROCESSED_DATA_PATH, TRACKS_FILE)
    artists_path = os.path.join(PROCESSED_DATA_PATH, ARTISTS_FILE)
    features_path = os.path.join(PROCESSED_DATA_PATH, AUDIO_FEATURES_FILE)
    
    if not os.path.exists(tracks_path) or not os.path.exists(artists_path):
        print("\n❌ ERRO: Arquivos processados não encontrados!")
        print(f"   Execute primeiro o script: 02_Limpeza_e_Transformacao.py")
        return
    
    # Conectar ao MySQL
    connection = connect_to_mysql()
    if not connection:
        print("\n❌ Não foi possível conectar ao MySQL")
        print("   Verifique suas credenciais no arquivo .env")
        return
    
    try:
        # Carregar arquivos CSV
        print("\n📂 Carregando arquivos processados...")
        df_artists = load_csv(artists_path)
        df_tracks = load_csv(tracks_path)
        df_features = None
        
        if os.path.exists(features_path):
            df_features = load_csv(features_path)
        
        if df_artists is None or df_tracks is None:
            print("❌ Erro ao carregar arquivos")
            return
        
        # Carregar no MySQL (ordem importa devido às foreign keys)
        print("\n" + "=" * 80)
        print("🗄️ INICIANDO CARGA NO BANCO DE DADOS")
        print("=" * 80)
        
        # 1. Carregar artistas primeiro (tabela pai)
        success = load_artists(connection, df_artists)
        if not success:
            print("❌ Falha ao carregar artistas")
            return
        
        # 2. Carregar tracks
        success = load_tracks(connection, df_tracks)
        if not success:
            print("❌ Falha ao carregar músicas")
            return
        
        # 3. Carregar audio features (se existir)
        if df_features is not None:
            success = load_audio_features(connection, df_features)
            if not success:
                print("⚠️ Falha ao carregar audio features")
        
        # Verificar carga
        verify_load(connection)
        
        print("\n✅ CARGA CONCLUÍDA COM SUCESSO!")
        print("\n💡 Próximos passos:")
        print("   1. Execute queries SQL para análises")
        print("   2. Conecte o Power BI ao banco de dados")
        print("   3. Crie os dashboards!")
        
    except Exception as e:
        print(f"\n❌ Erro durante a carga: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Conexão com MySQL fechada")

if __name__ == "__main__":
    main()