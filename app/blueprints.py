from app.api.top_liked_influencers import bp as top_liked_influencers_bp
from app.api.top_commented_influencers import bp as top_commented_influencers_bp
from app.api.top_nouns_by_influencer import bp as top_nouns_by_influencer_bp

blueprints = [
    (top_liked_influencers_bp, '/api'),
    (top_commented_influencers_bp, '/api'),
    (top_nouns_by_influencer_bp, '/api')
]