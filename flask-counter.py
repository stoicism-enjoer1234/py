from flask import Flask, jsonify
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def index():
    with counter.get_lock():
        counter.value += 1
        out = counter.value
        print(f'There are {out} requests now!', flush=True)
    return jsonify(count=out)

app.run()