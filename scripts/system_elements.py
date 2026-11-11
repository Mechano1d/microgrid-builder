

class SolarPanel:
    def __init__(self, power, price):
        self.nominal_power = power
        self.price = price

class WindTurbine:
    def __init__(self, power, price):
        self.nominal_power = power
        self.price = price

class Battery:
    def __init__(self, capacity, input_power, output_power, input_efficiency, output_efficiency, price):
        self.capacity = capacity
        self.input_power = input_power
        self.output_power = output_power
        self.input_efficiency = input_efficiency
        self.output_efficiency = output_efficiency
        self.price = price

class FuelGenerator:
    def __init__(self, power, efficiency, price, fuel_price, fuel_consumption):
        self.fuel_consumption = fuel_consumption
        self.fuel_price = fuel_price
        self.price = price
        self.efficiency = efficiency
        self.power = power

class GridConnection:
    def __init__(self, available, max_input, max_output, input_price, output_price):
        self.output_price = output_price
        self.input_price = input_price
        self.max_output = max_output
        self.max_input = max_input
        self.available = available

class Microgrid:
    def __init__(self, solar_panels, wind_turbines, battery, fuel_generator, grid_connection):
        self.outside_connection = grid_connection
        self.fuel_generator = fuel_generator
        self.battery = battery
        self.wind_turbines = wind_turbines
        self.solar_panels = solar_panels