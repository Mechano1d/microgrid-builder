
def loss_of_power_supply(deficit, consumption, delta):
    lsps = (sum(deficit) * delta) / (sum(consumption) * delta)
    return lsps