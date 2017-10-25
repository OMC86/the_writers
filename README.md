# The Writers

## Overview

### What is the purpose of this site?

The Writers is an online community for people who want to share their writing talents, discuss what they have written
with those who read their posts and possibly win some money entering writing competitions.

### What can users do?

#### General users
The site allows users to register and log in. Once users are logged in they can create posts, choosing whether
or not to make their posts public. Once a post is published, other authenticated users are able to post comments on it.
Users are also allowed to vote for competition entries they think deserve to win a competition.

#### Subscribed users
While subscribers enjoy the same privileges as general users, they also get the added benefit of entering their posts
in to competitions in which they can win a cash prize.


#### Admin
The administrator can delete and edit posts at his/her discretion and is also in charge of creating competitions.

##### Competitions
Competitions are held on the site at the discretion of the admin. They consist of two time periods; An entry period in
which **subscribers** can enter and a voting period in which **all users** can vote. A user can not vote for the same entry
twice. Once the voting period begins, entries can not be edited. Once the voting period ends, the winners will be displayed 
on the winners page.


##### Creating a competition
- In order to create a competition object the [django admin interface](https://thewriters.herokuapp.com/admin/post/competition/)
 must be used.
- Validation on the competition form ensures competitions won't be created in a way that breaks code in the views.
 - The rules are;
    1. The start date can not be set in the future.
    2. The date fields must follow a consecutive order.
    3. There can only be one active competition at any time.
- Admin should also be aware that in the event of there being no entries when the entry period finishes, or no votes once
the vote period has finished, the competition will be automatically deleted from the database.

##### Side note for examiner
As we are not allowed to add anything to our projects after the hand in date I have added a competition to last the
 duration of the marking period. Unfortunately this means you will unlikely see the various stages of the competition.
 If you would like to create a competition yourself to last say ten minutes, you would be able to enter, vote
 and see the new winner at the end as well as the various differences rendered in templates throughout the different 
 stages. If you would like to do this, please do not hesitate to contact me at christoal@outlook.com. I will
 be happy to provide you with the Admin details needed to create a competition. Feel free to delete the active competition
 I have set and create your own.


## Apps
Each app houses it's respective templates, js, css and urls

### Accounts
- Serve the landing page
- Sign up by creating a user object in the register view
- Log in by authenticating users in the login view
- Log out
- Subscribe by attaching a stripe id to the user object.
    - Webhook to check if user has paid subscription fee adds four more weeks to a subscription unless the user cancels.
    - Cancel subscription
- Upload profile image and store on cloudinary

### Comments
- Comments are created in the post app as they are attached to posts in the post detail views
- Edit and delete a comment

### Pages
- Serve the home page
- Serve the about page
 
### Post
- Posts
    - Create a post object as a featured post, competition entry or private post
    - Edit post
    - Delete post
    - Create a comment object via;
        - post_detail view
        - entry_detail view
        - featured_detail view
    - A view to display a list of 6 posts per page with pagination.
    - A view to display a post 
    - Share buttons so users can share posts on social media
    
- Create a competition object via the admin interface 
    - Get a competition winner
    - Display winners list for past competitions
    - Display entry detail pages where users can vote
    - Determine competition time periods
    - Create a vote object
    
    
### Search
- Django-filter is implemented in a way that allows users to Filter posts by;
    - Username
    - Post title
    - Post category
    - Post genre
    - Tags
    - Competition
    
- Users can access posts from the filtered results and vote for competition entries from here too.

### Vote
- The vote model is kept here

## Tech Used

### Tech used includes
- [Django](https://www.djangoproject.com/)
    - **Django** is used as the framework which allows for the model-view-template (MVT) architectural pattern
- [Django-filter](https://www.djangoproject.com/)
    - **Django-filter** enables users to filter the database easily.
- [Django-forms-bootstrap](https://pypi.python.org/pypi/django-forms-bootstrap/)
    - **Django-forms-bootstrap** is used to render forms with bootstrap styles.
- [Django-smtp-ssl](https://github.com/lehins/django-smartfields)
    - **Django-smtp-ssl** the email backend that allows a user to reset a lost password.
- [Bootstrap](http://getbootstrap.com/)
    - **Bootstrap** to give the project a simple, responsive layout.
- [Pillow](https://python-pillow.org/)
    - **Pillow** enables users to upload images to their posts and profiles.
- [Stripe](https://stripe.com/gb)
    - **Stripe** is the e-commerce tech used to handle subscriptions.
- [Cloudinary](https://cloudinary.com)
    - **Cloudinary** image hosting service also allows for image hosting and manipulation. 


## Templates and Static Files

### Root templates directory
- Templates not specific to any app and used across multiple pages. 
    - Base template from which most other templates are extended from.
    - Footer included on base and landing pages.
    - Messages display django.contrib messages

- Registration Directory
    - Houses all templates pertaining to password reset
    
- Landing page
    - Log in and sign up templates in the accounts app are extended from the landing template 
    
### General templates
- Competition general directory houses the competition template included in the home page and the competition detail page.
- Post general directory houses the post detail template and the post list template which are used to display all posts
 and post lists
 
    
### Media files
- Images uploaded by a user are hosted on Cloudinary.

## Tests
Some of the validation tests I used include
- [W3C](http://validator.w3.org/)
    - **W3C** validates html.
- [jigsaw](https://jigsaw.w3.org)
    - **Jigsaw** validates css
- [pep8](http://pep8online.com/)
    - **pep8** validates python code
    
#### Testing persisting subscriptions
To test that subscriptions were being renewed automatically each month I first had to make use of the 'curl' tool to send a fake 
‘invoice.payment_succeeded’ event to the webhook locally. I followed code institute's lesson on 'renewing a subscription' 
but instead of copying the example json, I used the invoice.payment_succeeded event from my own stripe account. 
This was throwing a 500 internal server error.

I used the debugger console to look at the error in more detail and noticed the error was coming from this line:
```python
event = stripe.Event.retrieve(event_json['object']['id'])
```
From this I gathered the event was being loaded but the event variable was unable to find the event id. I double checked
the subscription_webhook file to make sure it was there and indeed it was however I noticed it was not inside of the 
object dictionary.

By changing the code to: 
```python
event = stripe.Event.retrieve(event_json['id'])
```
The webhook was then able to get the event id but was breaking with KeyError: 'customer'. I realised this meant that the 
customer value could not be found. I double checked the subscription_webhook.sh file and noticed the customer and paid
 keys I was trying to access were inside the object dict which was inside a data dict.
 
 To enable these values to be found I had to make sure I was looking in the right place:
 ```python
 cust = event_json['data']['object']['customer']
 paid = event_json['data']['object']['paid']
```

#### Unit Testing
I used django's testing framework to carry some unit tests on the following apps:
- Accounts, Pages, Post
    - test page resolves
    - test page status code
    - check content is correct

    
## Acknowledgments 
I found the following tutorials to be very helpful when creating some of the features on the site. 
- [How to create a password reset view](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html)
- [How to Filter QuerySets Dynamically](https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html)
- [Redirecting to a passed in URL using next](http://andrearobertson.com/blog/2016/10/05/django-example-redirecting-to-a-passed-in-url/)
