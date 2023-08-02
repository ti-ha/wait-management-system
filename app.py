from flask import Flask, jsonify, session
from flask_cors import CORS
import uuid, os

# import the API routes
from routes import *

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.urandom(24)
app.json.sort_keys = False

app.register_blueprint(menu_routes.menu_blueprint)
app.register_blueprint(table_routes.table_blueprint)
app.register_blueprint(order_routes.order_blueprint)
app.register_blueprint(user_routes.user_blueprint)
app.register_blueprint(service_routes.service_blueprint)
app.register_blueprint(restaurant_routes.restaurant_blueprint)
app.register_blueprint(personalised_deal_routes.deals_blueprint)

@app.before_request
def assign_session_id():
    """ Assign a unique user id for guest users """
    if not session.get('user_id'):
        session['user_id'] = uuid.uuid4()
        session.permanent = True

@app.route('/')
def home():
    """ Home Page of the app """
    return jsonify({"message": "Hello world!"}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)