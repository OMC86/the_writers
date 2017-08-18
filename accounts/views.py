from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from accounts.forms import UserRegistrationForm, UserLoginForm, UserSubscriptionForm
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
import stripe
import arrow

stripe.api_key = settings.STRIPE_SECRET

# This view renders the landing page
def landing(request):
    return render(request, "landing.html")

# This view renders the base template after login which is the profile home page
def profile(request):
    return render(request, 'base.html')

# This renders the registration form and registers users
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered")
                return redirect(reverse('home'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)


# This renders the registration form and registers users

def subscribe(request):
    if request.method == 'POST':
        form = UserSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Customer.create(
                    email=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id'],
                    plan='WRITERS_MONTHLY',
                )

                if customer:
                    user = form.save()
                    user.stripe_id = customer.id
                    user.subscription_end = arrow.now().replace(weeks=+4).datetime
                    user.save()

                    user = auth.authenticate(email=request.POST.get('email'),
                                             password=request.POST.get('password1'))

                    if user is not None:
                        messages.success(request, "You have successfully subscribed")
                        return redirect(reverse('home'))
                    else:
                        messages.error(request, "We were unable to take a payment with that card!")

            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined!")
    else:
        today = datetime.date.today()
        form = UserSubscriptionForm(initial={'expiry_month': today.month, 'expiry_year': today.year})

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'subscribe.html', args)


def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
    except Exception, e:
        messages.error(request, e)
    return redirect('home')


# Renders the login form and authenticates user
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('home'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('login'))