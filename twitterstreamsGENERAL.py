#if oauth2 and urllib not installed yet :
#easy_install oauth2
#easy_install urllib2
#SEND DATA TO A NEW JSON FILE RUN BY :

# if not done before 
#easy_install oauth2
# python twitterstreams.py > newtwits.json 
#this one only pick up the twitts mentioning markit

import oauth2 as oauth
import urllib2 as urllib
import sys
import time
# See Assginment 6 instructions or README for how to get these credentials
access_token_key = "ACCESS_TOKEN_KEY"
access_token_secret = "ACCESS_TOKEN_SECRET"

consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "POST"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request.
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
  
  

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

  #return response.encode('utf8')

  return response
def fetchsamples():

 url="https://stream.twitter.com/1.1/statuses/filter.json?track=rugby,VI+nations"# nokia+map,nokkia+maps,nokia,google+map,apple+map,maps"
 parameters = []
 files = open("results_rugby.csv","a")
 try:
   response = twitterreq(url, "POST", parameters)
   for line in response:
  	files.write(line) #
   print line.strip()
   sys.stdout.flush()
 except:
  pass

	#sys.stdout.write(line.strip())
if __name__ == '__main__':
  fetchsamples()