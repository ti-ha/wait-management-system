from flask import Flask, jsonify, request
from wms import Menu
import json

app = Flask(__name__)

menu = Menu()

@app.route('/')
def home():
    return "Hello world!"

@app.route('/menu', methods=['GET'])
def get_menu():
    return menu.jsonify()


if __name__ == '__main__':
    app.run(port=5000)