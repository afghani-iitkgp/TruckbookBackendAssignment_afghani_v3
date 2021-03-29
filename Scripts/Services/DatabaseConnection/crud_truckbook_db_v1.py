import psycopg2
from Scripts.Utility import utils
from Constants import const


class TruckBookOperationCRUD:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=utils.configuration["postgres_credentials"]["host"],
            database=utils.configuration["postgres_credentials"]["database"],
            user=utils.configuration["postgres_credentials"]["user"],
            password=utils.configuration["postgres_credentials"]["password"]
        )

    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS users_table (
                _id SERIAL PRIMARY KEY,
                phone_number VARCHAR(255) NOT NULL UNIQUE,
                pass_hash VARCHAR(255) NOT NULL
            )
            """,

            """ 
            CREATE TABLE IF NOT EXISTS stations_table (
                    _id SERIAL PRIMARY KEY,
                    station_name VARCHAR(255) NOT NULL UNIQUE,
                    line_color VARCHAR(255) NOT NULL,
                    is_intersection_node BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        try:
            # connect to the PostgreSQL server
            cur = self.conn.cursor()

            # create table one by one
            for command in commands:
                cur.execute(command)

            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()



    def insert_new_user(self, phone_number, pass_hash):
        """ insert a new vendor into the vendors table """
        try:
            # create a new cursor
            cur = self.conn.cursor()


            sql_new_user = """INSERT INTO users_table (phone_number, pass_hash) VALUES(%s, %s) RETURNING phone_number;"""

            # execute the INSERT statement
            cur.execute(sql_new_user, (phone_number, pass_hash))

            # get the generated id back
            phone_number_new = cur.fetchone()[0]

            # commit the changes to the database
            self.conn.commit()

            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            if isinstance(error, psycopg2.errors.UniqueViolation):
                return 0
            else:
                utils.logger.error("--error--" + str(error))
        finally:
            if self.conn is not None:
                self.conn.close()

        return 1



    def insert_vendor_list(self, vendor_list):
        """ insert multiple vendors into the vendors table  """
        sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"

        # connect to the PostgreSQL database
        conn = self.conn
        try:
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.executemany(sql, vendor_list)
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def update_vendor(self, vendor_id, vendor_name):
        """ update vendor name based on the vendor id """
        sql = """ UPDATE vendors
                    SET vendor_name = %s
                    WHERE vendor_id = %s"""
        conn = self.conn
        updated_rows = 0
        try:
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(sql, (vendor_name, vendor_id))
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows


    def filter_by(self, phone_number):
        sql_query_filter = "SELECT * FROM {0} WHERE phone_number='{1}'".format(const.users_table, phone_number)
        try:
            # create a new cursor
            cur = self.conn.cursor()
            cur.execute(sql_query_filter)
            _rows = cur.fetchall()

            return _rows
        except Exception as e:
            print(e)

