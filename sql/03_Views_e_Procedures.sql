USE MusicMetrics;

-- View: Análise completa de músicas com features
CREATE OR REPLACE VIEW vw_tracks_complete AS
SELECT 
    t.track_id,
    t.track_name,
    ar.artist_name,
    al.album_name,
    t.duration_ms,
    t.explicit,
    t.popularity,
    t.release_date,
    YEAR(t.release_date) as release_year,
    af.danceability,
    af.energy,
    af.valence,
    af.tempo,
    af.acousticness,
    af.instrumentalness,
    af.liveness,
    af.speechiness
FROM dim_tracks t LEFT JOIN dim_artists ar ON t.artist_id = ar.artist_id
LEFT JOIN dim_albums al ON t.album_id = al.album_id LEFT JOIN dim_audio_features af ON t.track_id = af.track_id;

-- View: Estatísticas de audio features
CREATE OR REPLACE VIEW vw_audio_features_stats AS
SELECT 
    COUNT(*) as total_tracks,
    AVG(danceability) as avg_danceability,
    AVG(energy) as avg_energy,
    AVG(valence) as avg_valence,
    AVG(tempo) as avg_tempo,
    AVG(acousticness) as avg_acousticness,
    MIN(danceability) as min_danceability,
    MAX(danceability) as max_danceability,
    MIN(energy) as min_energy,
    MAX(energy) as max_energy
FROM dim_audio_features;

-- View: Músicas mais populares com audio features
CREATE OR REPLACE VIEW vw_top_popular_tracks AS
SELECT 
    t.track_id,
    t.track_name,
    a.artist_name,
    t.popularity,
    t.release_date,
    YEAR(t.release_date) as release_year,  -- Extrai o ano
    t.duration_ms,
    t.explicit,
    af.danceability,
    af.energy,
    af.valence,
    af.tempo,
    af.acousticness
FROM dim_tracks t INNER JOIN dim_artists a ON t.artist_id = a.artist_id
LEFT JOIN dim_audio_features af ON t.track_id = af.track_id
WHERE t.popularity > 0 ORDER BY t.popularity DESC;

-- View: Artistas mais populares com contagem de músicas
CREATE OR REPLACE VIEW vw_top_artists_with_tracks AS
SELECT 
    a.artist_id,
    a.artist_name,
    a.genres,
    a.popularity,
    a.followers,
    COUNT(t.track_id) as total_tracks,
    ROUND(AVG(t.popularity), 1) as avg_track_popularity,
    MAX(t.popularity) as max_track_popularity
FROM dim_artists a LEFT JOIN dim_tracks t ON a.artist_id = t.artist_id
WHERE a.popularity > 0  -- ← Artista com alguma popularidade
GROUP BY a.artist_id, a.artist_name, a.genres, a.popularity, a.followers
HAVING total_tracks > 0  -- ← Filtro de artistas com músicas
ORDER BY a.popularity DESC;

-- View: Evolução musical por década
CREATE OR REPLACE VIEW vw_music_by_decade AS
SELECT 
    FLOOR(YEAR(t.release_date) / 10) * 10 as decade,
    COUNT(t.track_id) as total_tracks,
    AVG(t.popularity) as avg_popularity,
    AVG(t.duration_ms / 60000) as avg_duration_min,
    AVG(af.danceability) as avg_danceability,
    AVG(af.energy) as avg_energy,
    AVG(af.valence) as avg_valence,
    AVG(af.tempo) as avg_tempo,
    AVG(af.acousticness) as avg_acousticness
FROM dim_tracks t LEFT JOIN dim_audio_features af ON t.track_id = af.track_id
WHERE t.release_date IS NOT NULL AND YEAR(t.release_date) BETWEEN 1900 AND 2025  -- Filtro de Anos
GROUP BY decade
ORDER BY decade;

-- View: Músicas mais dançantes
CREATE OR REPLACE VIEW vw_most_danceable_tracks AS
SELECT 
    t.track_name,
    a.artist_name,
    t.release_date,                        
    YEAR(t.release_date) as release_year,  
    af.danceability,
    af.energy,
    af.valence,
    t.popularity
FROM dim_tracks t INNER JOIN dim_artists a ON t.artist_id = a.artist_id
INNER JOIN dim_audio_features af ON t.track_id = af.track_id
WHERE af.danceability > 0.7
ORDER BY af.danceability DESC, t.popularity DESC;

SELECT * FROM vw_audio_features_stats;
SELECT * FROM vw_tracks_complete LIMIT 10;
SELECT * FROM vw_most_danceable_tracks LIMIT 10;
SELECT * FROM vw_music_by_decade LIMIT 10;
SELECT * FROM vw_top_artists_with_tracks LIMIT 10;
SELECT * FROM vw_top_popular_tracks LIMIT 10;
DESCRIBE dim_tracks;
