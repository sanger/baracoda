DROP SEQUENCE IF EXISTS heron;
CREATE SEQUENCE heron
START 200000;

DROP SEQUENCE IF EXISTS ht;
CREATE SEQUENCE ht
START 111111;

DROP SEQUENCE IF EXISTS sqp;
CREATE SEQUENCE sqp
START 1;

DROP SEQUENCE IF EXISTS csm;
CREATE SEQUENCE csm
    START 111111;

DROP SEQUENCE IF EXISTS pam;
CREATE SEQUENCE pam
    START 111111;

DROP SEQUENCE IF EXISTS rvi;
CREATE SEQUENCE rvi
    START 111111;

DROP TABLE IF EXISTS barcodes;
CREATE TABLE barcodes
(
    id SERIAL,
    barcode VARCHAR(255) NOT NULL,
    prefix VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    barcodes_group_id integer,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS barcodes_groups;
CREATE TABLE barcodes_groups
(
    id SERIAL,
    created_at timestamp,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS child_barcode_counter;
CREATE TABLE child_barcode_counter
(
    barcode VARCHAR(50) NOT NULL,
    child_count integer,
    PRIMARY KEY (barcode)
);

DROP INDEX IF EXISTS barcodes_group_id_index;
CREATE INDEX barcodes_group_id_index ON barcodes(barcodes_group_id);

DROP TABLE IF EXISTS alembic_version;
CREATE TABLE alembic_version
(
    version_num character varying(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version
    (version_num)
VALUES
    ('db39b037a71d');
