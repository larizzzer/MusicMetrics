"""
MusicMetrics - Extração de Dados do Spotify
Extrai dados pessoais do Spotify e salva em arquivos CSV para análise
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configurar autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='user-top-read user-read-recently-played user-library-read playlist-read-private'
))

def extract_top_artists(time_ranges=['short_term', 'medium_term', 'long_term'], limit=50):
    """Extrai top artistas para diferentes períodos"""
    all_artists = []
    
    for time_range in time_ranges:
        print(f"📊 Extraindo top artistas - {time_range}...")
        
        try:
            results = sp.current_user_top_artists(time_range=time_range, limit=limit)
            
            for idx, artist in enumerate(results['items'], 1):
                all_artists.append({
                    'rank': idx,
                    'time_range': time_range,
                    'artist_id': artist['id'],
                    'artist_name': artist['name'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'genres': ', '.join(artist['genres']) if artist['genres'] else None,
                    'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            time.sleep(0.5)  # Evitar rate limiting
            
        except Exception as e:
            print(f"❌ Erro ao extrair artistas ({time_range}): {e}")
    
    df = pd.DataFrame(all_artists)
    return df

def extract_top_tracks(time_ranges=['short_term', 'medium_term', 'long_term'], limit=50):
    """Extrai top músicas para diferentes períodos"""
    all_tracks = []
    
    for time_range in time_ranges:
        print(f"📊 Extraindo top músicas - {time_range}...")
        
        try:
            results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
            
            for idx, track in enumerate(results['items'], 1):
                all_tracks.append({
                    'rank': idx,
                    'time_range': time_range,
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
                    'artist_id': track['artists'][0]['id'],
                    'album_name': track['album']['name'],
                    'album_id': track['album']['id'],
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit'],
                    'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            time.sleep(0.5)  # Evitar rate limiting
            
        except Exception as e:
            print(f"❌ Erro ao extrair músicas ({time_range}): {e}")
    
    df = pd.DataFrame(all_tracks)
    return df

def extract_audio_features(track_ids):
    """Extrai características de áudio das músicas"""
    print(f"🎵 Extraindo audio features de {len(track_ids)} músicas...")
    
    all_features = []
    batch_size = 100  # API permite até 100 por requisição
    
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        
        try:
            features = sp.audio_features(batch)
            
            for feature in features:
                if feature:  # Algumas músicas podem não ter features disponíveis
                    all_features.append({
                        'track_id': feature['id'],
                        'danceability': feature['danceability'],
                        'energy': feature['energy'],
                        'key': feature['key'],
                        'loudness': feature['loudness'],
                        'mode': feature['mode'],
                        'speechiness': feature['speechiness'],
                        'acousticness': feature['acousticness'],
                        'instrumentalness': feature['instrumentalness'],
                        'liveness': feature['liveness'],
                        'valence': feature['valence'],
                        'tempo': feature['tempo'],
                        'time_signature': feature['time_signature']
                    })
            
            time.sleep(0.5)  # Evitar rate limiting
            
        except Exception as e:
            print(f"❌ Erro ao extrair audio features: {e}")
    
    df = pd.DataFrame(all_features)
    return df

def extract_recently_played(limit=50):
    """Extrai histórico recente de músicas tocadas"""
    print(f"⏮️ Extraindo últimas {limit} músicas tocadas...")
    
    all_played = []
    
    try:
        results = sp.current_user_recently_played(limit=limit)
        
        for item in results['items']:
            track = item['track']
            all_played.append({
                'played_at': item['played_at'],
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
                'artist_id': track['artists'][0]['id'],
                'album_name': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity']
            })
        
    except Exception as e:
        print(f"❌ Erro ao extrair músicas recentes: {e}")
    
    df = pd.DataFrame(all_played)
    return df

def save_data():
    """Função principal para extrair e salvar todos os dados"""
    print("=" * 60)
    print("🎵 MUSICMETRICS - Extração de Dados do Spotify")
    print("=" * 60)
    print()
    
    # Criar diretório de saída se não existir
    output_dir = '../data/raw'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. Extrair top artistas
    df_artists = extract_top_artists()
    if not df_artists.empty:
        filepath = f'{output_dir}/top_artists_{timestamp}.csv'
        df_artists.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"✅ Top artistas salvos: {filepath}")
        print(f"   Total de registros: {len(df_artists)}")
        print()
    
    # 2. Extrair top músicas
    df_tracks = extract_top_tracks()
    if not df_tracks.empty:
        filepath = f'{output_dir}/top_tracks_{timestamp}.csv'
        df_tracks.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"✅ Top músicas salvas: {filepath}")
        print(f"   Total de registros: {len(df_tracks)}")
        print()
        
        # 3. Extrair audio features das top músicas
        track_ids = df_tracks['track_id'].unique().tolist()
        df_features = extract_audio_features(track_ids)
        
        if not df_features.empty:
            filepath = f'{output_dir}/audio_features_{timestamp}.csv'
            df_features.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"✅ Audio features salvos: {filepath}")
            print(f"   Total de registros: {len(df_features)}")
            print()
    
    # 4. Extrair músicas tocadas recentemente
    df_recent = extract_recently_played()
    if not df_recent.empty:
        filepath = f'{output_dir}/recently_played_{timestamp}.csv'
        df_recent.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"✅ Músicas recentes salvas: {filepath}")
        print(f"   Total de registros: {len(df_recent)}")
        print()
    
    print("=" * 60)
    print("✅ Extração concluída com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    save_data()
