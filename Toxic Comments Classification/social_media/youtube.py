import numpy as np
import pandas as pd
# import streamlit as st 
from googleapiclient.discovery import build
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re 
import os

# youtube comments ertraction process
# Replace 'YOUR_API_KEY' with the API key you obtained
API_KEY = 'AIzaSyADZ3xWnP1_RBK68r7ADwKSAEY9PgxEY5E'
youtube = build('youtube', 'v3', developerKey=API_KEY)
comment=[]
authorname=[]
toxic=[]


def extract_video_id(video_url):
    # Regular expression to match the YouTube video ID
    pattern = re.compile(r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})')

    # Search for the pattern in the URL
    match = pattern.search(video_url)

    # If a match is found, return the video ID
    if match:
        return match.group(1)
    else:
        return "No id found! sorry"


def link(youtube_link):
    video_id=extract_video_id(youtube_link)
    if video_id:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=10
        )
        # print(request)
    
        while request:
            response = request.execute()
            # print(response)
            for item in response['items']:
                
                comment.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                authorname.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                # print([item])
                # print()
            if len(comment)>=100:
                break

            request = youtube.commentThreads().list_next(request, response)
            print(request)

    # tfidf=pickle.load(open("tf_idf.pkt","rb"))
    # tfidf_path = r"Toxic Comments Classification\social_media\tf_idf.pkt"
    # tfidf = pickle.load(open(tfidf_path, "rb"))

    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tfidf_path = os.path.join(project_dir, "social_media", "tf_idf.pkt")
    toxicity_model_path = os.path.join(project_dir, "social_media", "toxicity_model.pkt")

    try:
        with open(tfidf_path, "rb") as f:
            tfidf = pickle.load(f)
    except FileNotFoundError:
        print(f"File '{tfidf_path}' not found.")

    try:
        with open(toxicity_model_path, "rb") as f:
            toxicity_model = pickle.load(f)
    except FileNotFoundError:
        print(f"File '{toxicity_model_path}' not found.")
    # toxicity_model_path=r"Toxic Comments Classification\social_media\toxicity_model.pkt"
    nb_model=pickle.load(open(toxicity_model_path,"rb"))
    
    n=len(comment)
    for i in range(n):
        text_input=tfidf.transform([comment[i]]).toarray()
        prediction=nb_model.predict(text_input)
        if(prediction==1):
            toxic.append("Toxic")
        else:
            toxic.append("Non-Toxic")
    # Table={'Authors ' : authorname,
    # 'comments ' : comment,
    # 'Toxicity': toxic}
    table={}
    j=0
    for i in authorname:
           table[i]=[comment[j],toxic[j]]
           j+=1
    return table

# print(link('https://www.youtube.com/watch?v=dam0GPOAvVI')['Toxicity'])
# print(link('https://www.youtube.com/watch?v=3mZHj1tv8iY'))
