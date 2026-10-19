CREATE TABLE reklamodatel (
    id_reklamodatel INTEGER PRIMARY KEY,
    naimenovanie    VARCHAR(150) NOT NULL,
    telefon         VARCHAR(30)  NOT NULL
);

CREATE TABLE izdanie (
    id_izdanie   INTEGER PRIMARY KEY,
    nazvanie     VARCHAR(150) NOT NULL,
    tip_izdaniya VARCHAR(50)  NOT NULL,
    izdatelstvo  VARCHAR(150) NOT NULL
);

CREATE TABLE rascenka (
    id_rascenki INTEGER PRIMARY KEY,
    id_izdanie  INTEGER NOT NULL,
    cena        NUMERIC(10,2) NOT NULL CHECK (cena >= 0),
    CONSTRAINT fk_rascenka_izdanie FOREIGN KEY (id_izdanie)
        REFERENCES izdanie(id_izdanie) ON DELETE RESTRICT,
    CONSTRAINT uq_rascenka_izdanie UNIQUE (id_izdanie)
);

CREATE TABLE zayavka (
    id_zayavki       INTEGER PRIMARY KEY,
    id_reklamodatel  INTEGER NOT NULL,
    soderzhanie      TEXT NOT NULL,
    data_zayavki     DATE NOT NULL,
    CONSTRAINT fk_zayavka_reklamodatel FOREIGN KEY (id_reklamodatel)
        REFERENCES reklamodatel(id_reklamodatel) ON DELETE RESTRICT
);

CREATE TABLE razmeshchenie (
    id_razmeshcheniya INTEGER PRIMARY KEY,
    id_zayavki        INTEGER NOT NULL,
    id_izdanie        INTEGER NOT NULL,
    data_vyhoda       DATE NOT NULL,
    kolichestvo       INTEGER NOT NULL CHECK (kolichestvo > 0),
    CONSTRAINT fk_razmeshchenie_zayavka FOREIGN KEY (id_zayavki)
        REFERENCES zayavka(id_zayavki) ON DELETE RESTRICT,
    CONSTRAINT fk_razmeshchenie_izdanie FOREIGN KEY (id_izdanie)
        REFERENCES izdanie(id_izdanie) ON DELETE RESTRICT
);

CREATE INDEX idx_razmeshchenie_data_vyhoda ON razmeshchenie(data_vyhoda);
