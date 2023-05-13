from django.contrib import messages
from django.contrib.auth import authenticate, login
import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, CreateView
from django.contrib.auth.models import User
from .forms import  DepositForm, DepositLoginForm, BalanceForm, StatementForm, \
    TransferForm, TransferSubmitForm, DepositRegisterForm, CheckBookingState, BookingState, BookSubmitForm, BookForm, \
    PaymentMethodSubmit, PaymentMethodForm, CancelBookingSubmit, CancelBookingForm, GetOrderSubmit, OrderForm, \
    FindFlightSubmit, FlightForm
from accounts.models import AggregatorUser


class HomePageView(ListView):
    model = User
    template_name = 'home.html'



# checkbookingstate
class CheckBookingState(FormView):  # submit
    template_name = 'check_booking_state.html'
    form_class = CheckBookingState
    success_url = reverse_lazy('check')

    def form_valid(self, form):
        data = {
            "secret_key": form.cleaned_data.get('secret_key'),
            "order_id": form.cleaned_data.get('order_id')
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/checkBookingState', json=data)

        check_data = {
            "secret_key": form.cleaned_data.get('secret_key'),
            "order_id": int(form.cleaned_data.get('order_id'))
        }
        self.request.session['check_data'] = check_data
        return super().form_valid(form)


class CheckBookingView(ListView):
    template_name = 'check_result.html'
    context_object_name = 'check_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        check_list = []
        send_data = self.request.session.get('check_data')
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/checkBookingState', json=send_data)
        check_list.append(BookingState(response.json()['msg']))
        return check_list


# Book flight
class BookFlightSubmit(FormView):  # submit
    template_name = 'book_submit.html'
    form_class = BookSubmitForm
    success_url = reverse_lazy('book')

    def form_valid(self, form):
        data = {
            "flight_id": form.cleaned_data.get('flight_id'),
            "payer_name": form.cleaned_data.get('payer_name'),
            "payer_id": form.cleaned_data.get('payer_id'),
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/bookflight/', json=data)

        book_data = {
            "flight_id": int(form.cleaned_data.get('flight_id')),
            "payer_name": form.cleaned_data.get('payer_name'),
            "payer_id": int(form.cleaned_data.get('payer_id')),
        }
        self.request.session['book_data'] = book_data
        return super().form_valid(form)


class BookFlightView(ListView):
    template_name = 'book_result.html'
    context_object_name = 'book_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        book_list = []
        send_data = self.request.session.get('book_data')
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/bookflight', json=send_data)
        book_list.append(BookForm(response.json()['order_id']))
        return book_list


# PaymentMethod
class PaymentMethodSubmit(FormView):  # submit
    template_name = 'payment_method_submit.html'
    form_class = PaymentMethodSubmit
    success_url = reverse_lazy('paymentmethod')

    def form_valid(self, form):
        data = {
            "payment_provider": form.cleaned_data.get('payment_provider'),
            "order_id": form.cleaned_data.get('order_id')
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/paymentMethod', json=data)

        pm_data = {
            "payment_provider": form.cleaned_data.get('payment_provider'),
            "order_id": int(form.cleaned_data.get('order_id'))
        }
        self.request.session['pm_data'] = pm_data
        return super().form_valid(form)


class PaymentMethodView(ListView):
    template_name = 'payment_method_result.html'
    context_object_name = 'payment_method_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pm_list = []
        send_data = self.request.session.get('pm_data')
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/paymentMethod', json=send_data)
        pm_list.append(PaymentMethodForm(response.json()['status']))
        return pm_list


# Cancel
class CancelBookingSubmit(FormView):  # submit
    template_name = 'cancel_booking_submit.html'
    form_class = CancelBookingSubmit
    success_url = reverse_lazy('cancelbooking')

    def form_valid(self, form):
        data = {
            "order_id": form.cleaned_data.get('order_id'),
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/cancelbooking/', json=data)

        cb_data = {
            "order_id": int(form.cleaned_data.get('order_id')),
        }
        self.request.session['cb_data'] = cb_data
        return super().form_valid(form)


class CancelBookingView(ListView):
    template_name = 'cancel_booking_result.html'
    context_object_name = 'cancel_booking_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        cb_list = []
        send_data = self.request.session.get('cb_data')
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/cancelbooking', json=send_data)
        print(response.json())
        cb_list.append(CancelBookingForm(response.json()['state'], response.json()['order_id']))
        return cb_list


# Get order
class GetOrderSubmit(FormView):  # submit
    template_name = 'get_order_submit.html'
    form_class = GetOrderSubmit
    success_url = reverse_lazy('getorder')

    def form_valid(self, form):
        data = {
            "payer_name": form.cleaned_data.get('payer_name'),
            "payer_id": form.cleaned_data.get('payer_id'),
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/order', json=data)

        go_data = {
            "payer_name": form.cleaned_data.get('payer_name'),
            "payer_id": form.cleaned_data.get('payer_id'),
        }
        self.request.session['go_data'] = go_data
        return super().form_valid(form)


class GetOrderView(ListView):
    template_name = 'get_order_result.html'
    context_object_name = 'get_order_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        go_list = []
        send_data = self.request.session.get('go_data')
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/order', json=send_data)
        for item in response.json()["data"]:
            go_list.append(OrderForm(item['flight_num'],
                                     item['air_name'],
                                     item['departure_place'],
                                     item['departure_airport'],
                                     item['destin_place'],
                                     item['destin_airport'],
                                     item['departure_time'],
                                     item['arrival_time'],
                                     item['duration'],
                                     item['aircraft_type'],
                                     item['spare_seats'],
                                     item['seat_price'],
                                     item['payment_provider'],
                                     item['secret_key'],
                                     item['state'],
                                     item['payer_name'],
                                     item['flight_id'],
                                     item['order_id'],
                                     item['payer_id'],
                                     ))
        return go_list


# Find Flight
class FindFlightSubmit(FormView):  # submit
    template_name = 'find_flight_submit.html'
    form_class = FindFlightSubmit
    success_url = reverse_lazy('findflight')

    def form_valid(self, form):
        data = {
            "departure_time": form.cleaned_data.get('departure_time'),
            "departure_place": form.cleaned_data.get('departure_place'),
            "destin_place": form.cleaned_data.get('destin_place')
        }
        response = requests.get('http://sc192jl.pythonanywhere.com/api/Airline/findflight', params=data)

        ff_data = {
            "departure_time": form.cleaned_data.get('departure_time'),
            "departure_place": form.cleaned_data.get('departure_place'),
            "destin_place": form.cleaned_data.get('destin_place')
        }
        self.request.session['ff_data'] = ff_data
        return super().form_valid(form)


class FindFlightView(ListView):
    template_name = 'find_flight_result.html'
    context_object_name = 'find_flight_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        ff_list = []
        send_data = self.request.session.get('ff_data')
        response = requests.get('http://sc192jl.pythonanywhere.com/api/Airline/findflight', params=send_data)
        for item in response.json()["data"]:
            ff_list.append(FlightForm(item['flight_id'],
                                      item['flight_num'],
                                      item['air_name'],
                                      item['departure_place'],
                                      item['departure_airport'],
                                      item['destin_place'],
                                      item['destin_airport'],
                                      item['departure_time'],
                                      item['arrival_time'],
                                      item['duration'],
                                      item['aircraft_type'],
                                      item['spare_seats'],
                                      item['seat_price'],
                                      ))
        return ff_list


# Payment1
# register
payment_name_list = ['Payment_WS']


class PaymentDepositRegister(FormView):
    template_name = 'payment_register.html'
    form_class = DepositRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password'),
            "name": form.cleaned_data.get('name')
        }
        response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/signup/', json=data)

        return super().form_valid(form)


# deposit
class PaymentDepositSignup(FormView):
    template_name = 'payment_signup_deposit.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('deposit')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/signin/', json=data)
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['deposit_uid'] = uid
        return super().form_valid(form)


class PaymentDepositView(ListView):
    template_name = 'deposit.html'
    context_object_name = 'deposit_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('deposit_uid')[1]

    def get_queryset(self):
        deposit_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')

        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/deposit/', json=send_data)
            deposit_list.append(DepositForm(self.request.session.get('deposit_uid')[0], name, response.json()['msg']))
        return deposit_list


# balance
class PaymentBalanceSignup(FormView):
    template_name = 'payment_signup_deposit.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('balance')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['balance_uid'] = uid
        return super().form_valid(form)


class PaymentBalanceView(ListView):
    template_name = 'balance.html'
    context_object_name = 'balance_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('balance_uid')[1]

    def get_queryset(self):
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            print("###")
            return redirect('login_deposit.html')
        balance_list = []
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/balance/', json=send_data)
            balance_list.append(BalanceForm(self.request.session.get('balance_uid')[0], name, response.json()['income'],
                                            response.json()['expense']))
        return balance_list


# statement
class PaymentStatementSignup(FormView):
    template_name = 'payment_signup_deposit.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('statement')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['statement_uid'] = uid
        return super().form_valid(form)


class PaymentStatementView(ListView):
    template_name = 'statement.html'
    context_object_name = 'statement_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('statement_uid')[1]

    def get_queryset(self):
        statement_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list:
            response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/statement/', json=send_data)
            for i in range(len(response.json()['msg'])):
                statement_list.append(
                    StatementForm(self.request.session.get('statement_uid')[0],
                                  name,
                                  str(i + 1),
                                  response.json()['msg'][str(i)]['Time'],
                                  response.json()['msg'][str(i)]['Money'],
                                  response.json()['msg'][str(i)]['Recipient']))
        return statement_list


# transfer
class PaymentTransferSubmit(FormView):
    template_name = 'transfer_submit.html'
    form_class = TransferSubmitForm
    success_url = reverse_lazy('transfer')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/signin/', json=data)

        uid = response.json()['msg']
        print(uid)
        transfer_data = {
            "uid": uid,
            "password": form.cleaned_data.get('password'),
            "u2": form.cleaned_data.get('goal_username'),
            "u3": form.cleaned_data.get('goal_username'),
            "money": int(form.cleaned_data.get('money'))
        }
        self.request.session['transfer_data'] = transfer_data
        return super().form_valid(form)


class PaymentTransferView(ListView):
    template_name = 'transfer_result.html'
    context_object_name = 'transfer_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        transfer_list = []
        send_data = self.request.session.get('transfer_data')
        response = requests.post('https://ccty.pythonanywhere.com/Payment_WS/transfer/', json=send_data)
        transfer_list.append(TransferForm(response.json()['msg']))
        return transfer_list


# Payment weha
# register
payment_name_list2 = ['Payment_weha']


class PaymentDepositRegister2(FormView):
    template_name = 'payment_register2.html'
    form_class = DepositRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password'),
            "name": form.cleaned_data.get('name')
        }
        response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/signup/', json=data)
        return super().form_valid(form)


# deposit
class PaymentDepositSignup2(FormView):
    template_name = 'payment_signup_deposit2.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('deposit2')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/signin/', json=data)
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['deposit_uid'] = uid
        return super().form_valid(form)


class PaymentDepositView2(ListView):
    template_name = 'deposit.html'
    context_object_name = 'deposit_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('deposit_uid')[1]

    def get_queryset(self):
        deposit_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            print("11111")
            return redirect('login_deposit.html')

        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/deposit/', json=send_data)
            deposit_list.append(DepositForm(self.request.session.get('deposit_uid')[0], name, response.json()['msg']))
        return deposit_list


# balance
class PaymentBalanceSignup2(FormView):
    template_name = 'payment_signup_deposit2.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('balance2')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['balance_uid'] = uid
        return super().form_valid(form)


class PaymentBalanceView2(ListView):
    template_name = 'balance.html'
    context_object_name = 'balance_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('balance_uid')[1]

    def get_queryset(self):
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            print("###")
            return redirect('login_deposit.html')
        balance_list = []
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/balance/', json=send_data)
            balance_list.append(BalanceForm(self.request.session.get('balance_uid')[0], name, response.json()['income'],
                                            response.json()['expense']))
        return balance_list


# statement
class PaymentStatementSignup2(FormView):
    template_name = 'payment_signup_deposit2.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('statement2')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['statement_uid'] = uid
        return super().form_valid(form)


class PaymentStatementView2(ListView):
    template_name = 'statement.html'
    context_object_name = 'statement_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('statement_uid')[1]

    def get_queryset(self):
        statement_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list2:
            response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/statement/', json=send_data)
            for i in range(len(response.json()['msg'])):
                statement_list.append(
                    StatementForm(self.request.session.get('statement_uid')[0],
                                  name,
                                  str(i + 1),
                                  response.json()['msg'][str(i)]['Time'],
                                  response.json()['msg'][str(i)]['Money'],
                                  response.json()['msg'][str(i)]['Recipient']))
        return statement_list


# transfer
class PaymentTransferSubmit2(FormView):
    template_name = 'transfer_submit2.html'
    form_class = TransferSubmitForm
    success_url = reverse_lazy('transfer2')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/signin/', json=data)

        uid = response.json()['msg']
        print(uid)
        transfer_data = {
            "uid": uid,
            "password": form.cleaned_data.get('password'),
            "u2": form.cleaned_data.get('goal_username'),
            "u3": form.cleaned_data.get('goal_username'),
            "money": int(form.cleaned_data.get('money'))
        }
        self.request.session['transfer_data'] = transfer_data
        return super().form_valid(form)


class PaymentTransferView2(ListView):
    template_name = 'transfer_result.html'
    context_object_name = 'transfer_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        transfer_list = []
        send_data = self.request.session.get('transfer_data')
        response = requests.post('http://sc19yx2.pythonanywhere.com/Payment_weha/transfer/', json=send_data)
        transfer_list.append(TransferForm(response.json()['msg']))
        return transfer_list


# Payment nnr
# register
payment_name_list3 = ['Payment_nnr']


class PaymentDepositRegister3(FormView):
    template_name = 'payment_register3.html'
    form_class = DepositRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password'),
            "name": form.cleaned_data.get('name')
        }
        response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/signup/', json=data)
        return super().form_valid(form)


