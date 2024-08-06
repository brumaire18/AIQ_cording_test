from flask import Blueprint, request, jsonify
from app.models import db, InfluencerData

bp = Blueprint('top_liked_influencers', __name__)

@bp.route('/top-liked-influencers', methods=['GET'])
def get_top_liked_influencers():
    try:
        n = int(request.args.get('n', 10))
        results = db.session.query(
            InfluencerData.influencer_id,
            db.func.avg(InfluencerData.likes).label('average_likes')
        ).group_by(InfluencerData.influencer_id).order_by(db.desc('average_likes')).limit(n).all()

        influencers = [{'influencer_id': result.influencer_id, 'average_likes': result.average_likes} for result in results]
        return jsonify(influencers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
