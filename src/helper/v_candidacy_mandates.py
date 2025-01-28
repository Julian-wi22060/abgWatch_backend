from flask import Blueprint, jsonify, request
from helper.db_connection import get_db_connection

# Set blueprint for 'VIEW v_candidacy_mandates'
v_cm_bp = Blueprint("v_candidacy_mandates", __name__)


@v_cm_bp.route("/", methods=["GET"])
def get_v_candidacy_mandates():
    """
    Retrieves data from the 'mart.v_candidacy_mandates' view with optional grouping by party.
    Parameters:
        - grouped: Query parameter to specify grouping (0 = not grouped, 1 = grouped).
    Workflow:
        1. Read 'grouped' parameter from the query string.
        2. Dynamically adjust the SQL query based on the parameter.
        3. Execute the SQL query and fetch results.
        4. Return the results as JSON.
    Returns:
        - JSON array of objects on success.
        - JSON error response on failure.
    """
    grouped = request.args.get("grouped", "0")
    conn = None

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            if grouped == "1":
                # Query with grouping by party
                cur.execute("""
                    SELECT 
                        party_id,
                        politician_party_name,
                        COUNT(*) AS total_mandates
                    FROM mart.v_candidacy_mandates
                    GROUP BY party_id, politician_party_name;
                """)
            else:
                # Default query without grouping
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
