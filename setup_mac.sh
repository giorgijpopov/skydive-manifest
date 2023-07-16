#!/bin/bash

echo "Installing SQLite..."
brew update
brew install sqlite3

mkdir -p data

echo "Creating flights Database..."
sqlite3 data/flights.db <<EOF
CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    time TIME,
    flight_number TEXT,
    aircraft_model TEXT,
    parachutists TEXT
);
EOF

echo "Installing Python..."
brew install python3 python3-pip

echo "Installing environment..."
python3 -m venv myenv
source myenv/bin/activate

echo "Install Flask..."
pip install flask sqlalchemy

echo "Creating running script..."
cat <<EOT > run.sh
#!/bin/bash
source myenv/bin/activate
export FLASK_APP=src/app.py
flask run --host=0.0.0.0 --port=8000
EOT

chmod +x run.sh

echo "Success! You can run the application using ./run.sh"
