from flask import Blueprint, jsonify
from helper.db_connection import get_db_connection

v_cm_bp = Blueprint("v_candidacy_mandates", __name__)

@v_cm_bp.route("/", methods=["GET"])
def get_v_candidacy_mandates():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    candidacy_mandate_id,
                    parliament_id,
                    parliament_name_short,
                    parliament_name_long,
                    parliament_period_id,
                    start_date_period,
                    end_date_period,
                    politician_id,
                    politician_first_name,
                    politician_last_name,
                    politician_sex,
                    politician_year_of_birth,
                    politician_education,
                    party_id,
                    politician_party_name
                FROM mart.v_candidacy_mandates;
            """)
            rows = cur.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()
    return jsonify(rows)
