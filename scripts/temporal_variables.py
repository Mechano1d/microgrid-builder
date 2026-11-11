import math
import random
import pandas as pd
import matplotlib.pyplot as plt
from solar_simulation import calculate_solar_irradiance

class TimeSeries:
    def __init__(self, delta, length, values = None):
        if values is None:
            values = []
        self.delta = delta
        self.length = length
        self.values = values

    def solar_function(self, time):
        x = time * 24 * self.delta / self.length
        return -0.01 * math.pow(x - 12, 2) + 1

    def generate_solar(self, day=172, panel_tilt=30, panel_azimuth=0):
        self.values = []
        for t in range(self.length):
            time = t / self.length * 24
            self.values.append(calculate_solar_irradiance(
                day_of_year=day,
                local_time=time,
                panel_tilt=panel_tilt,
                panel_azimuth=panel_azimuth
            ))
            # print(self.values[len(self.values)-1])

    def generate_wind(self, mean, deviation):
        self.values = []
        for t in range(self.length):
            self.values.append(max(random.gauss(mean, deviation), 0))

    def generate_random_mean(self, mean, deviation):
        self.values = []
        for t in range(self.length):
            self.values.append(random.gauss(mean, deviation))

    def generate_random_interval(self, min, max):
        self.values = []
        for t in range(self.length):
            self.values.append(random.randrange(min, max))
