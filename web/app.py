from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://172.17.0.2:27017")
db = client['test_db']
collection = db["test_collection"]

collection.insert_one({
    'num_of_visits': 0
})


class Visit(Resource):
    def get(self):
        prev_num = collection.find({})[0]['num_of_visits']
        new_num = prev_num + 1
        collection.update_one({}, {'$set': {'num_of_visits': new_num}})
        return "Hello Visitor " + str(new_num)


def check_posted_data(data, function_name):
    if function_name == 'add' or function_name == 'subtract' or function_name == 'multiply':
        if 'x' not in data or 'y' not in data:
            return 301
        else:
            return 200
    elif function_name == 'divide':
        if 'x' not in data or 'y' not in data:
            return 301
        elif int(data['y']) == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, 'add')

        # make sure nothing crashes your server
        if status_code != 200:
            return_dict = {
                'message': '[ERROR] Either x or y missing in request body',
                'status_code': status_code
            }

            return jsonify(return_dict)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        z = x + y

        return_dict = {
            'message': z,
            'status_code': status_code
        }

        return jsonify(return_dict)


class Subtract(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, 'subtract')

        if status_code != 200:
            return_dict = {
                'message': '[ERROR] Either x or y missing in request body',
                'status_code': status_code
            }

            return jsonify(return_dict)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        z = x - y

        return_dict = {
            'message': z,
            'status_code': status_code
        }

        return jsonify(return_dict)


class Multiply(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, 'multiply')

        if status_code != 200:
            return_dict = {
                'message': '[ERROR] Either x or y missing in request body',
                'status_code': status_code
            }

            return jsonify(return_dict)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        z = x * y

        return_dict = {
            'message': z,
            'status_code': status_code
        }

        return jsonify(return_dict)


class Divide(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, 'divide')

        if status_code == 301:
            return_dict = {
                'message': '[ERROR] Either x or y missing in request body',
                'status_code': status_code
            }

            return jsonify(return_dict)

        elif status_code == 302:
            return_dict = {
                'message': '[ERROR] Cannot divide by 0',
                'status_code': status_code
            }

            return jsonify(return_dict)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        z = x / y

        return_dict = {
            'message': z,
            'status_code': status_code
        }

        return jsonify(return_dict)


api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')
api.add_resource(Visit, '/hello')


@app.route('/')
def index():
    return "Hello World!"


@app.route('/add_two_nums', methods=["POST"])
def add_two_nums():
    data_dict = request.get_json()

    if 'x' not in data_dict or 'y' not in data_dict:
        return "[ERROR] Either x or y missing in message body"

    x = data_dict['x']
    y = data_dict['y']
    z = x + y

    return_json = {
        'z': z
    }

    return jsonify(return_json)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
