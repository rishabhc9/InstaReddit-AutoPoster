import glob
import os
import sys
import time
import json
import requests
import urllib.request
import random
import shutil
from instabot import Bot
from PIL import Image  
import praw
from bs4 import BeautifulSoup

# Function to delete the config folder
def delete_config_folder():
    config_folder = "config"
    if os.path.exists(config_folder):
        shutil.rmtree(config_folder)

# Load Instagram and Reddit credentials from a JSON file
with open("credentials.json", "r") as file:
    credentials = json.load(file)

username = credentials["instagram"]["username"]
password = credentials["instagram"]["password"]

# Read subreddit names from subReddits.txt and select a random one
with open("subReddits.txt", "r") as file:
    subreddits = file.read().strip().split(',')
subreddit_name = random.choice(subreddits).strip()

# Delete the config folder before logging in
delete_config_folder()

# Initialize the bot and login
bot = Bot()
bot.login(username=username, password=password)

# Initialize Reddit API with credentials
reddit = praw.Reddit(
    client_id=credentials["reddit"]["client_id"],
    client_secret=credentials["reddit"]["client_secret"],
    user_agent=credentials["reddit"]["user_agent"],
    username=credentials["reddit"]["username"],
    password=credentials["reddit"]["password"],
)

uploaded = []
with open("data.txt", "r") as myfile:
    for item in myfile.readlines():
        uploaded.append(item.replace('\n', ''))  # Remove new lines from data returned

def Upload(link, title):
    # Scraping Trending Hashtags
    url = f"https://best-hashtags.com/hashtag/{subreddit_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <p1> tags and extract the text
    p1_tags = soup.find_all('p1')
    hashtags = ' '.join(tag.get_text() for tag in p1_tags)  # Join all hashtags into a single string

    captionPost = f'{title}\n{hashtags}'  # Remove the credits part, only hashtag and caption
    try:
        bot.upload_photo(link, caption=captionPost)
        print("Sleeping for 3 hours")
        time.sleep(3 * 60 * 60)  # Sleep after posting for 3 hours to avoid spamming API
    except Exception as e:
        print(e)
        print("Something went wrong")

while True:
    for submission in reddit.subreddit(subreddit_name).new():  # Use the specified subreddit
        print("\nChecking Submission At: ", submission.url)
        try:
            request = requests.get(submission.url)
        except:
            pass
        url = submission.url
        postType = ''
        Eligible = True
        for x in uploaded:  # Checking if post has already been uploaded
            if url in x:
                Eligible = False
                print("Post Already Posted", submission.url)

        if submission.is_self == False and Eligible == True:  # Making sure the post is not a text post
            if "jpg" in url or "png" in url or "jpeg" in url:
                print("Type Detected: Image")
                try:
                    os.remove("PostContent.jpeg.REMOVE_ME")  # Attempt to remove this file as it causes errors
                except:
                    print("No remove me file found")
                try:
                    img_data = request.content  # Storing image data
                    file = open('PostContent.jpeg', 'wb')  # Image name
                    file.write(img_data)
                    name = file.name
                    postType = 'i'
                    file.close()
                except:
                    pass
                try:
                    print("Resizing the image...")  # Resizing image size to fit aspect ratio
                    im = Image.open("PostContent.jpeg")
                    newsize = (1080, 1080) 
                    im1 = im.resize(newsize)
                    im.save('PostContent.jpeg')
                except Exception as e:
                    print(e)
                    print("Error while resizing")

                try:
                    print("Uploading Image...")
                    file = open('PostContent.jpeg', 'rb')
                    name = file.name
                    file.close()
                    uploaded.append(submission.url)  # Adding URL to the data file
                    with open('data.txt', 'w') as f:
                        for item in uploaded:
                            f.write(f"{item}\n")
                    Upload(name, submission.title)
                except Exception as e:
                    print(e)
        else:
            print("Ignoring Text Post At:", submission.url)

    # Delete the config folder after each run
    delete_config_folder()
