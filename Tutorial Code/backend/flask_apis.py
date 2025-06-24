from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    data = {
        'message': 'Error while loading'
    }

    return jsonify(data), 404

# @app.route('/api/addition/<int:a>/<int:b>', methods=['GET'])
# def addtion(a,b):
#     result = a + b

#     data = {
#         "value": result,
#         "message": f"Additon of two numbers {a} and {b} is {result}"
#     }

#     return jsonify(data), 200

@app.route('/api/addition', methods = ['GET'])
def addtion():
    request_data = request.get_json()
    result_data = {
        "value": request_data['a'] + request_data['b'],
        "message": f"Additon of two numbers {request_data['a']} and {request_data['b']} is {request_data['a'] + request_data['b']}"
    }

    return jsonify(result_data), 200

if __name__ == '__main__':
    app.run(debug=True)
