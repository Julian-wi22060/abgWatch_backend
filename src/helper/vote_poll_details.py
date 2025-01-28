from flask import Blueprint, jsonify
from helper.db_connection import get_db_connection

# Set blueprint for 'VIEW vote_poll_details'
vote_poll = Blueprint("vote_poll_details", __name__)


@vote_poll.route("/", methods=["GET"])
def get_vote_poll_details():
    """
    Retrieves all data from the 'mart.vote_poll_details' view and returns it as a JSON array.
    Workflow:
        1. Establish a connection to the database.
        2. Execute a SELECT query on the 'mart.vote_poll_details' view.
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
