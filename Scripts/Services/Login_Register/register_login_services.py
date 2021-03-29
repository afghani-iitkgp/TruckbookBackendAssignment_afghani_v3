import psycopg2
from Scripts.Services.DatabaseConnection.crud_truckbook_db_v1 import TruckBookOperationCRUD


class User:

    def __init__(self, phone_number, pass_hash):
        self.phone_number = phone_number
        self.pass_hash = pass_hash

        self.crud_obj = TruckBookOperationCRUD()


    def create_tables(self):
        self.crud_obj.create_tables()

    def new_user_signup(self):
        status = self.crud_obj.insert_new_user(self.phone_number, self.pass_hash)
        return status

    def old_user_login(self, phone_numer):
        row = self.crud_obj.filter_by(phone_numer)
        return row










