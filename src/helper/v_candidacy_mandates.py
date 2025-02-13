from flask import Blueprint, Response, request
from helper.db_connection import get_db_connection
import json
from datetime import date, datetime

# Set blueprint for 'VIEW v_candidacy_mandates'
v_cm_bp = Blueprint("v_candidacy_mandates", __name__)

def custom_json_serializer(obj):
    """
    Custom serializer function for handling non-serializable objects like dates.
    """
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@v_cm_bp.route("/", methods=["GET"])
def get_v_candidacy_mandates():
    """
    Retrieves data from the 'mart.v_candidacy_mandates' view with optional grouping by party or politician_party_name.
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
                rows = cur.fetchall()

                # Restructure results into a dictionary with party_id as key
                data = {
                    row[0]: {
                        "party_name": row[1],
                        "total_mandates": row[2]
                    } for row in rows
                }
            elif grouped == "2":
                # Query grouping by politician_party_name
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
                columns = [desc[0] for desc in cur.description]

                data = {}
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    party_name = row_dict.pop("politician_party_name")
                    party_id = row_dict["party_id"]

                    if party_name not in data:
                        data[party_name] = {
                            "party_id": party_id,
                            "politicians": {}
                        }

                    data[party_name]["politicians"][row_dict["politician_id"]] = row_dict
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
                columns = [desc[0] for desc in cur.description]
                data = {
                    row[0]: dict(zip(columns, row)) for row in rows
                }

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
