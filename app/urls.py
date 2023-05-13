from django.urls import path
from .views import HomePageView,  PaymentDepositView, \
    PaymentDepositSignup, PaymentBalanceView, PaymentBalanceSignup, PaymentStatementView, PaymentStatementSignup, \
    PaymentTransferView, PaymentTransferSubmit, PaymentDepositRegister, \
    PaymentDepositView2, PaymentDepositSignup2, PaymentBalanceView2, PaymentBalanceSignup2, PaymentStatementView2, PaymentStatementSignup2, \
    PaymentTransferView2, PaymentTransferSubmit2, PaymentDepositRegister2,\
    PaymentDepositView3, PaymentDepositSignup3, PaymentBalanceView3, PaymentBalanceSignup3, PaymentStatementView3, PaymentStatementSignup3, \
    PaymentTransferView3, PaymentTransferSubmit3, PaymentDepositRegister3,\
    CheckBookingState,CheckBookingView, BookFlightView, BookFlightSubmit, PaymentMethodSubmit, PaymentMethodView,\
    CancelBookingSubmit, CancelBookingView, GetOrderView , GetOrderSubmit, FindFlightSubmit, FindFlightView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('checksubmit/',CheckBookingState.as_view(), name='check_submit'),
    path('check/', CheckBookingView.as_view(), name='check'),
    path('booksubmit/', BookFlightSubmit.as_view(), name='book_submit'),
    path('book/', BookFlightView.as_view(), name='book'),
    path('paymentmethodsubmit/', PaymentMethodSubmit.as_view(), name='paymentmethod_submit'),
    path('paymentmethod/', PaymentMethodView.as_view(), name='paymentmethod'),
    path('cancelbookingsubmit/', CancelBookingSubmit.as_view(), name='cancelbooking_submit'),
    path('cancelbooking/', CancelBookingView.as_view(), name='cancelbooking'),
    path('getordersubmit/', GetOrderSubmit.as_view(), name='getorder_submit'),
    path('getorder/', GetOrderView.as_view(), name='getorder'),
    path('findflightsubmit/', FindFlightSubmit.as_view(), name='findflight_submit'),
    path('findflight/', FindFlightView.as_view(), name='findflight'),
    #Payment WS
    path('deposit/', PaymentDepositView.as_view(), name='deposit'),
    path('balance/', PaymentBalanceView.as_view(), name='balance'),
    path('statement/', PaymentStatementView.as_view(), name='statement'),
    path('transfer/', PaymentTransferView.as_view(), name='transfer'),
    path('paymentdepositlogin/', PaymentDepositSignup.as_view(), name='login_deposit'),
    path('paymentbalancelogin/', PaymentBalanceSignup.as_view(), name='login_balance'),
    path('paymentstatementlogin/', PaymentStatementSignup.as_view(), name='login_statement'),
    path('paymenttransfersubmit/', PaymentTransferSubmit.as_view(), name='submit_transfer'),
    path('paymentregister/', PaymentDepositRegister.as_view(), name='payment_register'),
    # Payment weha
    path('deposit2/', PaymentDepositView2.as_view(), name='deposit2'),
    path('balance2/', PaymentBalanceView2.as_view(), name='balance2'),
    path('statement2/', PaymentStatementView2.as_view(), name='statement2'),
    path('transfer2/', PaymentTransferView2.as_view(), name='transfer2'),
    path('paymentdepositlogin2/', PaymentDepositSignup2.as_view(), name='login_deposit2'),
    path('paymentbalancelogin2/', PaymentBalanceSignup2.as_view(), name='login_balance2'),
    path('paymentstatementlogin2/', PaymentStatementSignup2.as_view(), name='login_statement2'),
    path('paymenttransfersubmit2/', PaymentTransferSubmit2.as_view(), name='submit_transfer2'),
    path('paymentregister2/', PaymentDepositRegister2.as_view(), name='payment_register2'),
    # Payment nnr
    path('deposit3/', PaymentDepositView3.as_view(), name='deposit3'),
    path('balance3/', PaymentBalanceView3.as_view(), name='balance3'),
    path('statement3/', PaymentStatementView3.as_view(), name='statement3'),
    path('transfer3/', PaymentTransferView3.as_view(), name='transfer3'),
    path('paymentdepositlogin3/', PaymentDepositSignup3.as_view(), name='login_deposit3'),
    path('paymentbalancelogin3/', PaymentBalanceSignup3.as_view(), name='login_balance3'),
    path('paymentstatementlogin3/', PaymentStatementSignup3.as_view(), name='login_statement3'),
    path('paymenttransfersubmit3/', PaymentTransferSubmit3.as_view(), name='submit_transfer3'),
    path('paymentregister3/', PaymentDepositRegister3.as_view(), name='payment_register3'),
]
