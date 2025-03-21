"""A small example of a Kafka consumer."""
import os
import json
import argparse
import logging
from datetime import datetime, time
from dotenv import load_dotenv
from confluent_kafka import Consumer
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection, cursor
import psycopg2


load_dotenv('.env')


def create_consumer() -> 'consumer':
    """Creates a Kafka consumer"""
    return Consumer({
        "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
        "group.id": os.environ["GROUP"],
        "auto.offset.reset": "latest",
        'security.protocol': os.environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': os.environ["SASL_MECHANISM"],
        'sasl.username': os.environ["USERNAME"],
        'sasl.password': os.environ["PASSWORD"]
    })


def get_connection() -> connection:
    """Gains connection to the rds"""
    return psycopg2.connect(
        user=os.environ["DATABASE_USERNAME"],
        password=os.environ["DATABASE_PASSWORD"],
        host=os.environ["DATABASE_IP"],
        port=os.environ["DATABASE_PORT"],
        database=os.environ["DATABASE_NAME"]
    )


def get_cursor(conn: connection) -> cursor:
    """Produces a cursor based off the connection made"""
    return conn.cursor(cursor_factory=RealDictCursor)


def logger_setup(output_filename: str) -> tuple['logger', 'logger']:
    """logging configuration setup"""
    # Logger for errors (file)
    file_logger = logging.getLogger("file_logger")
    # Only handle ERROR messages and above
    file_logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler(f"{output_filename}")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_logger.addHandler(file_handler)

    # Logger for info (console)
    console_logger = logging.getLogger("console_logger")
    # Only handle INFO messages and above
    console_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    console_logger.addHandler(console_handler)

    return file_logger, console_logger


def key_values(output: dict) -> dict:
    """Extracts key values from the message"""
    site = output.get('site', 'site')
    val = output.get('val', 'val')
    at = output.get('at', 'at')
    incident_type = output.get('type', 'incident_type')
    return {"at": at, "site": site, "val": val, "incident_type": incident_type}


def key_validator(message_dict: dict) -> str:
    """Finds the keys that are missing from the message"""
    missing_keys = ''
    for key, val in message_dict.items():
        if val == 'incident_type' and message_dict["val"] == -1:
            missing_keys += key + ", "
        elif key == val and key != 'incident_type':
            missing_keys += key + ", "
    if len(missing_keys) == 0:
        return missing_keys
    return missing_keys[:-2]


def is_between_time(dt: datetime) -> bool:
    """Checks whether the date time is between the opening times"""
    start_time = time(8, 45)
    end_time = time(18, 15)
    return start_time <= dt.time() <= end_time


# pylint: disable=bare-except
def value_validator(message_dict: dict) -> str:
    """Finds any invalid values in the message"""
    invalid_keys = ''
    if message_dict["site"] not in ['0', '1', '2', '3', '4', '5']:
        invalid_keys += f"site:{message_dict['site']}, "
    if message_dict["val"] not in [-1, 0, 1, 2, 3, 4]:
        invalid_keys += f"val:{message_dict['val']}, "
    if message_dict["val"] == -1 and message_dict['incident_type'] not in [0, 1]:
        invalid_keys += f"type:{message_dict['incident_type']}, "
    try:
        date = datetime.fromisoformat(message_dict["at"])
        if is_between_time(date) is False:
            invalid_keys += f"at:{message_dict['at']}, "
    except:
        invalid_keys += f"at:{message_dict['at']}, "

    if len(invalid_keys) == 0:
        return invalid_keys
    return invalid_keys[:-2]


def message_formatter(values: dict) -> dict:
    """Formats each message: site, val and type so they resemble primary keys in the data base"""
    values["site"] = int(values["site"])
    date = datetime.fromisoformat(values["at"])
    values["at"] = date.strftime('%Y-%m-%d %H:%M:%S+00')

    if values["incident_type"] != "incident_type":
        values["type"] = values["incident_type"]
        if values["type"] == 0:
            values['type'] = 2

    values.pop("incident_type")

    if values["site"] == 0:
        values['site'] = 6

    if values["val"] == 0:
        values['val'] = 5

    return values


def load_to_db(formatted_message: dict) -> None:
    """Loads valid messages to database"""
    conn = get_connection()
    cur = get_cursor(conn)
    if formatted_message['val'] > -1:
        cur.execute(
            """INSERT INTO rating_interaction (exhibition_id, rating_id, event_at)
            VALUES (%s, %s, %s);""",
            (formatted_message['site'], formatted_message['val'], formatted_message['at']))
    else:
        cur.execute(
            """INSERT INTO request_interaction (exhibition_id, request_id, event_at)
            VALUES (%s, %s, %s);""", (formatted_message['site'], formatted_message['type'],
                                      formatted_message['at']))
    cur.close()
    conn.commit()
    conn.close()


def consume_messages(cons: Consumer, log_destination: str, file_logger, console_logger) -> None:
    """Processes Kafka messages, only logging valid ones."""
    while True:
        msg = cons.poll(1)
        if msg:
            output = json.loads(msg.value().decode())
            values = key_values(output)
            missing = key_validator(values)
            invalid = value_validator(values)

            if log_destination == 'file':
                error_logger_type = file_logger
            else:
                error_logger_type = console_logger

            if len(missing) > 0:
                console_logger.info(output)
                error_logger_type.error("%s Invalid missing %s key(s)",
                                        output, missing)
            elif len(invalid) > 0:
                console_logger.info(output)
                error_logger_type.error(
                    "%s Invalid values %s", output, invalid)
            else:

                formatted_message = message_formatter(values)
                load_to_db(formatted_message)
                console_logger.info(output)


def cli() -> tuple[str, str]:
    """Takes in inputs from the command line to help run the script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log_destination", default="terminal",
                        help="Choose to log to a 'file' or 'terminal'")
    parser.add_argument("-t", "--topic", default="lmnh",
                        help="Choose the consumers topic 'lmnh' is the default")
    parser.add_argument("-f", "--filename", default="errors.txt",
                        help="Choose an output filename - default is errors.txt")
    args = parser.parse_args()
    log_destination = args.log_destination
    topic = args.topic
    output_filename = args.filename
    return [topic, log_destination, output_filename]


def main() -> None:
    """Main function that the scripts runs off"""
    arguments = cli()
    file_logger, console_logger = logger_setup(arguments[2])
    consumer = create_consumer()
    consumer.subscribe([arguments[0]])
    consume_messages(consumer, arguments[1], file_logger, console_logger)


if __name__ == "__main__":
    main()
