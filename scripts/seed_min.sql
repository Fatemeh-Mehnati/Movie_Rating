-- Directors
INSERT INTO directors (id, name, birth_year, description) VALUES
(1, 'Christopher Nolan', 1970, 'British-American film director'),
(2, 'Francis Ford Coppola', 1939, 'American film director'),
(3, 'Frank Darabont', 1959, 'American film director')
ON CONFLICT (id) DO NOTHING;

-- Genres
INSERT INTO genres (id, name, description) VALUES
(1, 'Drama', 'Drama films'),
(2, 'Crime', 'Crime films'),
(3, 'Action', 'Action films'),
(4, 'Sci-Fi', 'Science fiction films'),
(5, 'Thriller', 'Thriller films')
ON CONFLICT (id) DO NOTHING;
