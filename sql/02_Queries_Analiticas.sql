USE MusicMetrics;

-- Aumento de timeout para algumas queries
SET SESSION wait_timeout = 900;
SET SESSION interactive_timeout = 900;

-- Views para saber o nome das colunas
SELECT * FROM vw_top_popular_tracks LIMIT 1;
SELECT * FROM vw_top_artists_with_tracks LIMIT 1;
SELECT * FROM vw_music_by_decade LIMIT 1;
SELECT * FROM vw_audio_features_stats;
SELECT * FROM vw_tracks_complete LIMIT 1;
SELECT * FROM vw_most_danceable_tracks LIMIT 1;
SELECT * FROM dim_tracks LIMIT 1;
SELECT * FROM dim_artists LIMIT 1;

-- Análise pelo SQL com regras de negócio
-- Top 10 artistas mais populares
SELECT
	  artist_name AS "Artista",
      popularity AS "Popularidade",
      FORMAT(followers, 0) AS "Seguidores"
FROM vw_top_artists_with_tracks
ORDER BY popularity DESC
LIMIT 10;

-- Músicas explicítas x Não explicítas
SELECT 
       CASE
		  WHEN explicit = 1 THEN "Explicíta"
          ELSE "Não Explicíta"
	  END AS Tipo,
      COUNT(*) AS "Contagem",
      ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM dim_tracks), 2) AS "Percentual"
FROM dim_tracks
GROUP BY explicit;

-- Duração média das músicas
SELECT 
	  ROUND(AVG(duration_ms) / 60000, 2) AS "Duração Média (min)",
      ROUND(MAX(duration_ms) / 60000, 2) AS "Música mais Longa (min)",
      ROUND(MIN(duration_ms) / 60000, 2) AS "Música mais Curta (min)"
FROM dim_tracks;

-- Top 5 artistas com mais músicas
SELECT
	  artist_name AS "Artista",
      total_tracks AS "Total de Músicas"
FROM vw_top_artists_with_tracks WHERE total_tracks >= 10
ORDER BY total_tracks DESC
LIMIT 5;

-- Evolução da popularidade por década
SELECT
	  decade AS "Decáda",
      total_tracks AS "Total de Músicas",
      ROUND(avg_popularity, 1) AS "Popularidade Média",
      CASE
		  WHEN avg_popularity < 10 THEN "Muito Baixa"
          WHEN avg_popularity < 25 THEN "Baixa"
          WHEN avg_popularity < 40 THEN "Média"
          ELSE "Alta"
	  END AS "Categoria"
FROM vw_music_by_decade
ORDER BY decade ASC;

-- Top 10 gêneros musicais mais comuns
SELECT
	  genres AS "Gênero",
      COUNT(*) AS "Quantidade de Artistas"
FROM dim_artists 
WHERE genres IS NOT NULL AND genres != '' AND genres != 'nan'
GROUP BY genres ORDER BY COUNT(*) DESC
LIMIT 10;
      
-- Artistas com apenas one-hit
SELECT
	  artist_name AS "Artista",
      total_tracks AS "Total de Músicas",
      max_track_popularity AS "Popularidade da Música"
FROM vw_top_artists_with_tracks 
WHERE total_tracks = 1 AND max_track_popularity > 70
ORDER BY max_track_popularity DESC;

-- Características Musicais a partir da Década de 1980
SELECT
	  decade AS "Década",
      ROUND(avg_danceability, 3) AS "Dançabilidade",
      ROUND(avg_energy, 3) AS "Energizada",
      ROUND(avg_valence, 3) AS "Valencia",
      ROUND(avg_tempo,3) AS "Tempo"
FROM vw_music_by_decade
WHERE decade >= 1980;

-- Artistas mais versáteis
SELECT 
    artist_name AS "Artista",
    total_tracks AS "Total de Músicas",
    max_danceability AS "Maior Dançabilidade",
    min_danceability AS "Menor Dançabilidade",
    variacao AS "Variação"
FROM tb_artist_versatility
WHERE total_tracks >= 20
ORDER BY variacao DESC
LIMIT 10;

-- Correlação: Popularidade vs Features de Áudio
SELECT
    CASE
        WHEN t.popularity > 80 THEN 'Populares'
        WHEN t.popularity BETWEEN 40 AND 60 THEN 'Medianas'
        WHEN t.popularity < 20 THEN 'Pouco Populares'
    END AS Categoria,
    ROUND(AVG(af.energy), 3) AS "Energia",
    ROUND(AVG(af.danceability), 3) AS "Dançabilidade",
    ROUND(AVG(af.valence), 3) AS "Valência",
    COUNT(*) AS "Total de Músicas"
FROM dim_tracks t INNER JOIN dim_audio_features af ON t.track_id = af.track_id
WHERE (t.popularity > 80 OR t.popularity BETWEEN 40 AND 60 OR t.popularity < 20)
AND af.energy IS NOT NULL AND af.danceability IS NOT NULL AND af.valence IS NOT NULL
GROUP BY Categoria
ORDER BY 
    CASE Categoria
        WHEN 'Populares' THEN 1
        WHEN 'Medianas' THEN 2
        WHEN 'Pouco Populares' THEN 3
    END;