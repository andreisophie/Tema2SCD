CREATE TABLE IF NOT EXISTS Tari (
    id SERIAL NOT NULL,
    nume_tara VARCHAR2(100) NOT NULL,
    latitudine DOUBLE PRECISION NOT NULL,
    longitudine DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nume_tara)
);

CREATE TABLE IF NOT EXISTS Orase (
    id SERIAL NOT NULL,
    id_tara INT NOT NULL,
    nume_oras VARCHAR2(100) NOT NULL,
    latitudine DOUBLE PRECISION NOT NULL,
    longitudine DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_tara) REFERENCES Tari(id) ON DELETE CASCADE,
    UNIQUE (id_tara, nume_oras)
);

CREATE TABLE IF NOT EXISTS Temperaturi (
    id SERIAL NOT NULL,
    valoare DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    id_oras INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_oras) REFERENCES Orase(id) ON DELETE CASCADE,
    UNIQUE (id_oras, timestamp)
);