# deposit
class PaymentDepositSignup3(FormView):
    template_name = 'payment_signup_deposit3.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('deposit3')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/signin/', json=data)
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['deposit_uid'] = uid
        return super().form_valid(form)


class PaymentDepositView3(ListView):
    template_name = 'deposit.html'
    context_object_name = 'deposit_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('deposit_uid')[1]

    def get_queryset(self):
        deposit_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')

        send_data = {
            "uid": self.get_user_id()
        }
        print(send_data)
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/deposit/', json=send_data)
            deposit_list.append(DepositForm(self.request.session.get('deposit_uid')[0], name, response.json()['msg']))
        return deposit_list


# balance
class PaymentBalanceSignup3(FormView):
    template_name = 'payment_signup_deposit3.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('balance3')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['balance_uid'] = uid
        return super().form_valid(form)


class PaymentBalanceView3(ListView):
    template_name = 'balance.html'
    context_object_name = 'balance_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('balance_uid')[1]

    def get_queryset(self):
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')
        balance_list = []
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/balance/', json=send_data)
            balance_list.append(BalanceForm(self.request.session.get('balance_uid')[0], name, response.json()['income'],
                                            response.json()['expense']))
        return balance_list


# statement
class PaymentStatementSignup3(FormView):
    template_name = 'payment_signup_deposit3.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('statement3')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/signin/', json=data)
            print(response.json())
            uid.append(form.cleaned_data.get('username'))
            uid.append(response.json()['msg'])
        self.request.session['statement_uid'] = uid
        return super().form_valid(form)


