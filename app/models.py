from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# DBモデルのクラス
class InfluencerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.String(64), index=True)
    post_id = db.Column(db.String(64))
    shortcode = db.Column(db.String(64))
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    thumbnail = db.Column(db.Text)  # URLが長いため、データ型をTextに変更
    text = db.Column(db.Text, nullable=True)  # 欠損値処理のため、NULLを許可
    post_date = db.Column(db.DateTime)
