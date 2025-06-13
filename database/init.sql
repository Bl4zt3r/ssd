CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS contenedores (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    ubicacion GEOGRAPHY(Point)
);

CREATE TABLE IF NOT EXISTS mediciones (
    id SERIAL PRIMARY KEY,
    contenedor_id INTEGER REFERENCES contenedores(id),
    nivel INTEGER,
    temp INTEGER,
    gases INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_mediciones_fecha ON mediciones(fecha);
CREATE INDEX IF NOT EXISTS idx_contenedores_ubicacion ON contenedores USING GIST (ubicacion);
