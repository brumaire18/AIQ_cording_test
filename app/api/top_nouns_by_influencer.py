from flask import Blueprint, request, jsonify
from app.models import db, InfluencerData
import MeCab
from collections import Counter

bp = Blueprint('top_nouns_by_influencer', __name__)


def extract_nouns(text):
    tagger = MeCab.Tagger()
    nouns = []
    node = tagger.parseToNode(text)
    while node:
        if node.feature.split(",")[0] == "名詞":
            nouns.append(node.surface)
        node = node.next
    return nouns


@bp.route('/top-nouns-by-influencer/<influencer_id>', methods=['GET'])
def get_top_nouns_by_influencer(influencer_id):
    try:
        n = int(request.args.get('n', 10))
        texts = db.session.query(InfluencerData.text).filter_by(influencer_id=influencer_id).all()

        all_nouns = []
        for text in texts:
            if text.text:
                all_nouns.extend(extract_nouns(text.text))

        noun_counts = Counter(all_nouns)
        top_nouns = noun_counts.most_common(n)
        top_nouns_list = [{'noun': noun, 'count': count} for noun, count in top_nouns]

        return jsonify(top_nouns_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
