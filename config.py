import os
from dotenv import load_dotenv

# .envに取得するCSVのファイルIDおよびデータベースへの接続URLを格納
# .envはパブリックに配置しないため、別途設定の必要がある、
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FILE_ID = os.getenv('CSV_FILE_ID')  # 取得するCSVのファイルID
