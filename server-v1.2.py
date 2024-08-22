import pika, sys, os, logging, mysql.connector, time

def main():
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    
    channel = connection.channel()

    channel.queue_declare(queue='db_insert')
    
    def callback(ch, method, properties, body):
        try:
            
            #global firstName, lastName

            print(f" [x] Received {body}")
            
            db_data=body.decode().split(' ')
    
            logging.info(f"Recieved some data {db_data}!")
    
            print("Recieved some data: ", db_data)
    
            firstName, lastName = db_data[0], db_data[1]

            print(firstName, lastName)

            table ="CREATE TABLE IF NOT EXISTS test_table(FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20));"

            cnx = mysql.connector.connect(user='root', password='', host = '127.0.0.1', database='test_db')

            logging.info("You successfully connected to MySQL database!") 

            print("You successfully connected to MySQL database!")  
    
            cursor = cnx.cursor()

            cursor.execute("USE test_db;")

            print("database test_db has been used")

            cursor.execute(table)

            logging.info("TABLE test_table has been created or picked")
    
            cursor.execute("INSERT INTO test_table(FIRST_NAME, LAST_NAME) VALUES (%s, %s)", (firstName, lastName))
    
            cnx.commit()

            print("Insert in test_table has been commited")

            cnx.close()
    
            logging.info("Data has been inserted successfully!")
        
        finally:

            return 'Info = ', db_data

    channel.basic_consume(queue='db_insert', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.start_consuming()
    
    #table ="CREATE TABLE IF NOT EXISTS test_table(FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20));"

    #time.sleep(5)
        
    #cnx = mysql.connector.connect(user='root', password='', host = '127.0.0.1', database='test_db')
    
    #logging.info("You successfully connected to MySQL database!")   
    
    #cursor = cnx.cursor()
    
    #cursor.execute("USE test_db;")

    #logging.info("USE test_db;")
    
    #cursor.execute(table)

    #logging.info("CREATE TABLE IF NOT EXISTS test_table(FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20));")
    
    #cursor.execute("INSERT INTO test_table(FIRST_NAME, LAST_NAME) VALUES (%s, %s)", (firstName, lastName))
    
    #cnx.commit()

    #cnx.close()
    
    #logging.info("Data has been inserted successfully!")


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