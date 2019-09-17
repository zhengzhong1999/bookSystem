

class Order:
    passenger_name = ''
    flight_name = ''
    flight_route = ''
    flight_ltime = ''
    flight_price = ''
    card = 0

    def __init__(self, pname, fname, froute, fltime, fprice, card):
        self.passenger_name = pname
        self.flight_name = fname
        self.flight_route = froute
        self.flight_ltime = fltime
        self.flight_price = fprice
        self.card = card