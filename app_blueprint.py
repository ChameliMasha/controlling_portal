from flask import Blueprint, render_template, request

app_blueprint = Blueprint('app_blueprint', __name__)

# Initial variables
variable_set = [
    {'name': 'UID', 'value': '451'},
    {'name': 'DV', 'value': '78.452'},
    {'name': 'DI', 'value': '8.42'},
    {'name': 'IV', 'value': '142'},
    {'name': 'CV', 'value': '52.14'},
    {'name': 'II', 'value': '96.3'}
]


@app_blueprint.route('/show')
def index():
    # Get URL parameters
    uid_val = request.args.get('uid')
    dv_val = request.args.get('dv')
    di_val = request.args.get('di')
    iv_val = request.args.get('iv')
    cv_val = request.args.get('cv')
    ii_val = request.args.get('ii')

    # Update variable_set based on URL parameters
    update_variable_set(uid_val, dv_val, di_val, iv_val, cv_val, ii_val)

    return render_template("index2.html", variable_set=variable_set)


@app_blueprint.route('/start')
def about():
    return render_template("about.html")


# Function to update variable_set based on URL parameters
def update_variable_set(uid_val, dv_val, di_val, iv_val, cv_val, ii_val):
    for variable in variable_set:
        if variable['name'] == 'UID' and uid_val is not None:
            variable['value'] = uid_val
        elif variable['name'] == 'DV' and dv_val is not None:
            variable['value'] = dv_val
        elif variable['name'] == 'DI' and di_val is not None:
            variable['value'] = di_val
        elif variable['name'] == 'IV' and iv_val is not None:
            variable['value'] = iv_val
        elif variable['name'] == 'CV' and cv_val is not None:
            variable['value'] = cv_val
        elif variable['name'] == 'II' and ii_val is not None:
            variable['value'] = ii_val


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
