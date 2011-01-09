import twitter as twt
import pprint
import os
import urlparse
import urllib
import string
import pickle
import time
from header import *

DestDir="/home/andreas/pyt/imgs-fullsize"
OldFile="/home/andreas/pyt/clienttry/oldUU.dat"
#NewFile="/home/andreas/pyt/clienttry/newUU.dat"

def chunks(l, n):
    """ Return a list of lists, each w/ n elements """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def DeleteOld(newdict, olddict):
    """ Delete pictures of user not in newlist anymore """
    print "Deleting old pictures..."
    for scr_name in olddict:
        if scr_name in newdict:
            # user is still in list, do nothing
            pass
        else:
            PicUrl=olddict[scr_name]
            rmfilename=scr_name+"."+getEnding(PicUrl)
            print "!!!![DELETING]!!!!: avatar of %s" % (scr_name)
            try:
                os.remove(rmfilename)
            except OSError:
                print "Datei nicht vorhanden. hm? Shouldn't happen."

def getFilename(url):
    """ gets (real) filename from URL """
    spliturl = urlparse.urlsplit(url)
    path = spliturl.path
    parts = string.split(path, "/")
    filename=parts[-1]
    return filename
    
def getEnding(url):
    """ Gets ending of a file from an URL """
    filename=getFilename(url)
    ending=string.split(filename, ".")[-1]
    return ending

def GetFollFrie(type):
    """ Get List of user objects"""
    if type=="Followers":
        friend_page = chirp.GetFriendIDs()
    elif type=="Friends":
        friend_page = chirp.GetFollowerIDs()
    else: return
    print "###########  %s  #############" % (type)
    #friendpage is a list of ids
    cnt=0
    ids = friend_page['ids']
    split_id_list = list(chunks(ids, 100))
    userinfolist=list()
    for x in split_id_list: # every x contains a list of 100 user objects
        cnt+=1
        print "Fetching set %s of %s ..." % (cnt, len(split_id_list))
        userinfolist.extend(chirp.UsersLookup(x))
        
    #userinfolist enthaelt jetzt Benutzerobjekte aller friends / followers
    return userinfolist
        
def GetUserUrlDict(users):
    """ Get dictionary of screen_name:pictureURLs pairs """
    UserUrlPair={}
    for i in users:
        UserUrlPair[i.screen_name]=i.profile_image_url
    return UserUrlPair

def GetFullSizeUrl(url):
    if "default_profile" in url:
        print 5*"\b", "def!"
        return url
    if "_normal" in url:
        rpos=url.rfind("_normal")
        be4=url[:rpos]
        after=url[rpos:]
        after=after.replace("_normal", "")
        fullsize=be4+after
        return fullsize
    else:
        print 10*"\b", "nonormal!"
        return url

def GetPic(UUdict):
    """ Actually Fetch pictures """

    if os.path.exists(DestDir):
        os.chdir(DestDir)
    elif os.path.isfile(DestDir):
        os.chdir(DestDir+".isadirectory")

    if os.path.isfile(OldFile):
        fi=open(OldFile)
        old=pickle.load(fi)
        fi.close()
    else:
        print "No old file found, starting from anew"
        old={}

    # function for deleting old files
    DeleteOld(UUdict, old)
    
    for cnt,scr_name in enumerate(UUdict):
        PicUrl=UUdict[scr_name]
        dest_filename=scr_name+"."+getEnding(PicUrl)
        state="{0:<3} of {1} [%s]: {2}".format(cnt+1, len(UUdict), dest_filename)

        # avatar of follower not yet on disk
        if os.path.isfile(dest_filename)==False:
            print state % ("Fetching".ljust(15))
            urllib.urlretrieve(GetFullSizeUrl(PicUrl), dest_filename)
            time.sleep(1)

        # Check if URL changed
        elif scr_name in old and PicUrl!=old[scr_name]:
            print state % ("Replacing".ljust(15))
            urllib.urlretrieve(GetFullSizeUrl(PicUrl), dest_filename)
            time.sleep(1)
            
        # already fetched - actually no reason for extra testing, else would do?
        elif os.path.isfile(dest_filename)==True \
                 and scr_name in old \
                 and PicUrl==old[scr_name]: 
            # file w/ screen_name exists,
            # screen_name is in both old and new lists
            # URL hasn't chenged
            print state % ("Already Fetched".ljust(15))

        elif scr_name not in old \
                 and os.path.isfile(dest_filename)==True: 
            # screen_name not in old list
            # but file w/ screen_name already exists
            print state % ("Refetching".ljust(15))
            urllib.urlretrieve(GetFullSizeUrl(PicUrl), dest_filename)
            time.sleep(1)
            
        else:
            print "other kind of error?"

    # write UrlDictPair to file
    fi=open(OldFile, "wb")
    pickle.dump(UUdict, fi)
    fi.close()

def GetFollPic(FriendUU):
    print 10*"#"
    print "Fetching Followers Pics"
    print 10*"#"
    GetPic(FriendUU)

def GetFriendPic(FollUU):
    print 10*"*"
    print "Fetching Friends Pics"
    print 10*"*"
    GetPic(FollUU)

def main():
    foll=GetFollFrie("Followers")
    frie=GetFollFrie("Friends")

    FoDict=GetUserUrlDict(foll)
    if FoDict==None or FoDict=={}:
        print "Dict empty?"
        raise Exception, "Empty Dict or not a dict"
   
    FrDict=GetUserUrlDict(frie)
    if FrDict==None or FrDict=={}:
        print "Dict empty?"
        raise Exception, "Empty Dict or not a dict"

    UUDict=dict(FoDict.items() + FrDict.items())
    GetPic(UUDict)

chirp=SelectAccount(True)
main()
