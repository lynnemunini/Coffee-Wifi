from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    opening = StringField('Opening Time (e.g 8 AM)', validators=[DataRequired()])
    closing = StringField('Closing Time (e.g 8 PM)', validators=[DataRequired()])
    rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=[('☕☕☕☕☕'), ('☕☕☕☕'), ('☕☕☕'), ('☕☕'), ('☕'), ('✘')])
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=[('💪💪💪💪💪'), ('💪💪💪💪'), ('💪💪💪'), ('💪💪'), ('💪'), ('✘')])
    power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=[('🔌🔌🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌'), ('🔌🔌'), ('🔌'), ('✘')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():        
        data = list(request.form.listvalues())
        data = data[1:-1]
        my_data = []
        for item in data:
            item = ''.join(item)
            my_data.append(item)
        # print(my_data)

        with open('cafe-data.csv', "a") as my_file:
            write = csv.writer(my_file)      
            write.writerow(my_data)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
