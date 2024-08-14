import pika, logging
from flask import Flask, render_template, request, jsonify
from jsonschema import validate

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


@app.route('/')
def hallo_everynyan():
     return "Hallo everynyan! How are you? I'm fine, thank you"


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


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
       app.run(debug=True, host = "0.0.0.0")