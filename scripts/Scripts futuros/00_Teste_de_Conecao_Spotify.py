"""
MusicMetrics - Spotify API Connection Test
Testa a conexão com a API do Spotify e exibe informações básicas do usuário
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurar autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='user-top-read user-read-recently-played user-library-read playlist-read-private'
))

def test_connection():
    """Testa a conexão com a API do Spotify"""
    try:
        # Pegar informações do usuário atual
        user = sp.current_user()
        print(f"✅ Conectado com sucesso!")
        print(f"👤 Usuário: {user['display_name']}")
        print(f"📧 Email: {user.get('email', 'N/A')}")
        print(f"🎵 Conta: {user.get('product', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def get_top_artists(time_range='medium_term', limit=10):
    """
    Retorna os artistas mais ouvidos
    time_range: 'short_term' (4 semanas), 'medium_term' (6 meses), 'long_term' (anos)
    """
    try:
        results = sp.current_user_top_artists(time_range=time_range, limit=limit)
        
        print(f"\n🎤 Seus Top {limit} Artistas ({time_range}):")
        print("-" * 50)
        
        for idx, artist in enumerate(results['items'], 1):
            genres = ', '.join(artist['genres'][:3]) if artist['genres'] else 'N/A'
            print(f"{idx}. {artist['name']}")
            print(f"   Gêneros: {genres}")
            print(f"   Popularidade: {artist['popularity']}/100")
            print()
        
        return results['items']
    except Exception as e:
        print(f"❌ Erro ao buscar top artistas: {e}")
        return []

def get_top_tracks(time_range='medium_term', limit=10):
    """
    Retorna as músicas mais ouvidas
    time_range: 'short_term' (4 semanas), 'medium_term' (6 meses), 'long_term' (anos)
    """
    try:
        results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
        
        print(f"\n🎵 Suas Top {limit} Músicas ({time_range}):")
        print("-" * 50)
        
        for idx, track in enumerate(results['items'], 1):
            artists = ', '.join([artist['name'] for artist in track['artists']])
            print(f"{idx}. {track['name']}")
            print(f"   Artista(s): {artists}")
            print(f"   Álbum: {track['album']['name']}")
            print(f"   Popularidade: {track['popularity']}/100")
            print()
        
        return results['items']
    except Exception as e:
        print(f"❌ Erro ao buscar top músicas: {e}")
        return []

def get_recently_played(limit=10):
    """Retorna as músicas tocadas recentemente"""
    try:
        results = sp.current_user_recently_played(limit=limit)
        
        print(f"\n⏮️ Últimas {limit} Músicas Tocadas:")
        print("-" * 50)
        
        for idx, item in enumerate(results['items'], 1):
            track = item['track']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            played_at = item['played_at']
            
            print(f"{idx}. {track['name']}")
            print(f"   Artista(s): {artists}")
            print(f"   Tocada em: {played_at}")
            print()
        
        return results['items']
    except Exception as e:
        print(f"❌ Erro ao buscar músicas recentes: {e}")
        return []

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 MUSICMETRICS - Teste de Conexão Spotify API")
    print("=" * 50)
    
    # Testar conexão
    if test_connection():
        print("\n" + "=" * 50)
        
        # Buscar top artistas
        get_top_artists(time_range='short_term', limit=5)
        
        # Buscar top músicas
        get_top_tracks(time_range='short_term', limit=5)
        
        # Buscar músicas recentes
        get_recently_played(limit=5)
        
        print("=" * 50)
        print("✅ Teste concluído com sucesso!")
        print("=" * 50)
