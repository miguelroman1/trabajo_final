import mysql.connector
from mysql.connector import Error

class Database:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',  # Tu contraseña de MySQL
                    database='sistema_calificaciones'
                )
            return self._connection
        except Error as e:
            print(f"Error de conexión: {e}")
            return None
    
    def get_cursor(self, dictionary=True):
        connection = self.connect()
        if connection:
            return connection.cursor(dictionary=dictionary)
        return None
    
    def commit(self):
        if self._connection and self._connection.is_connected():
            self._connection.commit()
    
    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None