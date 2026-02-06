CREATE DATABASE MusicMetrics;

USE MusicMetrics;

-- Tabela de Artistas
CREATE TABLE IF NOT EXISTS dim_artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genres TEXT,
    followers INT,
    popularity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_artist_name (artist_name),
    INDEX idx_popularity (popularity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Álbuns
CREATE TABLE IF NOT EXISTS dim_albums (
    album_id VARCHAR(50) PRIMARY KEY,
    album_name VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50),
    release_date DATE,
    total_tracks INT,
    album_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES dim_artists(artist_id),
    INDEX idx_album_name (album_name),
    INDEX idx_release_date (release_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Músicas
CREATE TABLE IF NOT EXISTS dim_tracks (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50),
    album_id VARCHAR(50),
    duration_ms INT,
    explicit BOOLEAN,
    popularity INT,
    release_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES dim_artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES dim_albums(album_id),
    INDEX idx_track_name (track_name),
    INDEX idx_popularity (popularity),
    INDEX idx_release_date (release_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Características de Áudio
CREATE TABLE IF NOT EXISTS dim_audio_features (
    track_id VARCHAR(50) PRIMARY KEY,
    danceability DECIMAL(5,4),
    energy DECIMAL(5,4),
    key_value INT,
    loudness DECIMAL(6,3),
    mode_value INT,
    speechiness DECIMAL(5,4),
    acousticness DECIMAL(5,4),
    instrumentalness DECIMAL(5,4),
    liveness DECIMAL(5,4),
    valence DECIMAL(5,4),
    tempo DECIMAL(6,3),
    time_signature INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES dim_tracks(track_id),
    INDEX idx_danceability (danceability),
    INDEX idx_energy (energy),
    INDEX idx_valence (valence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Tempo
CREATE TABLE IF NOT EXISTS dim_time (
    date_id INT PRIMARY KEY AUTO_INCREMENT,
    full_date DATE NOT NULL UNIQUE,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20),
    week INT NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    INDEX idx_full_date (full_date),
    INDEX idx_year_month (year, month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Algumas alterações antes de ir para as análises
-- ============================================

-- Limpeza das tabelas para recriação dos dados
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE dim_audio_features;
TRUNCATE TABLE dim_tracks;
TRUNCATE TABLE dim_artists;
SET FOREIGN_KEY_CHECKS = 1;

-- Verificação se foi realmente salvo direito os dados
SELECT artist_name,
	   genres
FROM dim_artists
LIMIT 10;

SELECT track_name,
	   popularity
FROM dim_tracks
LIMIT 10;

SELECT *
FROM dim_audio_features
LIMIT 10;

-- Desabilitar safe mode
SET SQL_SAFE_UPDATES = 0;

-- Fazer o UPDATE
UPDATE dim_artists SET genres = NULL WHERE genres = 'nan' OR genres = '' OR genres = '[]';

-- Reabilitar safe mode
SET SQL_SAFE_UPDATES = 1;

-- Verificar quantos foram alterados
SELECT COUNT(*) as artistas_sem_genero
FROM dim_artists WHERE genres IS NULL;

