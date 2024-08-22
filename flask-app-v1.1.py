import pika, logging
from flask import Flask, render_template, request, jsonify, make_response
from jsonschema import validate
from multiprocessing import Value


app = Flask(__name__)

schema = {
    "properties": {
        "firstname": {
            "type": "string"
            },
        "lastname": {
            "type": "string",
            }
        }
    }

counter = Value('i', 0)

@app.route('/')
def hallo_everynyan():
     return "Hallo everynyan! How are you? I'm fine, thank you"


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

@app.route('/metrics', methods=['GET'])
def get_metrics():
    with counter.get_lock():
        counter.value += 1
        out = counter.value
        print('there are ', str(out), "requests now", flush=True)
    return 'http_requests_total '+str(out)
    #return jsonify(http_requests_total=out)

@app.route('/', methods=["POST"])
def index():
    if validate(request.json, schema)==False:
        logging.error("TypeError in requestfile: ", request.json)
        return jsonify({"error": "Wrong data type!"}), 400
    if request.method == "POST":
        try:
            connection = pika.BlockingConnection(
                 pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='db_insert')
            firstname = request.json["firstname"]
            lastname = request.json["lastname"]
            data_for_db = firstname+ ' ' + lastname
            logging.info(f"Your data is {data_for_db}")
            print('Your data is: ', data_for_db)
            channel.basic_publish(exchange='', routing_key='db_insert', body=data_for_db)
            print(" [x] Sent 'Some data for your db!'", data_for_db)
            connection.close()
            logging.info("Data has been inserted successfully: ")
            return 'You successfully inserted your data! \n'
        except Exception as ex:
            return ex
    return render_template('index.html')


if __name__ == '__main__':
       app.run(debug=True)