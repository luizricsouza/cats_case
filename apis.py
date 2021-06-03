
import sqlite3
import settings
import datetime
import time
import logging

from flask import Flask
from flask import jsonify
from flask import g
from flask.globals import request
from rfc3339 import rfc3339

db_file = settings.db_file

FORMAT = '%(levelname)s %(name)s %(message)s'
logging.basicConfig(filename='app.log', level=logging.INFO, format=FORMAT)

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if (
        request.path == "/favicon.ico"
        or request.path.startswith("/static")
        or request.path.startswith("/admin/static")
    ):
        return response

    now = time.time()
    duration = round(now - g.start, 6)
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    params = dict(request.args)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=False)
    request_id = request.headers.get("X-Request-ID", "")

    log_params = {
        "time": timestamp,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration": duration,
        "ip": ip_address,
        "host": host,
        "params": params,
        "request_id": request_id,
    }

    parts = []
    for name, value in log_params.items():
        part = "{}={}".format(name, value)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response


@app.route('/cats_breeds', methods=['GET'])
def get_cats_breeds():
    temperament = request.args.get('temperament') if request.args.get('temperament') is not None else ''
    origin = request.args.get('origin') if request.args.get('origin') is not None else '%'

    json_breeds = {}

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    breeds = []

    for breed in cursor.execute('''SELECT breed_name FROM breeds
                                    WHERE origin LIKE "{}" AND temperament LIKE "%{}%"
                                    ORDER BY breed_name'''.format(origin, temperament)):
        breeds.append(breed[0])

    json_breeds['breeds'] = breeds

    conn.close()

    return jsonify(json_breeds)

@app.route('/breed_info', methods=['GET'])
def get_breed_info():
    breed_name = request.args.get('breed_name')
    json_breeds = {}

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM breeds WHERE breed_name = "{}"'.format(breed_name))

    breed_info = cursor.fetchone() 

    if breed_info is not None:
        json_breeds['id'] = breed_info[0]
        json_breeds['breed_name'] = breed_info[1]
        json_breeds['temperament'] = breed_info[2]
        json_breeds['origin'] = breed_info[3]
        json_breeds['description'] = breed_info[4]

        conn.close()

        return jsonify(json_breeds), 200
    else:
        conn.close()
        return 'breed not found', 404

if __name__ == '__main__':
    app.run()