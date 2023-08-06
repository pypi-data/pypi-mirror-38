import argparse
import hashlib
from base64 import standard_b64encode
from datetime import datetime

from MySQLdb import connect


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Insert the firmware binary code into the DB"
    )
    parser.add_argument(
        '--host',
        type=str,
        required=False,
        help='DB host',
        default='127.0.0.1'
    )
    parser.add_argument(
        '--port',
        required=False,
        type=int,
        help='DB port',
        default='3306'
    )
    parser.add_argument(
        '--db',
        required=False,
        type=str,
        help='DB name',
        default='firmwares'
    )
    parser.add_argument(
        '--username',
        required=False,
        type=str,
        help='DB username',
        default='root'
    )
    parser.add_argument(
        '--password',
        required=False,
        type=str,
        help='DB password',
        default='root'
    )
    parser.add_argument(
        '--binary_file',
        required=False,
        type=str,
        help='Binary file',
        default='testing_c_project'
    )

    return parser.parse_args()


def connect_to_db(host, port, db, username, password):
    return connect(
        host=host,
        user=username,
        port=port,
        passwd=password,
        db=db
    )


def get_binary_file(binary_file):
    result = b''
    
    with open(binary_file, 'rb') as f:
        for line in f:
            result += line
    
    return result


def encode_file(raw_file):
    return standard_b64encode(raw_file)


def encode_md5(base64_encoded):
    md5 = hashlib.md5()
    md5.update(base64_encoded)
    return md5.hexdigest()


def insert_firmware_version(db, base64_encoded):
    version = datetime.now().strftime("%Y.%m.%d.%H.%M")
    checksum = encode_md5(base64_encoded)
    cursor = db.cursor()

    cursor.execute(
        """
          INSERT INTO platform_firmware (version, firmware, checksum) 
          VALUES (%s, %s, %s)
        """,
        (version, base64_encoded, checksum)
    )
    db.commit()


def insert_firmware(parameters):
    raw_file = get_binary_file(parameters.binary_file)
    base64_encoded = encode_file(raw_file)
    db = connect_to_db(
        host=parameters.host,
        port=parameters.port,
        db=parameters.db,
        username=parameters.username,
        password=parameters.password
    )
    insert_firmware_version(db, base64_encoded)


def main():
    insert_firmware(parse_arguments())
