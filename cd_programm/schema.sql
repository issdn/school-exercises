DROP TABLE IF EXISTS cds;

CREATE TABLE cds (
    interpret TEXT CHECK(interpret <> ''),
    titel TEXT CHECK(titel <> ''),
    abspielzeit TEXT CHECK(abspielzeit <> '')
);