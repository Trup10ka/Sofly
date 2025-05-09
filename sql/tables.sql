CREATE TABLE IF NOT EXISTS users
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS type_of_insurance
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS insurance
(
    id                INT PRIMARY KEY AUTO_INCREMENT,
    sofly_uuid              CHAR(36) NOT NULL DEFAULT (UUID()),
    type_of_insurance INT NOT NULL,
    user_id           INT NOT NULL,
    start_date        DATE,
    end_date          DATE,
    cost_per_month    DECIMAL(10, 2),
    status            ENUM ('active', 'inactive', 'pending') DEFAULT 'active',

    FOREIGN KEY (type_of_insurance) REFERENCES type_of_insurance (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
