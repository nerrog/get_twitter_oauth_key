from multiprocessing import Process
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import webbrowser, argparse ,web_server, pprint

CK = ""
CS = ""

def yes_no_input(txt):
    while True:
        choice = input(txt).lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

def gen_auth_url(consumer_key, consumer_secret, oauth_callback):
    print("Generating the URL for authentication...")

    CK = consumer_key
    CS = consumer_secret

    twitter = OAuth1Session(consumer_key, consumer_secret)

    response = twitter.post(
        "https://api.twitter.com/oauth/request_token",
        params={'oauth_callback': oauth_callback}
    )
    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    authenticate_url = "https://api.twitter.com/oauth/authenticate"
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    print("Authentication url: "+authenticate_endpoint)
    webbrowser.open(authenticate_endpoint)
    print("Waiting for authentication...")
    proc = Process(target=web_server.run_server)
    proc.start()

def http_callback(list):
    print("Generating access token...")

    twitter = OAuth1Session(
        CK,
        CS,
        list[0],
        list[1],
    )

    response = twitter.post(
        "https://api.twitter.com/oauth/access_token",
        params={'oauth_verifier': list[1]}
    )

    access_token = dict(parse_qsl(response.content.decode("utf-8")))
    print("Access token token successfully generated!")
    print("===ACCESS TOKEN===")
    pprint.pprint(access_token)
    print("==================")
    print("Bye")


def main() -> None:
    print("get_twitter_oauth_key\nBy YU-PEI")
    parser = argparse.ArgumentParser(description='Easy to generate Twitter API OAuth keys.')

    parser.add_argument('CK', help='TwitterAPI Consumer key')
    parser.add_argument('CS', help='TwitterAPI Consumer secret')
    parser.add_argument('callback', help='TwitterAPI OAuth_callback')

    args = parser.parse_args()

    gen_auth_url(args.CK, args.CS, args.callback)

if __name__ == "__main__":
    main()