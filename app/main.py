import sys
import os
# この位置に書かないと、「from config import Config」が動かない
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from flask import Flask
from config import Config
from models import db, InfluencerData
from io import StringIO
import pandas as pd
import requests
from datetime import datetime
from blueprints import get_blueprints


# MySQLサーバーが利用可能になるまで待機する関数
def wait_for_mysql():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    while True:
        try:
            # DBインスタンスが生成されているか確認を行う
            conn = engine.connect()
            conn.execute(text("SELECT 1"))
            conn.close()
            break
        except OperationalError:
            print("Waiting for MySQL to be ready...")
            time.sleep(2)


# Flaskアプリを起動
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def home():
        return "Flask API is running!"

    with app.app_context():
        for bp, url_prefix in get_blueprints():
            app.register_blueprint(bp, url_prefix=url_prefix)

    return app


# データベースとテーブルの文字セットをUTF-8に設定
def set_utf8_charset():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        conn.execute(text("ALTER DATABASE Influencer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.execute(text("ALTER TABLE influencer_data CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))


# GoogleドライブからCSVファイルをダウンロード
def download_csv_from_google_drive(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode('utf-8')


# ダウンロードしたCSVのデータをDBに格納
def import_csv_to_db(csv_content):
    data = StringIO(csv_content)
    df = pd.read_csv(data)
    df = df.where(pd.notnull(df), None)  # 欠損値の処理

    for _, row in df.iterrows():
        influencer_data = InfluencerData(
            influencer_id=row['influencer_id'],
            post_id=row['post_id'],
            shortcode=row['shortcode'],
            likes=row['likes'],
            comments=row['comments'],
            thumbnail=row['thumbnail'],
            text=row['text'],
            post_date=datetime.strptime(row['post_date'], '%Y-%m-%d %H:%M:%S')
        )
        db.session.add(influencer_data)
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        wait_for_mysql()
        set_utf8_charset()  # 文字セットを設定
        db.create_all()  # テーブルが存在しない場合、作成する
        file_id = Config.CSV_FILE_ID
        csv_content = download_csv_from_google_drive(file_id)
        import_csv_to_db(csv_content)
    app.run(host='0.0.0.0', port=5000, debug=True)
