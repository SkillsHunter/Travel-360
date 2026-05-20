import pandas as pd

FLIGHT_DATA = pd.read_csv("data/flights.csv")


def get_flight_data(route):

    flight = FLIGHT_DATA[
        FLIGHT_DATA["route"] == route
    ]

    if flight.empty:
        return None

    return flight.iloc[0].to_dict()


def green_message(co2):

    if co2 < 100:
        return "Low-emission flight option"

    elif co2 < 250:
        return "Moderate carbon footprint"

    return "High carbon footprint"
