import oauth2 as oauth
import urllib2 as urllib
import ConfigParser

# See assignment1.html instructions or README for how to get these credentials

_debug = 0

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''


def twitterreq(url, method, parameters, oauth_keys):
    req = oauth.Request.from_consumer_and_token(oauth_keys["oauth_consumer"],
                                                token=oauth_keys["oauth_token"],
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1,
                     oauth_keys["oauth_consumer"], oauth_keys["oauth_token"])

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetchsamples(oauth_keys):
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters, oauth_keys)
    for line in response:
        print line.strip()


if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('twitter_api_key.cfg')
    api_key = config.get('twitter_api', 'api-key')
    api_secret = config.get('twitter_api', 'api-secret')
    access_token_key = config.get('twitter_api', 'access-token-key')
    access_token_secret = config.get('twitter_api', 'access-token-secret')
    if not api_key or not api_secret or not access_token_key or not access_token_secret:
        raise Exception('twitter api key or secret is unknown')

    twitter_api_keys = {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token_key": access_token_key,
        "access_token_secret": access_token_secret,
    }

    oauth_token = oauth.Token(
        key=twitter_api_keys["access_token_key"],
        secret=twitter_api_keys["access_token_secret"]
    )
    oauth_consumer = oauth.Consumer(
        key=twitter_api_keys["api_key"],
        secret=twitter_api_keys["api_secret"]
    )

    oauth_keys = {
        "oauth_token": oauth_token,
        "oauth_consumer": oauth_consumer,
    }

    fetchsamples(oauth_keys)
