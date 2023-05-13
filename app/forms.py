from django import forms


# Payment1
class DepositLoginForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})


class DepositRegisterForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})
    name = forms.CharField(label='name', error_messages={'required': 'Cannot be empty!'})


class BalanceLoginForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})


class DepositForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    deposit = forms.CharField

    def __init__(self, username, paymentname, deposit):
        self.paymentname = paymentname
        self.deposit = deposit
        self.username = username


class BalanceForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    income = forms.CharField
    expense = forms.CharField

    def __init__(self, username, paymentname, income, expense):
        self.paymentname = paymentname
        self.username = username
        self.income = income
        self.expense = expense


class StatementForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    number = forms.CharField
    time = forms.CharField
    money = forms.CharField
    recipient = forms.CharField

    def __init__(self, paymentname, username, number, time, money, recipient):
        self.paymentname = paymentname
        self.username = username
        self.number = number
        self.time = time
        self.money = money
        self.recipient = recipient


class TransferSubmitForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})
    goal_username = forms.CharField(label='goal_username', error_messages={'required': 'Cannot be empty!'})
    money = forms.CharField(label='money', error_messages={'required': 'Cannot be empty!'})


class TransferForm(forms.Form):
    status = forms.CharField

    def __init__(self, status):
        self.status = status


class CheckBookingState(forms.Form):
    secret_key = forms.CharField(label='secret_key', error_messages={'required': 'Cannot be empty!'})
    order_id = forms.IntegerField(label='order_id', error_messages={'required': 'Cannot be empty!'})


class BookingState(forms.Form):
    status = forms.CharField

    def __init__(self, status):
        self.status = status


class BookSubmitForm(forms.Form):
    flight_id = forms.IntegerField(label='flight_id', error_messages={'required': 'Cannot be empty!'})
    payer_name = forms.CharField(label='payer_name', error_messages={'required': 'Cannot be empty!'})
    payer_id = forms.IntegerField(label='payer_id', error_messages={'required': 'Cannot be empty!'})


class BookForm(forms.Form):
    order_id = forms.CharField

    def __init__(self, order_id):
        self.order_id = order_id


class PaymentMethodSubmit(forms.Form):
    payment_provider = forms.CharField(label='payment_provider', error_messages={'required': 'Cannot be empty!'})
    order_id = forms.IntegerField(label='order_id', error_messages={'required': 'Cannot be empty!'})


class PaymentMethodForm(forms.Form):
    status = forms.CharField

    def __init__(self, status):
        self.status = status


class CancelBookingSubmit(forms.Form):
    order_id = forms.IntegerField(label='order_id', error_messages={'required': 'Cannot be empty!'})


class CancelBookingForm(forms.Form):
    state = forms.CharField
    order_id = forms.CharField

    def __init__(self, state, order_id):
        self.state = state
        self.order_id = order_id


class GetOrderSubmit(forms.Form):
    payer_name = forms.CharField(label='payer_name', error_messages={'required': 'Cannot be empty!'})
    payer_id = forms.IntegerField(label='payer_id', error_messages={'required': 'Cannot be empty!'})


class OrderForm(forms.Form):


    flight_num = forms.CharField
    air_name = forms.CharField
    departure_place = forms.CharField
    departure_airport = forms.CharField
    destin_place = forms.CharField
    destin_airport = forms.CharField
    departure_time = forms.CharField
    arrival_time= forms.CharField
    duration= forms.CharField
    aircraft_type= forms.CharField
    spare_seats= forms.CharField
    seat_price= forms.CharField
    payment_provider= forms.CharField
    secret_key= forms.CharField
    state= forms.CharField
    flight_id = forms.CharField
    payer_name= forms.CharField
    order_id= forms.CharField
    payer_id= forms.CharField


    def __init__(self,  flight_num, air_name, departure_place, departure_airport, destin_place, destin_airport, \
                 departure_time, arrival_time, duration, aircraft_type, spare_seats, seat_price,  payment_provider,\
                 secret_key, state, payer_name, flight_id, order_id,payer_id):

        self.flight_num = flight_num
        self.air_name = air_name
        self.departure_place = departure_place
        self.departure_airport= departure_airport
        self.destin_place= destin_place
        self.destin_airport = destin_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.aircraft_type= aircraft_type
        self.spare_seats= spare_seats
        self.seat_price = seat_price
        self.payment_provider = payment_provider
        self.secret_key = secret_key
        self.state = state
        self.payer_name = payer_name
        self.flight_id = flight_id
        self.order_id = order_id
        self.payer_id = payer_id



class FindFlightSubmit(forms.Form):
    departure_time = forms.CharField(label='departure_time', error_messages={'required': 'Cannot be empty!'})
    departure_place = forms.CharField(label='departure_place', error_messages={'required': 'Cannot be empty!'})
    destin_place = forms.CharField(label='destin_place', error_messages={'required': 'Cannot be empty!'})


class FlightForm(forms.Form):
    flight_id = forms.CharField
    flight_num = forms.CharField
    air_name = forms.CharField
    departure_place = forms.CharField
    departure_airport = forms.CharField
    destin_place = forms.CharField
    destin_airport = forms.CharField
    departure_time = forms.CharField
    arrival_time= forms.CharField
    duration= forms.CharField
    aircraft_type= forms.CharField
    spare_seats= forms.CharField
    seat_price= forms.CharField

    def __init__(self, flight_id, flight_num, air_name, departure_place, departure_airport, destin_place, destin_airport, \
                 departure_time, arrival_time, duration, aircraft_type, spare_seats, seat_price):
        self.flight_id = flight_id
        self.flight_num = flight_num
        self.air_name = air_name
        self.departure_place = departure_place
        self.departure_airport= departure_airport
        self.destin_place= destin_place
        self.destin_airport = destin_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.aircraft_type= aircraft_type
        self.spare_seats= spare_seats
        self.seat_price = seat_price
