from flask import Blueprint, jsonify, request
from helper.db_connection import get_db_connection

# Set blueprint for 'VIEW vote_poll_details'
vote_poll = Blueprint("vote_poll_details", __name__)

@vote_poll.route("/", methods=["GET"])
def get_vote_poll_details():
    """
    Retrieves data from the 'mart.vote_poll_details' view with optional grouping by poll_id.
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
                # Query with grouping by poll_id
                cur.execute("""
                    SELECT 
                        poll_id,
                        COUNT(*) AS total_votes,
                        MIN(field_poll_date)
                    FROM mart.vote_poll_details
                    GROUP BY poll_id;
                """)
            else:
                # Default query without grouping
                cur.execute("""
                    SELECT 
                        vote_id,
                        politician_id,
                        vote_state,
                        poll_id,
                        field_poll_date,
                        poll_description
                    FROM mart.vote_poll_details;
                """)

            rows = cur.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn is not None:
            conn.close()

    return jsonify(rows)
