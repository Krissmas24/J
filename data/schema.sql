-- Schema for J Macro

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS session_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT,
    details TEXT
);

CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    state_json TEXT
);

CREATE TABLE IF NOT EXISTS event_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT,
    message TEXT
);

-- Initial default settings
INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'Dark');
INSERT OR IGNORE INTO settings (key, value) VALUES ('accent_color', '#FFD700');
INSERT OR IGNORE INTO settings (key, value) VALUES ('opacity', '0.85');
INSERT OR IGNORE INTO settings (key, value) VALUES ('language', 'English');
INSERT OR IGNORE INTO settings (key, value) VALUES ('auto_start', 'false');
INSERT OR IGNORE INTO settings (key, value) VALUES ('webhook_url', '');
INSERT OR IGNORE INTO settings (key, value) VALUES ('anti_afk', 'true');
INSERT OR IGNORE INTO settings (key, value) VALUES ('auto_sell', 'false');
INSERT OR IGNORE INTO settings (key, value) VALUES ('shake_threshold', '250');
INSERT OR IGNORE INTO settings (key, value) VALUES ('bar_speed_multiplier', '1.0');
