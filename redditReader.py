#Creator: Serenity
#Created Date: 1/19/16
#Things needed to be improved:
#error handling if a bad subreddit is put in
#the ability to comment
#the ability to rechoose subreddit without relaunching program
#the ability to up vote

#library to handle reddit api
import praw
#handle screen clearing
import os
#color code things
from colorama import Fore, Back, Style
#how to look at pictures automagically!
from PIL import Image
import requests
from StringIO import StringIO
#how to open webbrowsers automagically!
import webbrowser

#Rename the color scheme to something easier
red = Fore.RED
green = Fore.GREEN
pink = Fore.MAGENTA
blue = Fore.BLUE
yellow = Fore.YELLOW
reset = Style.RESET_ALL

#Acceptable image extensions
imgExt = ['.jpg', '.png']

#define their choices as a global variable so we can use it anywhere
choices = []

#Create function for printing comments/replies
def checkComments(comments):
    #sets a counter to slowly go through comments so they are readable
    counter = 0
    for comment in comments:
        counter += 1
        if counter % 3 == 0:
            choice = raw_input(red + "Do you want to continue reading comments?: (y for yes)" + reset)
            if choice != 'y':
                return
        print yellow + str(comment.author)+ ": " + reset + comment.body
        print "********************"
        #If a comment has replies, go get them
        if(len(comment.replies) > 0):
            depth = 1
            getReplies(comment.replies, depth)

def getReplies(replies, depth):
    #Max depth of replies on a comment on reddit is 9
    if depth > 9:
        return
    for reply in replies:
        print depth * "    " + yellow + str(reply.author)+ ": " + reset+ reply.body
        print "********************"
        #If a reply has a reply go through the same steps as above
        if len(reply.replies) > 0:
            getReplies(reply.replies, depth+1)

def getComments(idNum):
    choice = raw_input(red + "Do you want to read the comments? (y for yes):" + reset)
    if (choice == 'y'):
        submission = r.get_submission(submission_id=idNum)
        checkComments(submission.comments)

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print pink + "Welcome to Serenity's Reddit Reader!"
    print "Here you can spend dangerous amounts of time.... "
    print "But first! You must choice what you want to do!"
    print reset
    subredditChoice = raw_input("Name you flavor of Reddit: ")
    typeOfPosts = raw_input("Hot or New?: (type each word as you see it) ")
    openBrowser = raw_input("Automatically open web browser for links that aren't pictures? (yes or no): ")
    print "Great! Now that I have all your data, here is a few reminders!"
    print "You can type 'm' any time to come back to this menu to choose differently"
    print "Good luck being productive today!"
    raw_input("Press any key to continue")
    global choices
    choices = [subredditChoice, typeOfPosts, openBrowser]
    return choices

def displayPic(url):
    Image.open(StringIO((requests.get(url)).content)).show()


def browseReddit(subreddit):
    global choices
    for x in subreddit:
		#checks if subreddit entered is good or bad
        if(x.title == None):
            print "You entered a bad subreddit, there is no info!"
            break
		#skips over stickied posts because no one wants to see them
        if(str(x.stickied) == "True"):
            continue
		#clears screen for both windows and linux
        os.system('cls' if os.name == 'nt' else 'clear')
        print blue + "Title: " + reset + x.title
        print blue + "Author: " + reset + str(x.author)
        if x.selftext != '': 
            print blue + "Text: " + reset + x.selftext
		#Tries to figure out if it is an image, if it isn't is it text on
		#reddit? Probably just text then so don't pop open a browser
		#It isn't an image, but it isn't reddit, open a browser, open it!
		#Unless you told it not to earlier
        if any(img in x.url for img in imgExt):
            displayPic(x.url)
        elif ("reddit" not in x.url and choices[2].lower() == 'yes'):
            webbrowser.open(x.url, autoraise=False)
        else:
            print blue + "URL: " + reset + str(x.url)
        print blue + "Number of Comments: " + reset + str( x.num_comments)
        if (x.num_comments > 0):
            getComments(x.id) 
        choice = raw_input(green + "Move to next one? (y for yes):"+ reset)
        if (choice.lower() == 'm'):
            getNewReddit()
        elif (choice != 'y'):
            print "Okaaayyy BYEEEEE"
            return

def getReddit(choices):
    if choices[1].lower() == "hot":
        subreddit = r.get_subreddit(choices[0].lower()).get_hot(limit = 1000)
    elif choices[1].lower() == "new":
        subreddit = r.get_subreddit(choices[0].lower()).get_new(limit = 1000)
    else: 
        print "Okay now you broke me... "
        exit(0)
    return subreddit

def getNewReddit():
    newSub = raw_input(yellow + "So I hear you want a new subreddit? Press y to confirm: " + reset)
    if (newSub == 'y'):
        browseReddit(getReddit(menu()))
    else:
        exit()



#Set user agent string and start an instance of reddit
user_agent = ("Serenity Test v0.1")
r = praw.Reddit(user_agent = user_agent)
#create a subreddit reader
#Use 
#choices = menu()
#subreddit = getReddit(choices)
#browseReddit(subreddit)
browseReddit(getReddit(menu()))



#2orurx
#41uk11
