from datetime import datetime

def datetime_converter(integer):
    # Given integer representing a Unix timestamp
    timestamp = integer

    # Convert Unix timestamp to a datetime object
    dt_object = datetime.utcfromtimestamp(timestamp)

    # Format the datetime object as a string (adjust format as needed)
    formatted_datetime = dt_object.strftime('%Y-%m-%d')
    return formatted_datetime

def day_extractor(x):
    day = x.split(" ")[0]
    return int(day)