-- Schema based on the provided diagram: users <-> profiles (1:1), profiles -> images (1:N)

CREATE TABLE IF NOT EXISTS profiles (
  id SERIAL PRIMARY KEY,
  sex TEXT NOT NULL CHECK (sex IN ('male', 'female', 'other')),
  sexual_preferences TEXT NOT NULL CHECK (sexual_preferences IN ('male', 'female', 'both', 'other')),
  biography TEXT,
  list_of_interests TEXT[] NOT NULL DEFAULT '{}',
  fame INTEGER NOT NULL DEFAULT 0 CHECK (fame >= 0),
  longitude NUMERIC(9,6),
  latitude  NUMERIC(9,6)
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  profile_id INTEGER UNIQUE REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  is_verified BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS images (
  id SERIAL PRIMARY KEY,
  profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  is_avatar BOOLEAN NOT NULL DEFAULT FALSE
);

-- Ensure only one avatar per profile
CREATE UNIQUE INDEX IF NOT EXISTS images_one_avatar_per_profile
  ON images (profile_id)
  WHERE is_avatar = TRUE;

-- ------------------------------------------------------------
-- Seed test data (10 users/profiles with avatars)
-- Note: docker-entrypoint-initdb.d scripts run only on first DB init.
-- ------------------------------------------------------------

INSERT INTO profiles (sex, sexual_preferences, biography, list_of_interests, fame, longitude, latitude) VALUES
  ('male',   'female', 'Coffee, hiking, and honest conversations.', ARRAY['hiking','coffee','travel']::text[], 42, 30.523400, 50.450100),
  ('female', 'male',   'Bookworm. Learning to cook Italian.',       ARRAY['books','cooking','movies']::text[], 18, 30.516700, 50.433300),
  ('other',  'both',   'Music producer. Night walks are the best.', ARRAY['music','photography','art']::text[], 67, 30.500000, 50.454660),
  ('male',   'both',   'Gym, startups, and board games.',           ARRAY['fitness','startups','boardgames']::text[], 55, 30.540000, 50.460000),
  ('female', 'both',   'Dog person. Sunday brunch enthusiast.',     ARRAY['dogs','brunch','yoga']::text[], 33, 30.490000, 50.420000),
  ('male',   'other',  'Trying every ramen place in town.',         ARRAY['food','ramen','cycling']::text[], 25, 30.610000, 50.490000),
  ('female', 'female', 'Design, museums, and spontaneous trips.',   ARRAY['design','museums','travel']::text[], 61, 30.520000, 50.470000),
  ('other',  'other',  'Quiet days, loud concerts.',                ARRAY['concerts','cats','gaming']::text[], 12, 30.450000, 50.410000),
  ('male',   'female', 'Runner. Learning Ukrainian.',               ARRAY['running','languages','nature']::text[], 47, 30.575000, 50.445000),
  ('female', 'male',   'Tea, poetry, and rainy weather.',           ARRAY['tea','poetry','movies']::text[], 29, 30.560000, 50.430000);

INSERT INTO users (profile_id, name, surname, email, password, is_verified) VALUES
  (1,  'Alex',   'Koval',     'alex.koval@example.com',   'password123', TRUE),
  (2,  'Marta',  'Shevchenko','marta.shevchenko@example.com','password123', TRUE),
  (3,  'Sam',    'Bondar',    'sam.bondar@example.com',   'password123', TRUE),
  (4,  'Ihor',   'Melnyk',    'ihor.melnyk@example.com',  'password123', TRUE),
  (5,  'Olena',  'Tkachenko', 'olena.tkachenko@example.com','password123', TRUE),
  (6,  'Danylo', 'Hrytsenko', 'danylo.hrytsenko@example.com','password123', TRUE),
  (7,  'Iryna',  'Pavlenko',  'iryna.pavlenko@example.com','password123', TRUE),
  (8,  'Noah',   'Sydorenko', 'noah.sydorenko@example.com','password123', TRUE),
  (9,  'Artem',  'Marchenko', 'artem.marchenko@example.com','password123', TRUE),
  (10, 'Sofia',  'Klymenko',  'sofia.klymenko@example.com','password123', TRUE);

INSERT INTO images (profile_id, image_url, is_avatar) VALUES
  (1,  'https://picsum.photos/seed/matcha-1/600/600',  TRUE),
  (2,  'https://picsum.photos/seed/matcha-2/600/600',  TRUE),
  (3,  'https://picsum.photos/seed/matcha-3/600/600',  TRUE),
  (4,  'https://picsum.photos/seed/matcha-4/600/600',  TRUE),
  (5,  'https://picsum.photos/seed/matcha-5/600/600',  TRUE),
  (6,  'https://picsum.photos/seed/matcha-6/600/600',  TRUE),
  (7,  'https://picsum.photos/seed/matcha-7/600/600',  TRUE),
  (8,  'https://picsum.photos/seed/matcha-8/600/600',  TRUE),
  (9,  'https://picsum.photos/seed/matcha-9/600/600',  TRUE),
  (10, 'https://picsum.photos/seed/matcha-10/600/600', TRUE);
