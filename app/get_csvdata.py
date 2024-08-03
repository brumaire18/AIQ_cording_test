from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from io import StringIO
import pandas as pd
import requests
from config import Config
from models import db, InfluencerData
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


app = create_app()


# Google DriveのURLからCSVデータを取得する
def download_csv_from_google_drive(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode('utf-8')


# 取得したCSVデータをMySQLに格納する
def import_csv_to_db(csv_content):
    data = StringIO(csv_content)
    df = pd.read_csv(data)
    df = df.where(pd.notnull(df), None) # 欠損地の処理

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
    with app.app_context():
        db.create_all()  # テーブルが存在しない場合、作成する
        file_id = Config.CSV_FILE_ID
        csv_content = download_csv_from_google_drive(file_id)
        import_csv_to_db(csv_content)
