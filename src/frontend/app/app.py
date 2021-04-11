from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'PONG', 200

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    return render_template('book.html')

@app.route('/bookTrip', methods=['GET', 'POST'])
def bookTrip():
    selectedCity = request.json['city']
    selectedRoute = request.json['route']

    print("The selected Route is " + selectedRoute)
    print("The selected City is " + selectedCity)

    return render_template('book.html')


@app.route('/cancelTrip', methods=['GET', 'POST'])
def cancelTrip():
    selectedCity = request.json['city']
    selectedRoute = request.json['route']

    print("The selected route is " + selectedRoute)
    print("The selected Country is " + selectedCity)

    return render_template('book.html')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)