from sqlalchemy import text


def find_pooling_matches(db):

    query = text("""

    WITH AirportPairs AS (

        SELECT

            Person_A.request_id AS ID_A,
            Person_A.company_id AS Company_A,
            Person_A.request_time AS Time_A,

            Person_B.request_id AS ID_B,
            Person_B.company_id AS Company_B,
            Person_B.request_time AS Time_B,

            Person_A.airport_code

        FROM travel_requests AS Person_A

        JOIN travel_requests AS Person_B

        ON Person_A.airport_code = Person_B.airport_code

    ),

    ValidPartners AS (

        SELECT *
        FROM AirportPairs

        WHERE Company_A < Company_B

    )

    SELECT *

    FROM ValidPartners

    WHERE

    ABS(
        EXTRACT(
            EPOCH FROM (Time_A - Time_B)
        ) / 60
    ) <= 30

    """)

    result = db.execute(query)

    rows = result.fetchall()

    return rows
