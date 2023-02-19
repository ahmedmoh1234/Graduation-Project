from flask import Flask, jsonify, request
import jwt


# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.5'

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    print('Test')
    return 'test'


@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data['command']
    print(command)
    return 'Success'

if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)