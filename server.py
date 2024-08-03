import pika, sys, os, MySQLdb, logging


def main():
    logging.basicConfig(level=logging.INFO, filename="app_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
    db=MySQLdb.connect("127.0.0.1", "root", "", "test_db") # 1 was "localhost"
    logging.info("You successfully connected to MySQL database!")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    
    channel = connection.channel()

    channel.queue_declare(queue='db_insert')

    
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        db_data=body.decode()
        db_data = db_data.split(' ')
        logging.info(f"Recieved some data {db_data}!")
        print("Recieved some data: ", db_data)
        firstName = db_data[0]
        lastName = db_data[1]
        cur = db.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        cur.connection.commit()
        cur.close()
        logging.info("Data has been inserted successfully!")
        return 'You successfully inserted your data!'
    
    
    channel.basic_consume(queue='db_insert', on_message_callback=callback, auto_ack=True)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt", exc_info=True)
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            logging.error("SystemExit", exc_info=True)
            os._exit(0)