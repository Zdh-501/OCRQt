import json
import pyodbc

def dbConnect():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        connection_string = f'DRIVER={{{config["driver"]}}};' \
                            f'SERVER={config["server"]};' \
                            f'DATABASE={config["database"]};' \
                            f'UID={config["uid"]};' \
                            f'PWD={config["pwd"]}'

        connection = pyodbc.connect(connection_string)
        print("Connection successful")
        return connection
    except pyodbc.Error as e:
        print("Error in connection", e)
    except FileNotFoundError:
        print("Configuration file not found")
