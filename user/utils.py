from django.contrib.auth.models import User
from .models import NiftyUser
from rest_framework.authtoken.models import Token

def create_user(twitter_handle, twitter_id, oauth_secret):
    """ Utility function to create a Nifty user from Twitter Oauth """

    #we use the twitter id as the username because twitter_handle can be changed
    user, created = User.objects.get_or_create(username=twitter_id)
    user.set_password(oauth_secret)
    user.save()

    n_user, created = NiftyUser.objects.get_or_create(
        user=user,
        profile_name=twitter_handle,
        handle=twitter_handle,
        twitter_user_id=twitter_id
    )

    return user, n_user

def create_token(user, oath_token):
    """ Utility function to create a Django oauth token from the Twitter token """

    token, created = Token.objects.get_or_create(user=user, key=oath_token)

    return token
