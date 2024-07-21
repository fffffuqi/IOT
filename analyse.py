import sqlite3
import random
from datetime import datetime, timedelta
import math
import os

# Define the directory and file path
directory = r'C:\Users\17590\PycharmProjects\onnxcaffe\database'
if not os.path.exists(directory):
    os.makedirs(directory)
db_path = os.path.join(directory, 'analyse.db')

# Create and connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS analyse (
                    time TEXT,
                    temperature REAL,
                    lighting BOOLEAN,
                    Doorswitch BOOLEAN,
                    Windowswitch BOOLEAN,
                    Alert BOOLEAN,
                    Curtain BOOLEAN,
                    conditioner BOOLEAN)''')

# Generate time series from 08:00 to 14:00 every half hour
start_time = datetime.strptime("08:00", "%H:%M")
end_time = datetime.strptime("14:00", "%H:%M")
delta = timedelta(minutes=30)

# Temperature variation parameters
max_temp = 35
min_temp = 20

# Insert data
current_time = start_time
data_list = []
while current_time <= end_time:
    time_str = current_time.strftime("%H:%M")
    hours = current_time.hour + current_time.minute / 60.0
    # Using a sine function to simulate temperature variation
    temperature = min_temp + (max_temp - min_temp) * math.sin(math.pi * (hours - 8) / 8)
    temperature = round(temperature, 2)
    lighting = random.choice([1, 0])
    Doorswitch = random.choice([1, 0])
    Windowswitch = random.choice([1, 0])
    Alert = random.choice([1, 0])
    Curtain = random.choice([1, 0])
    conditioner = random.choice([1, 0])

    data_list.append((time_str, temperature, lighting, Doorswitch, Windowswitch, Alert, Curtain, conditioner))
    cursor.execute(
        "INSERT INTO analyse (time, temperature, lighting, Doorswitch, Windowswitch, Alert, Curtain, conditioner) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (time_str, temperature, lighting, Doorswitch, Windowswitch, Alert, Curtain, conditioner))
    current_time += delta

# Commit transaction and close connection
conn.commit()
conn.close()

import pandas as pd

# Display the generated data
data_df = pd.DataFrame(data_list, columns=["time", "temperature", "lighting", "Doorswitch", "Windowswitch", "Alert", "Curtain", "conditioner"])
print(data_df)
