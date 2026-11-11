import temporal_variables
import system_elements
import analytics
import matplotlib.pyplot as plt

def simulate(time, delta, microgrid):

    # wind availability: random values in range of [0, 1]
    wind_series = temporal_variables.TimeSeries(delta, time)
    wind_series.generate_wind(0.5, 1)

    # solar availability: 0 at start, rises up to 1, then falls back to 0, with added randomness
    solar_series = temporal_variables.TimeSeries(delta, time)
    solar_series.generate_solar()
    print(solar_series)

    # consumption coefficient: random values in range of [0, 1]
    consumption_series = temporal_variables.TimeSeries(delta, time)
    consumption_series.generate_random_mean(1, 0.5)

    # series for battery charge/discharge
    battery_series = temporal_variables.TimeSeries(delta, time)

    # series for generator output
    generator_series = temporal_variables.TimeSeries(delta, time)

    # series for microgrid power balance
    balance_series = temporal_variables.TimeSeries(delta, time)

    # series for microgrid deficit
    deficit_series = temporal_variables.TimeSeries(delta, time)

    # series for timestamps
    time_series = [t for t in range(time)]


    # calculating total attributes
    # solar
    solar_output = sum([s.nominal_power for s in microgrid.solar_panels])

    # wind
    wind_output = sum([w.nominal_power for w in microgrid.wind_turbines])

    # battery
    max_storage = microgrid.battery.capacity
    storage = max_storage * 0.6
    charge_rate_max = microgrid.battery.input_power
    discharge_rate_max = microgrid.battery.output_power
    battery_input_efficiency = microgrid.battery.input_efficiency
    battery_output_efficiency = microgrid.battery.output_efficiency

    # generator
    generator_power_max = microgrid.fuel_generator.power

    # cost calculation
    initial_cost = (sum([s.price for s in microgrid.solar_panels]) + sum([w.price for w in microgrid.wind_turbines])
                    + microgrid.battery.price + microgrid.fuel_generator.price)

    running_cost = 0
    power_exchange_cost = 0
    fuel_cost = 0

    generator_running_cost = microgrid.fuel_generator.fuel_price * microgrid.fuel_generator.fuel_consumption / generator_power_max
    import_running_cost = microgrid.outside_connection.input_price
    export_running_profit = microgrid.outside_connection.output_price
    exchange_available = microgrid.outside_connection.available
    exchange_history = []


    # consumption
    consumption_multiplier = 1000

    for t in range(time):


        battery_change = 0
        generator_power = 0
        balance = (solar_series.values[t] * solar_output + wind_series.values[t] * wind_output -
                   consumption_series.values[t] * consumption_multiplier)

        if balance < 0:
            if storage * battery_output_efficiency >= -balance:
                battery_change = min(abs(balance) / battery_output_efficiency, discharge_rate_max)
                storage -= battery_change
                balance += battery_change * battery_output_efficiency
                battery_change = -battery_change


            else:
                battery_change = storage
                storage = 0
                balance += battery_change * battery_output_efficiency
                battery_change = -battery_change
                if generator_running_cost < import_running_cost or not exchange_available:
                    generator_power = min(generator_power_max, -balance)
                    fuel_cost = generator_running_cost * generator_power
                    balance += generator_power

                    if balance < 0 and exchange_available:
                        imported_power = min(microgrid.outside_connection.max_input, -balance)
                        balance += imported_power
                        power_exchange_cost += imported_power * import_running_cost

                else:
                    imported_power = min(microgrid.outside_connection.max_input, -balance)
                    balance += imported_power
                    power_exchange_cost += imported_power * import_running_cost
                    if balance < 0:
                        generator_power = min(generator_power_max, -balance)
                        fuel_cost = generator_running_cost * generator_power
                        balance += generator_power

        else:
            battery_change = min(balance * battery_input_efficiency, charge_rate_max)
            if storage + battery_change <= max_storage:
                storage += battery_change * battery_input_efficiency
                storage = min(storage, max_storage)
                balance -= battery_change / battery_input_efficiency
            else:
                battery_change = max_storage - storage
                storage = max_storage
                balance = balance - battery_change / battery_input_efficiency
                if exchange_available:
                    exported_power = min(balance, microgrid.outside_connection.max_output)
                    power_exchange_cost -= exported_power * export_running_profit

        running_cost += fuel_cost + power_exchange_cost
        exchange_history.append(power_exchange_cost)
        battery_series.values.append(battery_change)
        generator_series.values.append(generator_power)
        balance_series.values.append(balance)

    solar_history = [v * solar_output for v in solar_series.values]
    wind_history = [v * wind_output for v in wind_series.values]
    consumption_history = [v * consumption_multiplier for v in consumption_series.values]
    deficit_series = [min(b, 0) for b in balance_series.values]

    lpsp = analytics.loss_of_power_supply(deficit_series, consumption_history, delta)
    running_cost = fuel_cost + power_exchange_cost
    print(lpsp)
    print(f"Fixed expenditures: {initial_cost}")
    print(f"Running expenses: {running_cost}")
    print(f"Fuel expenses: {fuel_cost}")
    print(f"Exchange expenses: {power_exchange_cost}")
    print(f"Total: {initial_cost + running_cost}")
    print(exchange_history)

    fig, ax = plt.subplots()

    ax.plot(time_series, solar_history, color="orange", label="Solar generation")
    ax.plot(time_series, wind_history, color="blue", label="Wind generation")
    ax.plot(time_series, consumption_history, color="red", label="Consumption")
    ax.plot(time_series, battery_series.values, color="green", label="Battery")
    ax.plot(time_series, generator_series.values, color="brown", label="Fuel generator")
    ax.plot(time_series, balance_series.values, color="black", label="Energy balance")

    ax.legend()
    #ax.plot(time_series, balance_series)

    plt.show()