-- 観光地レビューアプリ データベーススキーマ
--
-- ⚠️ 注意: このファイルはドキュメント・参考用です
-- 実際のデータベース初期化では database/init_db.py が使用されます。
-- init_db.py には追加のカラム（photo_filename, avg_rating等）やトリガーが含まれています。
--

-- ユーザーマスターテーブル
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 観光地マスターテーブル
CREATE TABLE IF NOT EXISTS tourist_spots (
    spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_name TEXT NOT NULL,
    address TEXT,
    access TEXT,
    business_hours TEXT,
    fee TEXT,
    map_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- レビューデータテーブル
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    spot_id INTEGER NOT NULL,
    review_content TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (spot_id) REFERENCES tourist_spots(spot_id) ON DELETE CASCADE
);

-- イベントマスターテーブル
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    location TEXT,
    area TEXT,
    category TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックスの作成（パフォーマンス向上のため）
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_spot ON reviews(spot_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_events_area ON events(area);
CREATE INDEX idx_events_date ON events(event_date);