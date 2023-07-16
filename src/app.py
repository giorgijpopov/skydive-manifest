from datetime import datetime
from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect

from models import Flight

database_path = 'data/flights.db'
engine = create_engine(f'sqlite:///{database_path}')

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
def index():
    current_datetime = datetime.now()

    closest_flight = (
        session.query(Flight)
        .filter(Flight.date >= current_datetime.date(), Flight.time >= current_datetime.time())
        .order_by(Flight.date, Flight.time)
        .first()
    )

    remaining_time = None
    if closest_flight:
        datetime1 = datetime.combine(datetime.min, closest_flight.time)
        datetime2 = datetime.combine(datetime.min, current_datetime.time())
        diff = datetime1 - datetime2
        hours = diff.seconds // 3600
        minutes = (diff.seconds // 60) % 60
        seconds = diff.seconds % 60
        remaining_time = str(time(hours, minutes, seconds))

    return render_template('index.html', flight=closest_flight, remaining_time=remaining_time)

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        time_str = request.form.get('time')
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        flight_number = request.form.get('flight_number')
        aircraft_model = request.form.get('aircraft_model')
        parachutists = request.form.getlist('parachutist')

        existing_flight = (
            session.query(Flight)
            .filter_by(date=date, flight_number=flight_number)
            .first()
        )

        if existing_flight:
            return "Flight with this flight number already exists on this date"

        new_flight = Flight(date=date, time=time_obj, flight_number=flight_number, aircraft_model=aircraft_model, parachutists=';'.join(parachutists))
        session.add(new_flight)
        session.commit()

        return redirect('/')
    else:
        return render_template('add_flight.html')
