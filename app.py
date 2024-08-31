import os
import time
import json
import requests
import shutil
import random  # Ensure this is imported
from instabot import Bot
from PIL import Image  
import praw
from bs4 import BeautifulSoup

# Function to delete the config folder
def delete_config_folder():
    config_folder = "config"
    if os.path.exists(config_folder):
        shutil.rmtree(config_folder)

# Load Instagram and Reddit credentials and subreddits from a JSON file
with open("config.json", "r") as file:
    data = json.load(file)

# Extract credentials and subreddits
instagram_creds = data["instagram"]
reddit_creds = data["reddit"]
subreddits = data["subreddits"]

username = instagram_creds["username"]
password = instagram_creds["password"]

# Select a random subreddit from the list
subreddit_name = random.choice(subreddits).strip()

# Delete the config folder before logging in
delete_config_folder()

# Initialize the bot and login
bot = Bot()
bot.login(username=username, password=password)

# Initialize Reddit API with credentials
reddit = praw.Reddit(
    client_id=reddit_creds["client_id"],
    client_secret=reddit_creds["client_secret"],
    user_agent=reddit_creds["user_agent"],
    username=reddit_creds["username"],
    password=reddit_creds["password"],
)

uploaded = []
if os.path.exists("data.txt"):
    with open("data.txt", "r") as myfile:
        for item in myfile.readlines():
            uploaded.append(item.strip())  # Remove new lines from data returned

def upload(link, title):
    # Scraping Trending Hashtags
    url = f"https://best-hashtags.com/hashtag/{subreddit_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <p1> tags and extract the text
    p1_tags = soup.find_all('p1')
    hashtags = ' '.join(tag.get_text() for tag in p1_tags)  # Join all hashtags into a single string

    caption_post = f'{title}\n{hashtags}'  # Remove the credits part, only hashtag and caption
    try:
        bot.upload_photo(link, caption=caption_post)
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
            continue
        url = submission.url
        eligible = True
        for x in uploaded:  # Checking if post has already been uploaded
            if url in x:
                eligible = False
                print("Post Already Posted", submission.url)

        if not submission.is_self and eligible:  # Making sure the post is not a text post
            if any(ext in url for ext in ["jpg", "png", "jpeg"]):
                print("Type Detected: Image")
                try:
                    os.remove("PostContent.jpeg.REMOVE_ME")  # Attempt to remove this file as it causes errors
                except:
                    print("No remove me file found")
                try:
                    img_data = request.content  # Storing image data
                    with open('PostContent.jpeg', 'wb') as file:  # Image name
                        file.write(img_data)
                    post_type = 'i'
                except:
                    continue
                try:
                    print("Resizing the image...")  # Resizing image size to fit aspect ratio
                    im = Image.open("PostContent.jpeg")
                    newsize = (1080, 1080)
                    im1 = im.resize(newsize)
                    im1.save('PostContent.jpeg')
                except Exception as e:
                    print(e)
                    print("Error while resizing")

                try:
                    print("Uploading Image...")
                    uploaded.append(submission.url)  # Adding URL to the data file
                    with open('data.txt', 'w') as f:
                        for item in uploaded:
                            f.write(f"{item}\n")
                    upload('PostContent.jpeg', submission.title)
                except Exception as e:
                    print(e)
        else:
            print("Ignoring Text Post At:", submission.url)

    # Delete the config folder after each run
    delete_config_folder()
