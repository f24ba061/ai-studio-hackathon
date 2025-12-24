# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール（Playwright用の依存関係を追加）
RUN apt-get update && apt-get install -y \
    sqlite3 \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwrightのブラウザをインストール
RUN playwright install chromium

# アプリケーションのソースコードをコピー
COPY app/ ./app/
COPY database/ ./database/
COPY frontend/ ./frontend/

# テストスクリプトをコピー
COPY tests/ ./tests/

# データベース初期化スクリプトをコピー
COPY database/init_db.py ./
COPY database/add_tourist_spots.py ./database/
COPY database/add_sample_users.py ./database/
COPY database/add_sample_reviews.py ./database/

# 起動スクリプトをコピー
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ポート3001を公開
EXPOSE 3001

# 起動スクリプトを実行
ENTRYPOINT ["./docker-entrypoint.sh"]
