from flask import Blueprint, jsonify
from helper.db_connection import get_db_connection

# Set blueprint for 'VIEW v_candidacy_mandates'
v_cm_bp = Blueprint("v_candidacy_mandates", __name__)


@v_cm_bp.route("/", methods=["GET"])
def get_v_candidacy_mandates():
    """
    Retrieves all data from the 'mart.v_candidacy_mandates' view and returns it as a JSON array.
    Workflow:
        1. Establish a connection to the database.
        2. Execute a SELECT query on the 'mart.v_candidacy_mandates' view.
        3. Return the retrieved rows as a JSON array.
        4. Close the database connection, regardless of whether an exception occurred.
    Returns:
        - On success:
            A JSON array of objects
        - On error:
            A JSON response with an "error" key containing the error message, and
            an HTTP status code of 500.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    politician_id,
                    politician_first_name,
                    politician_last_name,
                    politician_sex,
                    politician_year_of_birth,
                    politician_education,
                    party_id,
                    politician_party_name,
                    parliament_id,
                    parliament_name_short,
                    parliament_name_long,
                    parliament_period_id,
                    start_date_period,
                    end_date_period
                FROM mart.v_candidacy_mandates;
            """)
            rows = cur.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()
    return jsonify(rows)
