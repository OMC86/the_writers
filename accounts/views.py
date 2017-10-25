from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from accounts.forms import UserRegistrationForm, UserLoginForm, UserSubscriptionForm, UserPhotoForm
from models import User
import datetime
import stripe
import arrow
import json


stripe.api_key = settings.STRIPE_SECRET


# renders the landing page
def landing(request):
    args = {'next': request.GET.get('next', '')}
    return render(request, "landing.html", args)


# There is a link in the readme README to the tutorial used to implement 'next' logic
# I also used the example form 'registering new users' on Code institute's website
#  to write the register view, which renders the registration form and registers users
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


# I followed code institutes 'handling authentication' lesson to write the log in view
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
    """
    Uploads a profile image to cloudinary and saves to user object
    """
    context = dict(backend_form=UserPhotoForm())
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            pic = request.FILES.get('avatar', False)
            user = request.user
            user.avatar = pic
            user.save()
            return redirect(reverse('home'))

    context.update(csrf(request))
    return render(request, 'uploadavatar.html', context)


# I followed the 'stripe subscriptions' lessons to write the following three views
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
        subscribed = request.user.check_subscription()
        today = datetime.date.today()
        form = UserSubscriptionForm(initial={'expiry_month': today.month, 'expiry_year': today.year})

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE, 'subscribed': subscribed}
    args.update(csrf(request))

    return render(request, 'subscribe.html', args)


@login_required
def cancel_subscription(request):
    try:
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
        messages.info(request, "Your subscription has been canceled.")
    except Exception, e:
        messages.error(request, e)

    return redirect('home')


@csrf_exempt
def subscriptions_webhook(request):
    event_json = json.loads(request.body)
    try:
        event = stripe.Event.retrieve(event_json['id'])
        cust = event_json['data']['object']['customer']
        paid = event_json['data']['object']['paid']
        user = User.objects.get(stripe_id=cust)
        if event and paid:
            user.subscription_end = arrow.now().replace(weeks=+4).datetime
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=402)
    return HttpResponse(status=200)
