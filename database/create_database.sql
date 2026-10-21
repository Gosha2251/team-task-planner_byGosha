-- ============================================
-- Datubāzes izveide
-- ============================================

CREATE DATABASE IF NOT EXISTS team_task_planner
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE team_task_planner;

-- ============================================
-- Teams
-- ============================================

CREATE TABLE IF NOT EXISTS Teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- ============================================
-- Users
-- ============================================

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    team_id INT,

    FOREIGN KEY (team_id)
        REFERENCES Teams(id)
        ON DELETE SET NULL
);

-- ============================================
-- Status
-- ============================================

CREATE TABLE IF NOT EXISTS Status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- ============================================
-- Tasks
-- ============================================

CREATE TABLE IF NOT EXISTS Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status_id INT NOT NULL,
    assigned_to INT,
    team_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (status_id)
        REFERENCES Status(id),

    FOREIGN KEY (assigned_to)
        REFERENCES Users(id)
        ON DELETE SET NULL,

    FOREIGN KEY (team_id)
        REFERENCES Teams(id)
        ON DELETE CASCADE
);

-- ============================================
-- Comments
-- ============================================

CREATE TABLE IF NOT EXISTS Comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (task_id)
        REFERENCES Tasks(id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
);

-- ============================================
-- Sākotnējie statusi
-- ============================================

INSERT IGNORE INTO Status (id, name)
VALUES
    (1, 'New'),
    (2, 'In Progress'),
    (3, 'Done');