from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from accounts.forms import UserRegistrationForm, UserLoginForm, UserSubscriptionForm, UserUploadPhoto
from models import User
import datetime
import stripe
import arrow
import json
from pages.views import profile


stripe.api_key = settings.STRIPE_SECRET


# renders the landing page
def landing(request):
    args = {'next': request.GET.get('next', '')}
    return render(request, "landing.html", args)


# renders the registration form and registers users
def register(request):

    redirect_to = request.POST.get('next', '')
    url_is_safe = is_safe_url(redirect_to)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if redirect_to is not None and url_is_safe:
                auth.login(request, user)
                messages.info(request, "You have successfully logged in")
                return redirect(redirect_to)

            elif user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('home'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form = UserRegistrationForm()

    args = {'form': form, 'next': request.GET.get('next', '')}
    args.update(csrf(request))

    return render(request, 'register.html', args)


# This renders the registration form and registers users
@login_required
def subscribe(request):
    if request.method == 'POST':
        form = UserSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Customer.create(
                    card=form.cleaned_data['stripe_id'],
                    plan='WRITERS_MONTHLY',
                )

                if customer:
                    user = request.user
                    user.stripe_id = customer.id
                    user.subscription_end = arrow.now().replace(weeks=+4).datetime
                    user.save()
                    messages.success(request, "You have successfully subscribed")
                    return redirect(reverse('home'))

            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined!")
    else:
        today = datetime.date.today()
        form = UserSubscriptionForm(initial={'expiry_month': today.month, 'expiry_year': today.year})

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'subscribe.html', args)


@login_required
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
    except Exception, e:
        messages.error(request, e)
    return redirect('home')

# http://andrearobertson.com/blog/2016/10/05/django-example-redirecting-to-a-passed-in-url/
# Renders the login form and authenticates user
def login(request):

    redirect_to = request.POST.get('next', '')
    url_is_safe = is_safe_url(redirect_to)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if redirect_to is not None and url_is_safe:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(redirect_to)
            elif user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('home'))
            else:
                form.add_error(None, "Your email or password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form, 'next': request.GET.get('next', '')}
    args.update(csrf(request))
    return render(request, 'login.html', args)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required
def upload(request):
    if request.method == 'POST':
        form = UserUploadPhoto(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.avatar = request.FILES['avatar']
            user.save()
            return redirect(reverse('home'))
    else:
        form = UserUploadPhoto()
    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'uploadavatar.html', args)


@csrf_exempt
def subscriptions_webhook(request):
    event_json = json.loads(request.body)
    # Verify the event by fetching it from Stripe
    try:
        # firstly verify this is a real event generated by Stripe.com
        # commented out for testing - uncomment when live
        # event = stripe.Event.retrieve(event_json['object']['id'])
        cust = event_json['object']['customer']
        paid = event_json['object']['paid']
        user = User.objects.get(stripe_id=cust)
        if user and paid:
            user.subscription_end = arrow.now().replace(weeks=+4).datetime  # 4 weeks from now
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=404)
    return HttpResponse(status=200)

