#!/usr/bin/env python3
import sqlite3
import os
import sys

def get_db_path():
    """データベースファイルのパスを取得"""
    # 環境変数DB_PATHが設定されていればそれを使用（Docker用）
    db_path = os.environ.get('DB_PATH')
    if db_path:
        return db_path
    # 環境変数がなければデフォルトのパス（プロジェクトルート）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'data', 'tourism_review.db')

def add_sample_events():
    """群馬県のイベント用にサンプルデータを追加"""

    # データベースに接続
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 群馬県イベント用のサンプルデータ
    sample_events = [
        # 1月
        ('高崎だるま市', '2025-01-06', '少林山達磨寺', 'takasaki', '祭り', '日本三大だるま市の一つ。境内に縁起だるまの露店が並び、多くの参拝者で賑わいます。'),
        ('高崎だるま市', '2025-01-07', '少林山達磨寺', 'takasaki', '祭り', '日本三大だるま市の一つ。境内に縁起だるまの露店が並び、多くの参拝者で賑わいます。'),

        # 2月
        ('榛名湖氷上ワカサギ釣り', '2025-02-15', '榛名湖', 'ikaho', 'アウトドア', '冬の風物詩。凍結した榛名湖でワカサギ釣りが楽しめます。'),

        # 3月
        ('敷島公園 桜まつり', '2025-03-28', '敷島公園', 'maebashi', '花見', '約300本の桜が咲き誇る前橋市の人気花見スポット。夜間はライトアップも実施されます。'),

        # 4月
        ('赤城南面千本桜まつり', '2025-04-05', '前橋市赤城町', 'maebashi', '花見', '約1,000本のソメイヨシノが1.3kmにわたって咲き誇る桜の名所。'),
        ('みどり市さくらまつり', '2025-04-12', 'ながめ公園', 'kiryu', '花見', '渡良瀬川沿いの桜並木が美しい。桜のトンネルは圧巻です。'),

        # 5月
        ('草津温泉感謝祭', '2025-05-03', '草津温泉', 'kusatsu', '祭り', '温泉に感謝する伝統行事。餅つきや湯もみショーなどのイベントが開催されます。'),
        ('つつじまつり', '2025-05-10', '館林つつじが岡公園', 'tatebayashi', '花', '約1万株のつつじが咲き誇る圧巻の景色。'),

        # 6月
        ('沼田まつり', '2025-06-14', '沼田市中心街', 'minakami', '祭り', '天狗みこしが見どころの伝統的な夏祭り。'),

        # 7月
        ('前橋七夕まつり', '2025-07-12', '前橋市中心商店街', 'maebashi', '祭り', '豪華な七夕飾りが商店街を彩る夏の風物詩。'),
        ('榛名湖花火大会', '2025-07-25', '榛名湖畔', 'ikaho', '花火', '湖上に打ち上げられる花火が幻想的。約3,000発の花火が夏の夜を彩ります。'),

        # 8月
        ('桐生八木節まつり', '2025-08-02', '桐生市本町通り', 'kiryu', '祭り', '関東三大祭りの一つ。威勢の良い八木節踊りが街を盛り上げます。'),
        ('桐生八木節まつり', '2025-08-03', '桐生市本町通り', 'kiryu', '祭り', '関東三大祭りの一つ。威勢の良い八木節踊りが街を盛り上げます。'),
        ('前橋花火大会', '2025-08-09', '利根川河畔', 'maebashi', '花火', '約1万5千発の花火が夏の夜空を彩る、群馬県最大級の花火大会。'),
        ('渋川へそ祭り', '2025-08-16', '渋川市中心街', 'ikaho', '祭り', 'お腹に顔を描いて踊る、ユニークでユーモアあふれるお祭り。'),

        # 9月
        ('尾瀬紅葉シーズン', '2025-09-20', '尾瀬国立公園', 'minakami', '自然', '草紅葉が美しい秋の尾瀬。黄金色に染まる湿原は圧巻です。'),

        # 10月
        ('富岡製糸場秋まつり', '2025-10-11', '富岡製糸場', 'tomioka', '祭り', '世界遺産で開催される秋のイベント。地元グルメや伝統工芸の出展があります。'),
        ('伊香保まつり', '2025-10-18', '伊香保温泉', 'ikaho', '祭り', '伝統の樽みこしが石段街を練り歩く勇壮な祭り。'),

        # 11月
        ('妙義山紅葉まつり', '2025-11-08', '妙義山', 'tomioka', '自然', '奇岩と紅葉のコントラストが美しい秋のイベント。'),

        # 12月
        ('草津温泉感謝祭冬', '2025-12-06', '草津温泉湯畑', 'kusatsu', '祭り', '冬の湯畑でのライトアップイベント。幻想的な雰囲気の中、温泉に感謝します。'),
        # XSSテスト用イベント（level_3のBのバグ確認用）
        ('<img src=x onerror="alert(\'XSS攻撃\')">テストイベント', '2025-12-25', '群馬県高崎市', 'takasaki', 'その他', 'XSSテスト用のイベントです。このイベント名にはXSSコードが含まれています。'),
    ]

    # データを挿入
    try:
        cursor.executemany(
            'INSERT INTO events (event_name, event_date, location, area, category, description) VALUES (?, ?, ?, ?, ?, ?)',
            sample_events
        )
        conn.commit()
        print(f"✅ {len(sample_events)}件のイベントデータを追加しました！")

        # 追加後のイベント数を確認
        cursor.execute('SELECT COUNT(*) FROM events')
        total_count = cursor.fetchone()[0]
        print(f"📊 イベントテーブルの総データ数: {total_count}件")

        # 月別のイベント数を表示
        print("\n月別イベント数:")
        cursor.execute('''
            SELECT substr(event_date, 6, 2) as month, COUNT(*) as event_count
            FROM events
            GROUP BY month
            ORDER BY month
        ''')
        for row in cursor.fetchall():
            print(f"  {int(row[0])}月: {row[1]}件")

        # 地域別のイベント数を表示
        print("\n地域別イベント数:")
        cursor.execute('''
            SELECT area, COUNT(*) as event_count
            FROM events
            GROUP BY area
            ORDER BY event_count DESC
        ''')
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}件")

    except sqlite3.IntegrityError as e:
        print(f"❌ エラー: データの重複があります。{e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_sample_events()
