from flask import Flask, render_template, request
from controller import chart_data, create_chart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dates', methods=['POST'])
def create():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    return render_template('chart.html', line_chart = create_chart(chart_data(start_date, end_date)))

if __name__ == '__main__':
    app.run(debug=True)

