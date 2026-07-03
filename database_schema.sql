CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE assets(
    id INTEGER PRIMARY KEY,
    asset_name VARCHAR(100),
    asset_type VARCHAR(100),
    asset_tag VARCHAR(100) UNIQUE,
    purchase_date DATE,
    status VARCHAR(50),
    is_active BOOLEAN
);

CREATE TABLE allocations(
    id INTEGER PRIMARY KEY,
    asset_id INTEGER,
    employee_id INTEGER,
    assigned_date DATE,
    return_date DATE,
    allocation_status VARCHAR(50)
);
