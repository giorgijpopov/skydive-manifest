from datetime import datetime
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect
import json

from models import Flight

skydivers_separator = ';'
database_path = 'data/flights.db'
engine = create_engine(f'sqlite:///{database_path}')

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
def index():
    today = date.today()
    return render_template('index.html', date=today)

@app.route('/next_flight')
def next_flight():
    return render_template('next_flight.html')
@app.route('/next_flight_data')
def next_flight_data():
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
        remaining_time = diff.seconds // 60
        flight_data = {
            'flight': {
                'flight_number': closest_flight.flight_number,
                'aircraft_model': closest_flight.aircraft_model,
                'parachutists': closest_flight.parachutists,
            },
            'remaining_time': remaining_time,
        }
        return json.dumps(flight_data)
    else:
        return json.dumps({'flight': None, 'remaining_time': None})

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

        new_flight = Flight(date=date, time=time_obj, flight_number=flight_number, aircraft_model=aircraft_model, parachutists=skydivers_separator.join(parachutists))
        session.add(new_flight)
        session.commit()

        return redirect(f'/flights_by_date?date={date}')
    else:
        date_str = request.args.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Incorrect date type, please try YYYY-MM-DD."

        existing_flight_numbers = [
            flight.flight_number for flight in session.query(Flight).filter_by(date=date).all()
        ]
        flight_number = 1
        while flight_number in existing_flight_numbers:
            flight_number += 1

        return render_template('add_flight.html', date_str=date_str, flight_number=flight_number)

@app.route('/edit_flight', methods=['GET', 'POST'])
def edit_flight():
    if request.method == 'POST':
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        flight_number = request.form.get('flight_number')

        flight_to_edit = (
            session.query(Flight)
            .filter_by(date=date, flight_number=flight_number)
            .first()
        )

        if flight_to_edit:
            flight_to_edit.time = datetime.strptime(request.form.get('time'), '%H:%M').time()
            flight_to_edit.aircraft_model = request.form.get('aircraft_model')
            flight_to_edit.parachutists = skydivers_separator.join(request.form.getlist('parachutist'))
            session.commit()
            return redirect(f'/flights_by_date?date={date}')
        else:
            return "Flight not found"
    else:
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
        flight_number = request.args.get('flight_number')

        flight_to_edit = (
            session.query(Flight)
            .filter_by(date=date, flight_number=flight_number)
            .first()
        )

        if flight_to_edit:
            return render_template('edit_flight.html', flight=flight_to_edit)
        else:
            return "Flight not found"

@app.route('/flights_by_date', methods=['GET'])
def flights_by_date():
    date_str = request.args.get('date')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return "Incorrect date type, please try YYYY-MM-DD."

    flights = (
        session.query(Flight)
        .filter_by(date=date)
        .order_by(Flight.time)
        .all()
    )

    return render_template('flights_by_date.html', date=date, flights=flights)

@app.route('/delete_flight', methods=['POST'])
def delete_flight():
    date_str = request.json.get('date')
    flight_number = request.json.get('flight_number')

    flight_to_delete = (
        session.query(Flight)
        .filter_by(date=date_str, flight_number=flight_number)
        .first()
    )

    if flight_to_delete:
        session.delete(flight_to_delete)
        session.commit()

    return redirect(f'/flights_by_date?date={date_str}')