import twitter as twt
import time
from keys import *

chirp=None

def getRemaining():
    remain = chirp.GetRateLimitStatus()
    print "Remaining API:", remain['remaining_hits'], "of", remain['hourly_limit']
    print "Resets:", time.ctime(remain['reset_time_in_seconds'])

def SelectAccount(autoauth=False):
    print "Select account: "
    for p,v in enumerate(access_token_list):
        print p, "\b)", v['name']
    nr=int(raw_input("> "))
    access_token = access_token_list[nr]
    if autoauth==True:
        return Auth(access_token)
    else:
        return access_token

def Auth(access_token):
    chirp = twt.Api(access_token['consumer_key'],
                    access_token['consumer_secret'],
                    access_token['oauth_token'],
                    access_token['oauth_token_secret'])
    return chirp

# try:
#     obj=chirp.VerifyCredentials()
# except twt.TwitterError, ex:
#     print "Fehler im Token oder bei Twitter"
#     print ex
#     sys.exit(-1)
    
#print "User %s successfully authentificated" % (obj.screen_name)
#getRemaining()
