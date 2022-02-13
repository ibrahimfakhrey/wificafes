from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6c'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# db.create_all()
class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Neighborhood', validators=[DataRequired()])
    has_sockets = BooleanField('Power Socket Availability')
    has_toilet = BooleanField('Toilet Availability')
    has_wifi = BooleanField('Wifi Strength Rating')
    can_take_calls = BooleanField('can take calls?')
    seats = StringField('How many seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee price (please add unit e.g £)', validators=[DataRequired()])
    submit = SubmitField('Submit the  field')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        print("It's working")
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)





@app.route('/cafes')
def cafes():
    cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', all_cafes=cafes)

@app.route('/delete/<cafe_id>')
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))
if __name__ == '__main__':
    app.run(debug=True)