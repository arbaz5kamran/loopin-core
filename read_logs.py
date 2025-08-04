# read_logs.py
from flask import Blueprint, request, jsonify, session
from extensions import db
from models import ReadLog
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('read_logs', __name__)

@bp.route('/mark_read', methods=['POST'])
def mark_read():
    data = request.get_json() or {}
    update_id = data.get('update_id')
    guest_name = (data.get('reader_name') or '').strip()
    user_id = session.get("user_id")  # ✅ Only check session

    if not update_id:
        return jsonify(status='error', message='Missing update_id'), 400

    if not user_id and not guest_name:
        return jsonify(status='error', message='Missing guest_name'), 400

    try:
        # Prevent duplicate read logs for same user or guest on same update
        exists = db.session.query(ReadLog.id).filter_by(
            update_id=update_id,
            user_id=user_id if user_id else None,
            guest_name=None if user_id else guest_name
        ).first()

        if exists:
            # Still return current read count
            read_count = db.session.query(func.count(ReadLog.id)).filter_by(update_id=update_id).scalar()
            return jsonify(status='success', read_count=read_count), 200

        log = ReadLog(
            update_id=update_id,
            user_id=user_id if user_id else None,
            guest_name=None if user_id else guest_name,
            timestamp=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()

        read_count = db.session.query(func.count(ReadLog.id)).filter_by(update_id=update_id).scalar()
        return jsonify(status='success', read_count=read_count), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(status='error', message=str(e)), 500
