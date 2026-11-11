import math
import random
import system_elements
import simulation
import tkinter as tk
from tkinter import ttk

# Seconds in a day: 86400
def initialize_random(time, delta):
    # generating available system elements
    solar_panels = []
    wind_turbines = []
    batteries = []
    fuel_generators = []

    for i in range(5):
        # setting possible attribute values
        prices = [80, 90, 100, 120, 150]
        powers = [100, 200, 300]
        generator_powers = [1000, 2000, 3000]
        capacities = [1000, 500, 1500]
        battery_efficiencies = [0.8, 0.85, 0.9]
        fuel_efficiencies = [0.3, 0.35, 0.4]
        fuel_prices = [0.5]
        fuel_consumptions = [0.01]

        # generating random elements
        solar_panel = system_elements.SolarPanel(random.choice(powers), random.choice(prices))
        wind_turbine = system_elements.WindTurbine(random.choice(powers), random.choice(prices))
        battery = system_elements.Battery(random.choice(capacities), random.choice(powers), random.choice(powers),
                                          random.choice(battery_efficiencies), random.choice(battery_efficiencies),
                                          random.choice(prices))
        fuel_generator = system_elements.FuelGenerator(random.choice(generator_powers),
                                                       random.choice(fuel_efficiencies),
                                                       random.choice(prices), random.choice(fuel_prices),
                                                       random.choice(fuel_consumptions))
        connection = system_elements.GridConnection(1, 1000, 1000, 10, 10)

        # adding to the pool
        solar_panels.append(solar_panel)
        wind_turbines.append(wind_turbine)
        batteries.append(battery)
        fuel_generators.append(fuel_generator)


    #return solar_panels, wind_turbines, batteries, fuel_generators

    microgrid = system_elements.Microgrid(solar_panels, wind_turbines, batteries[1], fuel_generators[1], connection)
    simulation.simulate(time, delta, microgrid)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Microgrid Configuration")

    # Main container
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Configure columns to expand equally
    for col in range(4):
        main_frame.columnconfigure(col, weight=1)


    # Helper function for creating a parameter field
    def add_field(parent, label, default_value, row):
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", padx=5, pady=3
        )

        variable = tk.StringVar(value=str(default_value))
        entry = ttk.Entry(parent, textvariable=variable, width=12)
        entry.grid(row=row, column=1, padx=5, pady=3)

        return variable


    # SOLAR PANEL
    solar_frame = ttk.LabelFrame(main_frame, text="Solar Panel", padding=10)
    solar_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    solar_power = add_field(solar_frame, "Power", 100, 0)
    solar_number = add_field(solar_frame, "Number", 10, 1)
    solar_price = add_field(solar_frame, "Price", 10, 2)

    # WIND TURBINE
    wind_frame = ttk.LabelFrame(main_frame, text="Wind Turbine", padding=10)
    wind_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    wind_power = add_field(wind_frame, "Power", 100, 0)
    wind_number = add_field(wind_frame, "Number", 10, 1)
    wind_price = add_field(wind_frame, "Price", 10, 2)

    # BATTERY
    battery_frame = ttk.LabelFrame(main_frame, text="Battery", padding=10)
    battery_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    battery_capacity = add_field(battery_frame, "Capacity", 100, 0)
    battery_power = add_field(battery_frame, "Power", 100, 1)
    battery_max_power = add_field(battery_frame, "Max Power", 100, 2)
    battery_charge_efficiency = add_field(
        battery_frame, "Charge Efficiency", 0.9, 3
    )
    battery_discharge_efficiency = add_field(
        battery_frame, "Discharge Efficiency", 0.9, 4
    )
    battery_price = add_field(battery_frame, "Price", 10, 5)

    # FUEL GENERATOR
    generator_frame = ttk.LabelFrame(
        main_frame, text="Fuel Generator", padding=10
    )
    generator_frame.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

    generator_power = add_field(generator_frame, "Power", 100, 0)
    generator_efficiency = add_field(generator_frame, "Efficiency", 0.9, 1)
    generator_price = add_field(generator_frame, "Price", 10, 2)
    fuel_price = add_field(generator_frame, "Fuel Price", 1, 3)
    fuel_consumption = add_field(
        generator_frame, "Fuel Consumption", 1, 4
    )

    # OUTSIDE CONNECTION
    connection_frame = ttk.LabelFrame(
        main_frame, text="Outside Connection", padding=10
    )
    connection_frame.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)

    connection_export_price = add_field(connection_frame, "Export price", 10, 0)
    connection_import_price = add_field(connection_frame, "Import price", 10, 1)
    connection_export_power = add_field(connection_frame, "Export power", 1000, 2)
    connection_import_power = add_field(connection_frame, "Import power", 1000, 3)
    connection_available = add_field(connection_frame, "Availability (1 or 0)", 1, 4)



    def initialize_custom(time, delta):
        # solar
        solar_panels = []
        solar_panel = system_elements.SolarPanel(int(solar_power.get()), int(solar_price.get()))
        for i in range(int(solar_number.get())):
            solar_panels.append(solar_panel)

        # wind
        wind_turbines = []
        wind_turbine = system_elements.WindTurbine(int(wind_power.get()), int(wind_price.get()))
        for i in range(int(wind_number.get())):
            wind_turbines.append(wind_turbine)

        # battery
        battery = system_elements.Battery(int(battery_capacity.get()), int(battery_power.get()),
                                          int(battery_power.get()), float(battery_charge_efficiency.get()),
                                          float(battery_discharge_efficiency.get()), int(battery_price.get()))

        # generator
        generator = system_elements.FuelGenerator(int(generator_power.get()),
                                                       float(generator_efficiency.get()),
                                                       int(generator_price.get()), int(fuel_price.get()),
                                                       int(fuel_consumption.get()))
        connection = system_elements.GridConnection(int(connection_available.get()),
                                                    int(connection_import_power.get()),
                                                    int(connection_export_power.get()),
                                                    int(connection_import_power.get()),
                                                    int(connection_export_price.get()))
        microgrid = system_elements.Microgrid(solar_panels, wind_turbines, battery, generator, connection)
        simulation.simulate(time, delta, microgrid)

    time = add_field(root, "Simulation time", 100, 4)
    delta = add_field(root, "Delta", 1, 5)

    random_init = ttk.Button(root, text="Run! (Use random values)", command=lambda: initialize_random(int(time.get()),
                                                                                                      int(delta.get())))
    random_init.grid()

    custom_init = ttk.Button(root, text="Run! (Use custom values)", command=lambda: initialize_custom(int(time.get()),
                                                                                                      int(delta.get())))
    custom_init.grid()




    chosen_solar_panels = [1, 2]
    chosen_wind_turbines = [2, 3]
    chosen_battery = 3
    chosen_generator = 4
    
    root.mainloop()