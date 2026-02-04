-- ============================================
-- VIEWS ANALÍTICAS
-- ============================================

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
FROM dim_tracks t
LEFT JOIN dim_artists ar ON t.artist_id = ar.artist_id
LEFT JOIN dim_albums al ON t.album_id = al.album_id
LEFT JOIN dim_audio_features af ON t.track_id = af.track_id;

-- View: Top artistas atual
CREATE OR REPLACE VIEW vw_current_top_artists AS
SELECT 
    fta.rank_position,
    a.artist_name,
    a.genres,
    a.popularity,
    a.followers,
    fta.time_range,
    fta.extracted_at
FROM fact_top_artists fta
INNER JOIN dim_artists a ON fta.artist_id = a.artist_id
WHERE fta.extracted_at = (SELECT MAX(extracted_at) FROM fact_top_artists)
ORDER BY fta.time_range, fta.rank_position;

-- View: Top músicas atual
CREATE OR REPLACE VIEW vw_current_top_tracks AS
SELECT 
    ftt.rank_position,
    t.track_name,
    ar.artist_name,
    t.popularity,
    t.duration_ms,
    af.danceability,
    af.energy,
    af.valence,
    ftt.time_range,
    ftt.extracted_at
FROM fact_top_tracks ftt
INNER JOIN dim_tracks t ON ftt.track_id = t.track_id
INNER JOIN dim_artists ar ON t.artist_id = ar.artist_id
LEFT JOIN dim_audio_features af ON t.track_id = af.track_id
WHERE ftt.extracted_at = (SELECT MAX(extracted_at) FROM fact_top_tracks)
ORDER BY ftt.time_range, ftt.rank_position;

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

-- ============================================
-- PROCEDURES ÚTEIS
-- ============================================

-- Procedure: Limpar dados antigos (manter apenas últimos 90 dias)
DELIMITER //
CREATE PROCEDURE sp_cleanup_old_data()
BEGIN
    DELETE FROM fact_listening_history 
    WHERE played_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    DELETE FROM fact_top_artists 
    WHERE extracted_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    DELETE FROM fact_top_tracks 
    WHERE extracted_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
END //
DELIMITER ;

-- ============================================
-- FIM DO SCHEMA
-- ============================================

SELECT 'Schema MusicMetrics criado com sucesso!' as status;
