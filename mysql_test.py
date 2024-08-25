import sys, os, logging, mysql.connector, time

table ="CREATE TABLE IF NOT EXISTS test_table(FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20));"
time.sleep(20)
def main():
    logging.basicConfig(level=logging.INFO, filename="app_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
    cnx = mysql.connector.connect(user='root', password='', host = '127.0.0.1', database='test_db')
    logging.info("You successfully connected to MySQL database!")
    try:
        firstName = 'randomname'
        lastName = 'randomsurname'
        cursor = cnx.cursor()
        cursor.execute("Use test_db;")
        cursor.execute(table)
        cursor.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        cnx.commit()
        logging.info("Data has been inserted successfully!")
    finally:
        cnx.close()
        


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