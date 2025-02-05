create or replace function public.check_connection()
returns json language sql as $$
  select json_build_object(
    'timestamp', now(),
    'connection', 'active'
  );
$$;

-- Habilitar la extensión para generar UUIDs si aún no está habilitada.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

----------------------------------------------------
-- Tabla: users
-- Almacena la información básica del usuario.
----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    auth_provider TEXT NOT NULL, -- Ejemplo: 'google', 'apple', 'github', 'email'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

----------------------------------------------------
-- Tabla: images
-- Registra las imágenes subidas y procesadas.
----------------------------------------------------
CREATE TABLE IF NOT EXISTS images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    original_image_url TEXT NOT NULL,
    processed_image_url TEXT,  -- Puede ser nulo hasta que se genere la imagen procesada.
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ,  -- Se actualizará cuando se procese la imagen.
    CONSTRAINT fk_images_users FOREIGN KEY (user_id)
      REFERENCES users (id) ON DELETE CASCADE
);

-- Índice para mejorar la búsqueda de imágenes por usuario.
CREATE INDEX IF NOT EXISTS idx_images_user_id ON images(user_id);

----------------------------------------------------
-- Tabla: character_analysis
-- Almacena el resultado del análisis por cada carácter.
----------------------------------------------------
CREATE TABLE IF NOT EXISTS character_analysis (
    id SERIAL PRIMARY KEY,
    image_id UUID NOT NULL,
    character CHAR(1) NOT NULL,
    score NUMERIC(4,3) NOT NULL,  -- Ej: 0.978, 0.823, etc.
    position INTEGER NOT NULL,    -- Posición del carácter en la secuencia.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_analysis_images FOREIGN KEY (image_id)
      REFERENCES images (id) ON DELETE CASCADE
);

-- Índice para búsquedas rápidas de análisis por imagen.
CREATE INDEX IF NOT EXISTS idx_analysis_image_id ON character_analysis(image_id);

----------------------------------------------------
-- (Opcional) Tabla: analysis_metadata
-- Si se requiere almacenar metadatos adicionales del análisis,
-- como el modelo utilizado o parámetros de la ejecución.
----------------------------------------------------
CREATE TABLE IF NOT EXISTS analysis_metadata (
    id SERIAL PRIMARY KEY,
    image_id UUID NOT NULL,
    model_name TEXT NOT NULL,
    execution_time_ms INTEGER,
    additional_info JSONB,  -- Para almacenar información extra en formato JSON.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_metadata_images FOREIGN KEY (image_id)
      REFERENCES images (id) ON DELETE CASCADE
);

-- Índice para búsquedas rápidas en metadatos.
CREATE INDEX IF NOT EXISTS idx_metadata_image_id ON analysis_metadata(image_id);
