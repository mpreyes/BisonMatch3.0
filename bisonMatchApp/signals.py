from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Lustudent
from django.db import connection
from contextlib import closing
from django.dispatch import receiver


@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    print("show me the money")
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "bisonmatch2.0@gmail.com":
            # Not a valid payment
            print("not a valid payment")
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        lnumber = "L2278619"
        if ipn_obj.custom == "premium_plan":
            print("premium plan")
        else:
            price = 3.0
            print("not premium plan")

        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
            Lustudent.paid = 1
            Lustudent.save()
            SQL_UPDATE = "UPDATE `lustudent` SET  `Paid` = `1` WHERE `lnumber` = " + str(lnumber) + ";"
            print(SQL_UPDATE)
            with closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                cursor.execute(SQL_UPDATE)
            connection.close()
            print("okay!")
    else:
        print("error in payment status")
    try:
        ipn_obj.verify(ipn_obj)
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)

    valid_ipn_received.connect(show_me_the_money)