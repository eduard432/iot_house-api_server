import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.config = {
            "host": "db-iot-house.crq6g0k0ir55.us-east-2.rds.amazonaws.com ",
            "user": "admin",
            "password": "edufelipecamila",
            "database": "iot_house"
        }

    def connect(self):
        return mysql.connector.connect(**self.config)

db = Database()
