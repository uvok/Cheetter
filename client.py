from header import *
import pprint
import os
import sys
import textwrap

splitlenght=80
headerwidth=splitlenght+20

def Decision():
    """  Returns 1 for next, 2 for replay, 0 for main menu """
    print "[n]ext page, [r]eply to a tweet, [b]ack to main menu\n?> ",
    dec={"n":1, "r":2, "b":0}
    a=""
    a=raw_input()
    try:
        return dec[a]
    except KeyError:
        print "Falsche Eingabe"
        return Decision()

def postReply(msg):
    """ Post a reply

    msg (message object to reply to) """
    
    repl_id=msg.id
    repl_name=msg.user.screen_name
    repl_text=msg.text
    print "reply to: [%s] %s" % (repl_name, msg.text)
    rt=raw_input(":> @{0} ".format(repl_name))
    extra_text="@"+repl_name+" "+u"\u2026"
    split_length=135-len(extra_text.encode("utf-8"))
    replist=textwrap.wrap(rt, split_length)
    maxind=len(replist)-1
    n=-1
    for i in replist:
        n+=1
        if maxind-n: ## continued mode
            reply="@{0} {1}{2}".format(repl_name, i, u"\u2026".encode("utf-8"))
        else: ## non-continued mode
            reply="@{0} {1}".format(repl_name, i)
        postUpdate(reply, repl_id)

def postUpdate(txt=None, irt_id=None):
    """ Post a status message

    text (string) - text of message
    irt_id (int)  - status ID to reply to"""
    
    #arg={"in_reply_to_status_id":irt_id}
    if txt:
        msg=txt
        print "Sending message: \"%s\"" % (msg),
        if irt_id: print "(REPLY)",

        try:
            a=raw_input("\nokay? ")
        except KeyboardInterrupt:
            print "Abbruch"
            return
        if a!="y":
            return
    else:
        msg = raw_input("Status?: ")
        
    try:
        succ = chirp.PostUpdates(str(msg), u'\u2026'.encode('utf-8'), in_reply_to_status_id=irt_id) ###may fail
    except IndexError:
        print "Index error. You typed something, didn't you?"
        return
    except twt.TwitterError:
        print "Twitter-Fehler"
        return
    for i in succ:
        pprint.pprint(i.__dict__)

def printHome(pg=1, count=40):
    """ Prints home timeline) """
    print headerwidth*'+'
    print " Home Timeline ".center(headerwidth, '+')
    print headerwidth*'+'
    hom=chirp.GetFriendsTimeline(count=count, page=pg)
    print len(hom)
    printMessageObject(hom)

    ho=Decision()
    if ho==1:
        printHome(pg=pg+1)
    elif ho==2:
        nr=int(raw_input("Reply to status # "))
        try:
            postReply(hom[nr])
        except KeyError:
            print "Falsche Eingabe!"
    else:
        return

def printReplies(pg=1, amnt=20):
    """ Prints replies

    pg (int) - page to fetch
    amnt (int) - amount of replies on page nr to fetch"""
    
    print headerwidth*'#'
    print " @replies ".center(headerwidth, '#')
    print headerwidth*'#'
    reps=chirp.GetReplies(page=pg)

    while True:
        printMessageObject(reps[0:amnt])
    
        re=Decision()
        if re==1:
            printReplies(pg+1)
        elif re==2:
            nr=int(raw_input("Reply to status # "))
            try:
                postReply(reps[nr])
            except IndexError:
                print "Falsche Eingabe!"
        else:
            return

def printDMs(pg=1, amnt=20):
    """ Prints DMs

    pg (int) - page to fetch
    amnt (int) - amount of direct messages on page nr to fetch"""

    print headerwidth*'*'
    print " DMs ".center(headerwidth, '*')
    print headerwidth*'*'
    dms=chirp.GetDirectMessages(page=pg)
    printMessageObject(dms[0:amnt])
    re=Decision()
    if re==1:
        printDMs(pg+1)
    elif re==2:
        postDM() ## TODO: PostDM
    else:
        return

def printLine(name, text, continued=False):
    """ Print a line w/ a status message

    name (string) - screen name
    text (string) - text of status message
    continued (bool) - Is output continued from a previous line?"""
    if continued==False:
        print "[%s] %s" % (name.center(20), text)
    else:
        print " ".ljust(22), text

def printMessageObject(msgs):
    """ Prints status objects or DMs

    msgs (list) - list of message objects"""
    
    i=0
    for msg in msgs:
        prefix=" ("+str(i).center(2)+") "
        if isinstance(msg, twt.Status):
            sender=msg.user.screen_name
            content=prefix+msg.text
        elif isinstance(msg, twt.DirectMessage):
            sender=msg.sender_screen_name
            content=msg.text
        else:
            print "error"
            exit()
            
        cont=False
        spltxt=textwrap.wrap(content, splitlenght) ## splrep ist der Text!!
        for j in spltxt:
            printLine(sender, j[0:splitlenght], cont)
            if len(j)>splitlenght:
                printLine(sender, j[splitlenght:140], True)
            cont=True
        i+=1

def main():
    menu=( ("Quit", exit),
           ("Print Home Timeline", printHome),
           ("Post Update",postUpdate),
           ("Print Replies",printReplies),
           ("Print DMs",printDMs) )

    # Print Menu Selection
    for num, tup in enumerate(menu):
        if num==0: continue
        print num, "\b)", tup[0]
    print "\n0) Quit"
    selec=raw_input(">>>")
    
    if selec.isdigit()==True:
        selec=int(selec)
        if selec>0 and selec<len(menu):
            menu[selec][1]()
            main()
#        elif selec==0:
#           exit(0)
        else:
            pass

if __name__ == "__main__":
    chirp=SelectAccount(True)

    if len(sys.argv) > 1:
        postUpdate(" ".join(sys.argv[1:]))
    else: main()
