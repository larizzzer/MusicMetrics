USE MusicMetrics;

-- Views para saber o nome das colunas
SELECT * FROM vw_top_popular_tracks LIMIT 1;
SELECT * FROM vw_top_artists_with_tracks LIMIT 1;

-- Análise de Dados pelo SQL com regras de negócio
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
      COUNT(*) AS "Contagem",
      ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM dim_tracks), 2) AS "Percentual",
      CASE
		  WHEN explicit = 1 THEN "Explicíta"
          ELSE "Não Explicíta"
	  END AS Tipo
FROM dim_tracks
GROUP BY explicit
LIMIT 6;