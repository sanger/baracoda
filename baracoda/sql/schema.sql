-- Counter table replaces PostgreSQL sequences
DROP TABLE IF EXISTS barcode_sequence_counters;
CREATE TABLE barcode_sequence_counters
(
    sequence_name VARCHAR(50) NOT NULL,
    current_value INTEGER NOT NULL,
    PRIMARY KEY (sequence_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Initialize all 6 sequences with their start values
INSERT INTO barcode_sequence_counters (sequence_name, current_value) VALUES
    ('heron', 200000),
    ('ht', 111111),
    ('sqp', 1),
    ('csm', 111111),
    ('pam', 111111),
    ('rvi', 111111);

-- Barcodes table
DROP TABLE IF EXISTS barcodes;
CREATE TABLE barcodes
(
    id INTEGER AUTO_INCREMENT,
    barcode VARCHAR(255) NOT NULL,
    prefix VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    barcodes_group_id INTEGER,
    PRIMARY KEY (id),
    INDEX barcodes_group_id_index (barcodes_group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Barcode groups table
DROP TABLE IF EXISTS barcodes_groups;
CREATE TABLE barcodes_groups
(
    id INTEGER AUTO_INCREMENT,
    created_at TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Child barcode counter
DROP TABLE IF EXISTS child_barcode_counter;
CREATE TABLE child_barcode_counter
(
    barcode VARCHAR(50) NOT NULL,
    child_count INTEGER,
    PRIMARY KEY (barcode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Alembic version tracking
DROP TABLE IF EXISTS alembic_version;
CREATE TABLE alembic_version
(
    version_num VARCHAR(32) NOT NULL,
    PRIMARY KEY (version_num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Set to last migration (will be updated after new migration created)
INSERT INTO alembic_version (version_num) VALUES ('4f525be49d95');