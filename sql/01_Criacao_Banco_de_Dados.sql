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

SELECT artist_name,
	   genres
FROM dim_artists
LIMIT 10;

SELECT track_name,
	   popularity
FROM dim_tracks
LIMIT 10;

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
-- FATOS (Fact Tables)
-- ============================================

-- Tabela de Top Artistas (histórico de rankings)
CREATE TABLE IF NOT EXISTS fact_top_artists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    artist_id VARCHAR(50) NOT NULL,
    time_range VARCHAR(20) NOT NULL,
    rank_position INT NOT NULL,
    extracted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES dim_artists(artist_id),
    INDEX idx_time_range (time_range),
    INDEX idx_extracted_at (extracted_at),
    INDEX idx_rank (rank_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Top Músicas (histórico de rankings)
CREATE TABLE IF NOT EXISTS fact_top_tracks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    track_id VARCHAR(50) NOT NULL,
    time_range VARCHAR(20) NOT NULL,
    rank_position INT NOT NULL,
    extracted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES dim_tracks(track_id),
    INDEX idx_time_range (time_range),
    INDEX idx_extracted_at (extracted_at),
    INDEX idx_rank (rank_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de Histórico de Reprodução
CREATE TABLE IF NOT EXISTS fact_listening_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    track_id VARCHAR(50) NOT NULL,
    played_at TIMESTAMP NOT NULL,
    date_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES dim_tracks(track_id),
    FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
    INDEX idx_played_at (played_at),
    INDEX idx_date_id (date_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;




-- Limpeza das tabelas para recriação dos dados
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE dim_audio_features;
TRUNCATE TABLE dim_tracks;
TRUNCATE TABLE dim_artists;
SET FOREIGN_KEY_CHECKS = 1;

