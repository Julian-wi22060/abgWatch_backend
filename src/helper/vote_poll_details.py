from flask import Blueprint, Response, request
from helper.db_connection import get_db_connection
import json
from datetime import date, datetime

# Set blueprint for 'VIEW vote_poll_details'
vote_poll = Blueprint("vote_poll_details", __name__)


def custom_json_serializer(obj):
    """
    Custom serializer function for handling non-serializable objects like dates.
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


@vote_poll.route("/", methods=["GET"])
def get_vote_poll_details():
    """
    Retrieves data from the 'mart.vote_poll_details' view with optional grouping by poll_id.
    """
    grouped = request.args.get("grouped", "0")
    conn = None

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            if grouped == "1":
                # Query to group by poll_id, count vote_state occurrences, include poll_date and poll_description
                cur.execute("""
                    SELECT 
                        poll_id,
                        vote_state,
                        COUNT(*) AS state_count,
                        MIN(field_poll_date) AS poll_date,
                        MIN(poll_description)
                    FROM mart.vote_poll_details
                    GROUP BY poll_id, vote_state
                    ORDER BY poll_id, vote_state;
                """)
                rows = cur.fetchall()

                # Restructure results into a dictionary with poll_id as the key
                data = {}
                for row in rows:
                    poll_id = row[0]
                    vote_state = row[1]
                    state_count = row[2]
                    poll_date = row[3]
                    poll_description = row[4]

                    if poll_id not in data:
                        data[poll_id] = {"poll_date": poll_date, "vote_states": {}, "poll_description": poll_description}
                    data[poll_id]["vote_states"][vote_state] = state_count

            elif grouped == "2":
                # Query to group by poll_id, count vote_state occurrences and include poll_date
                cur.execute("""
                    SELECT 
                        poll_id,
                        vote_state,
                        COUNT(*) AS state_count,
                        MIN(field_poll_date) AS poll_date
                    FROM mart.vote_poll_details
                    GROUP BY poll_id, vote_state
                    ORDER BY poll_id, vote_state;
                """)
                rows = cur.fetchall()

                # Restructure results into a dictionary with poll_id as the key
                data = {}
                for row in rows:
                    poll_id = row[0]
                    vote_state = row[1]
                    state_count = row[2]
                    poll_date = row[3]

                    if poll_id not in data:
                        data[poll_id] = {"poll_date": poll_date, "vote_states": {}}
                    data[poll_id]["vote_states"][vote_state] = state_count

            else:
                # Default query without grouping, includes vote_state directly
                cur.execute("""
                    SELECT 
                        vote_id,
                        politician_id,
                        vote_state,
                        poll_id,
                        field_poll_date,
                        poll_description
                    FROM mart.vote_poll_details
                    ORDER BY field_poll_date ASC;
                """)
                columns = [desc[0] for desc in cur.description]
                rows = [dict(zip(columns, row)) for row in cur.fetchall()]
                data = {row['vote_id']: row for row in rows}

    # Handle exceptions
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False, indent=1, sort_keys=True),
            status=500,
            mimetype="application/json; charset=utf-8"
        )
    finally:
        if conn is not None:
            conn.close()

    # Serialize data using the custom JSON serializer
    return Response(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True, default=custom_json_serializer),
        mimetype="application/json; charset=utf-8"
    )
