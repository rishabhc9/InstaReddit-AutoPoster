# InstaReddit AutoPoster

## Overview

Introducing **InstaReddit AutoPoster** – the ultimate tool to effortlessly boost your Instagram feed! Say goodbye to manual posting and hello to automation. This powerful tool grabs stunning image posts from your favorite subreddits and schedules them for automatic upload to Instagram at your chosen intervals. With an intuitive Tkinter GUI and seamless Reddit integration via PRAW, InstaReddit AutoPoster makes it easy to keep your Instagram fresh and engaging without lifting a finger. Dive into hassle-free social media management and let InstaReddit AutoPoster do the heavy lifting for you!

## Features

- **Load Credentials**: Input Instagram and Reddit credentials from a JSON file.
- **Select Subreddits**: Choose a file containing subreddit names.
- **Set Posting Interval**: Define the interval between posts in hours.
- **Automatic Hashtag Scraping**: Scrapes hashtags based on the selected subreddit name and includes them in the Instagram post captions.
- **Post Automation**: Automatically fetches images from Reddit subreddits and posts them to Instagram.
- **Error Handling**: Provides status updates and error messages on the GUI.

## Requirements

- Python 3.6 or higher
- Instabot
- PRAW
- Pillow
- Requests
- BeautifulSoup4
- Tkinter

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/instagram-poster.git
   cd instagram-poster
   ```
2. **Install Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Create a credentials.json file with the following structure:**

   ```bash
   {
     "instagram": {
       "username": "your_instagram_username",
       "password": "your_instagram_password"
     },
     "reddit": {
       "client_id": "your_reddit_client_id",
       "client_secret": "your_reddit_client_secret",
       "user_agent": "your_reddit_user_agent",
       "username": "your_reddit_username",
       "password": "your_reddit_password"
     }
   }
   ``` 
4. **Create a Subreddit Names File: Prepare a .txt file with subreddit names, one per line or comma-separated.**
   ```bash
   dankmemes,dankinindia,
   ```

5. **Run the script:**

   ``` bash
   python app.py
   # or
   python gui_app.py
   ```

## Usage:

1. Load Credentials File: Click the "Browse" button next to "Credentials File (.json)" and select your credentials.json file.

2. Select Subreddit Names File: Click the "Browse" button next to "Subreddit Names File (.txt)" and select your subreddit names file.

3. Set Posting Interval: Enter the interval between posts in hours.

4. Start Posting: Click the "Run" button to start the posting process. The tool will begin fetching images from the selected subreddits and uploading them to Instagram at the specified interval.

5. Check Status: The status label at the bottom of the GUI will provide updates on the posting process, including any errors or confirmation messages.


###

For any questions or issues, please contact:  [rishabhchopda79@gmail.com](rishabhchopda79@gmail.com).

