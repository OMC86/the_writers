# The Writers

## Overview

### What is the purpose of this site?

The Writers is an online community for people who want to share their writing talents, discuss what they have written
with those who read their posts and possibly win some money entering writing competitions.

### What can users do?

#### General users
The site allows users to register and log in. Once users are logged in they can create posts, choosing whether
or not to make their posts public. Once a post is published, other authenticated users are able to post comments on it.
Users are also allowed to vote for competition entries they think deserve to win.

#### Subscribed users
While subscribers enjoy the same privileges as general users, they also get the added benefit of entering their posts
in to competitions in which they can win a cash prize.


### Admin
The administrator has permissions to delete and edit posts and is also in charge of creating competitions.

#### Competitions
Competitions are held on the site at the discretion of the admin. They consist of two time periods; An entry period in
which **subscribers** can enter and a voting period in which **all users** can vote. A user can not vote for the same entry
twice. Once the voting period begins, entries can not be edited. Once the voting period ends, the winners will be displayed 
on the winners page.

#### Creating a competition
- In order to create a competition object the [django admin interface](https://thewriters.herokuapp.com/admin/post/competition/)
 must be used.
- There can only be one competition at any time. Due to the validation, once a competition is active it can not be edited.
If a mistake has been made there are two options.
    - Delete the competition and create a new one.
    - In order to edit with out deleting go to post/admin.py comment out **lines 25 and 26** and push to git. Once the
    amendment has been made, save the competition, then simply remove the comments and push to git once more.
    ```python
        elif comp.is_active():
            raise forms.ValidationError('Only one active competition is permitted at a time')

- Admin should also be aware that in the event of there being no entries when the entry period finishes, or no votes once
the vote period has finished, the competition will be automatically deleted from the database.
- The date fields in the competition form must follow a consecutive order from the begining of the entry period to
 the end of the voting period in order for the competition to be saved.

## Features

- Site Based Features
    - Sign up
    - Subscribe
    - Log in
    - Log out
    - Post, edit, delete objects
    - Filter search
    - Form validation
    - Image handling
    - Password reset
    - Calculate the competition prize
    - Get the winner/winners of a competition
    - Delete a competition
    
- User Based Features
    - Write a post
    - Edit and delete a post
    - Publish a post
    - Write a comment
    - Edit and delete a comment
    - Enter a post in an active competition
    - Vote for a competition entry
    - Read published posts
    - Search for specific posts
    - Share posts on social media
    

## Tech Used

### Tech used includes
- [Django](https://www.djangoproject.com/)
    - **Django** is used as the framework which allows for the model-view-template (MVT) architectural pattern
- [Django-filter](https://www.djangoproject.com/)
    - **Django-filter** enables users to filter the database easily.
- [Django-forms-bootstrap](https://pypi.python.org/pypi/django-forms-bootstrap/)
    - **Django-forms-bootstrap** is used to render forms with bootstrap styles.
- [Django-smartfields](https://github.com/lehins/django-smartfields)
    - **Django-smartfields** is used to resize images.
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


## Apps
Each app houses it's respective templates, js, css and urls

### Accounts
- Serve the landing page
- Create a user object
- Authenticate users
- Handle subscriptions
- Upload profile image

### Comments
- Create a comment object
- Edit and delete a comment

### Pages
- Serve the home page
- Serve the about page
 
### Post
- Create a post object
    - Edit post
    - Delete post
    - Serve post list pages
    - Serve post detail pages
    
- Create a competition object
    - Get a competition winner
    - Serve competition winner list
    - Serve competition detail pages
    - Determine competition time periods
    - Cast vote
    
- Create a vote object
    
### Search
- Filter database
- Serve the detailed post view from filtered objects

### Vote
- House the vote model

## Templates and Static Files

### Root templates directory
- Templates not specific to any app and used across multiple pages. 
    - Base template from which most other templates are extended from.
    - Footer is rendered on all pages but the landing page
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
- [Nibbler](http://nibbler.silktide.com/)
    - **Nibbler** gives you a report scoring a website out of 10 for various criteria.
- [W3C](http://validator.w3.org/)
    - **W3C** validates html.
- [Wave Accessibility Tool](http://wave.webaim.org/)
    - **Wave accessibility tool**  highlights areas of a page which can be made more accessible.

## Acknowledgments 
- I found the following tutorials to be very helpful when creating some of the features on the site. 
- [How to create a password reset view](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html)
- [How to Filter QuerySets Dynamically](https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html)
- [Redirecting to a passed in URL using next](http://andrearobertson.com/blog/2016/10/05/django-example-redirecting-to-a-passed-in-url/)





    

