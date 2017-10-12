from __future__ import division

from django.shortcuts import render_to_response
from django.http import HttpResponse



import sys
import json
import praw

from textblob import TextBlob

#Reddit API
reddit = praw.Reddit(client_id='SNFZ3rpEE84D5w',
                        client_secret='UdXX4thJdhHhjuXVZkLwFhCdcXQ',
                        redirect_uri='http://localhost:8080',
                        user_agent='testscript by /u/thefissure')
                        
                        
# Handles subreddit information such as #comments and karma
class SubredditInfo:
    def __init__(self, name):
        self.name = name
        self.num_comments = 0
        self.positive=0
        self.negative=0
        self.karma=0
    
    def add_comment(self, pol, karma):
        self.num_comments += 1
        if (pol > 0):
            self.positive += 1
        elif (pol < 0):
            self.negative += 1
        self.karma += karma
        
    def __repr__(self):
        return "Subreddit: " + str(self.name) + ", total#: " + str(self.num_comments) + \
                ", pos: " + "{0:.2f}".format(self.positive / self.num_comments) + \
                ", neg: " + "{0:.2f}".format(self.negative / self.num_comments) + ", total karma: " + str(self.karma)



def index(request):
    
    username = request.GET['username']
    
    user = reddit.redditor(username)
    
    #List of SubredditInfo objects
    listSubreddits = []
    
    
    # Use PRAW to parse all the reddit comments for one User
    for comment in user.comments.new(limit=20):
        print (comment.subreddit)
        print (comment.body)
        print (comment.score)
        
        analysis = TextBlob(comment.body)
        print (analysis.sentiment.polarity)
        
        if any(x.name == comment.subreddit for x in listSubreddits):
            for sub in listSubreddits:
                if sub.name == comment.subreddit:
                    sub.add_comment(analysis.sentiment.polarity, comment.score)
            
        else:
            temp = SubredditInfo(comment.subreddit)
            temp.add_comment(analysis.sentiment.polarity, comment.score)
            listSubreddits.append(temp)
            
    
    newlist = sorted(listSubreddits, key= lambda x: x.positive/x.num_comments, reverse=True)
    filtered = [elem for elem in newlist if elem.num_comments > 5]
    
    print (filtered)
    
    
    
    resultList = []
    for x in newlist:
        
        tup = []
        tup.append(str(x.name))
        tup.append(str(x.num_comments))
        tup.append(str(x.positive))
        tup.append(str(x.negative))
        tup.append(x.karma)
        print tup
        resultList.append(tup)
        
    print resultList
    
    return render_to_response('index.html', {"list": resultList})
    
    
#def results(request):
 #   username = request.GET['username']
  #  
   # print username

# Create your views here.
