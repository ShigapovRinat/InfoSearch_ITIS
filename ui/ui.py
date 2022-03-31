from flask import Flask, render_template, request
from task5 import task5

app = Flask(__name__)


@app.route('/find', methods=['POST'])
def find():
    global result
    expression = request.form['expression']
    print(expression)
    result = task5.resolve_expression(expression)
    print(result)
    if len(result) == 0:
        return render_template('not_found.html', expression=expression)
    return render_template('main.html', result=result, expression=expression)


@app.route('/')
def index():
    global result
    result = []
    return render_template('main.html', result=result)


if __name__ == "__main__":
    result = []
    task5.prepare()
    task5.fill_tf()
    app.run()