class PaymentStatementView3(ListView):
    template_name = 'statement.html'
    context_object_name = 'statement_list'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('statement_uid')[1]

    def get_queryset(self):
        statement_list = []
        if self.request.session.get('deposit_uid')[1] == "You have no account, please sign up.":
            return redirect('login_deposit.html')
        send_data = {
            "uid": self.get_user_id()
        }
        for name in payment_name_list3:
            response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/statement/', json=send_data)
            for i in range(len(response.json()['msg'])):
                statement_list.append(
                    StatementForm(self.request.session.get('statement_uid')[0],
                                  name,
                                  str(i + 1),
                                  response.json()['msg'][str(i)]['Time'],
                                  response.json()['msg'][str(i)]['Money'],
                                  response.json()['msg'][str(i)]['Recipient']))
        return statement_list


# transfer
class PaymentTransferSubmit3(FormView):
    template_name = 'transfer_submit3.html'
    form_class = TransferSubmitForm
    success_url = reverse_lazy('transfer3')

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/signin/', json=data)

        uid = response.json()['msg']
        print(uid)
        transfer_data = {
            "uid": uid,
            "password": form.cleaned_data.get('password'),
            "u2": form.cleaned_data.get('goal_username'),
            "u3": form.cleaned_data.get('goal_username'),
            "money": int(form.cleaned_data.get('money'))
        }
        self.request.session['transfer_data'] = transfer_data
        return super().form_valid(form)


class PaymentTransferView3(ListView):
    template_name = 'transfer_result.html'
    context_object_name = 'transfer_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        transfer_list = []
        send_data = self.request.session.get('transfer_data')
        response = requests.post('https://sc192yz.pythonanywhere.com/Payment_nnr/transfer/', json=send_data)
        transfer_list.append(TransferForm(response.json()['msg']))
        return transfer_list
