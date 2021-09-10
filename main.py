import tweepy
import time

key = ''
secret = ''


def unfollow_muted_users():
    api = authenticate_user()
    unfollow_muted_users_you_follow(api)


def authenticate_user():
    auth = tweepy.OAuthHandler(key, secret)
    redirect_url = auth.get_authorization_url()
    print('You must give access to this application through the following url: ' + redirect_url)
    code = input("Once you have given this app access to your account, provide the code given back to you: ")
    code = code.strip()
    try:
        auth.get_access_token(code)
    except tweepy.TweepError:
        print('Error! Failed to get access token. Possibly an incorrect code was entered.')
    finally:
        authenticated = tweepy.OAuthHandler(key, secret)
        authenticated.set_access_token(auth.access_token, auth.access_token_secret)
        api = tweepy.API(authenticated)
        return api


def unfollow_muted_users_you_follow(api):
    followIds = api.friends_ids()
    cursor = -1
    nextSet = True
    i = 0
    j = 0
    while nextSet:
        if i > 15 or j > 50:
            time.sleep(900)
            i = 0
            j = 0

        mutes = api.mutes(cursor=cursor)
        i += 1
        users = mutes[0]
        cursor = mutes[1][1]
        if len(users) < 20:
            nextSet = False
        for user in users:
            if user.id in followIds:
                print(user.screen_name)
                try:
                    api.destroy_friendship(user.id)
                    j += 1
                except tweepy.TweepError:
                    print('Failed to remove a user from follow list: ' + id)

    print('Successfully unfollowed all muted accounts.')


if __name__ == '__main__':
    unfollow_muted_users()
