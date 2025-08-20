CREATE TABLE conversation_sets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    speaker VARCHAR(100),
    context TEXT,             -- field context baru, default string kosong
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE conversation_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    set_id INT NOT NULL,
    path VARCHAR(255),
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (set_id) REFERENCES conversation_sets(id) ON DELETE CASCADE
);

INSERT INTO conversation_sets (title, category, speaker)
VALUES ('IT Interview 1', 'learning', 'tensa');

INSERT INTO conversation_items (set_id, path, content)
VALUES
(1, 'audio/day1.mp3', 'What are Python’s key features that make it popular for backend development?'),
(1, 'audio/day2.mp3', 'What is the difference between list, tuple, and set in Python?'),
(1, 'audio/day3.mp3', 'How does Python handle memory management?'),
(1, 'audio/day4.mp3', 'What are Python’s mutable and immutable data types?'),
(1, 'audio/day5.mp3', 'Can you explain the difference between shallow copy and deep copy in Python?'),
(1, 'audio/day6.mp3', 'What are Python decorators and when would you use them?'),
(1, 'audio/day7.mp3', 'What is the difference between @staticmethod, @classmethod, and instance methods?'),
(1, 'audio/day8.mp3', 'How does Python’s garbage collection work?'),
(1, 'audio/day9.mp3', 'What is the Global Interpreter Lock (GIL) and why is it important?');

CREATE TABLE users (
    id VARCHAR(24) PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) DEFAULT NULL,
    email VARCHAR(150) DEFAULT NULL,
    password VARCHAR(255) DEFAULT NULL,
    type ENUM('superadmin', 'admin', 'user') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    conversation_set_id INT DEFAULT 1,
    score INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_set_id) REFERENCES conversation_sets(id) ON DELETE SET DEFAULT
);



CREATE TABLE packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    quota_prompt INT NOT NULL DEFAULT 3,
    quota_input INT NOT NULL DEFAULT 4,
    quota_output INT NOT NULL DEFAULT 4,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO packages (name, description, quota_prompt, quota_input, quota_output)
VALUES
('basic', '', 3, 4, 4),
('standard', '', 10, 50, 50),
('premium', '', 100, 1000, 500),
('enterprise', '', 1000, 5000, 5000);

CREATE TABLE user_conversation_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(24) NOT NULL,
    item_id INT NOT NULL,                        -- pertanyaan yang dikirim
    answer TEXT,                                 -- jawaban user
    sentence_score INT DEFAULT 0,                -- skor kalimat (grammar dsb)
    context_score INT DEFAULT 0,                 -- skor konteks/makna
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- kapan dikirim
    answered_at DATETIME DEFAULT NULL,           -- kapan dijawab
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES conversation_items(id) ON DELETE CASCADE
);

CREATE TABLE llm_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(24) DEFAULT NULL,
    message TEXT NOT NULL,
    system_instruction TEXT DEFAULT NULL,
    response TEXT NOT NULL,
    input_token INT DEFAULT 0,
    output_token INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_package (
    user_id VARCHAR(24) PRIMARY KEY,
    package_id INT NOT NULL,
    quota_prompt INT NOT NULL,
    quota_input INT NOT NULL,
    quota_output INT NOT NULL,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE CASCADE
);