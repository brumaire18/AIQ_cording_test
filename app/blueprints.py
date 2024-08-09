from api.top_liked_influencers import bp as top_liked_influencers_bp


# 各種APIのエンドポイントを記述
def get_blueprints():
    blueprints = [
        (top_liked_influencers_bp, '/api')
    ]
    return blueprints
