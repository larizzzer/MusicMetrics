USE MusicMetrics;

-- Views para saber o nome das colunas
SELECT * FROM vw_top_popular_tracks LIMIT 1;
SELECT * FROM vw_top_artists_with_tracks LIMIT 1;
SELECT * FROM vw_music_by_decade LIMIT 1;

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