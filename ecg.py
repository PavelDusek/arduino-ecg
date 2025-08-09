# coding: utf-8
"""Simple script to plot ECG data from serial port."""

# Arduino code may be found at
# https://navody.dratek.cz/navody-k-produktum/ekg-monitoring-srdecni-frekvence-ad8232.html

import datetime

import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PORT = "/dev/ttyUSB0"  # on linux, $USER has to be in uucp group
BAUDRATE = 9600
DURATION_MILIS = 1000 / BAUDRATE
TIMEOUT = 1  # maximal timeout for serial communication
DATAPOINTS = 10000  # number of datapoint to measure

now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

data = []
with serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT) as ser:
    for _ in range(DATAPOINTS):
        data.append(ser.readline().strip().decode())

data = np.array(
    [int(measurement) if measurement not in ["!", ""] else 0 for measurement in data]
)
time = np.arange(0, len(data)) * DURATION_MILIS

plt.plot(time, data)
plt.title(timestamp)
plt.xlabel("time [ms]")
plt.ylabel("ECG signal")
plt.savefig(f"{timestamp}.png")
plt.show()

df = pd.DataFrame({"time": time, "ecg": data})
df.to_csv(f"{timestamp}.csv", index=False)
