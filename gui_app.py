import tkinter as tk
from tkinter import filedialog
import threading
import json
import requests
import random
import shutil
import os
from instabot import Bot
from PIL import Image
import praw
from bs4 import BeautifulSoup
import time

class InstagramPosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Instagram Auto Poster")
        
        # Credentials File
        tk.Label(root, text="Credentials File (.json)").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.credentials_file_entry = tk.Entry(root, width=50)
        self.credentials_file_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.load_credentials_file).grid(row=0, column=2, padx=10, pady=5)
        
        # Subreddit Names File
        tk.Label(root, text="Subreddit Names File (.txt)").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.subreddit_file_entry = tk.Entry(root, width=50)
        self.subreddit_file_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.load_subreddit_file).grid(row=1, column=2, padx=10, pady=5)
        
        # Interval
        tk.Label(root, text="Interval (In hours)").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.interval_entry = tk.Entry(root, width=10)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Run Button
        tk.Button(root, text="Run", command=self.start_posting).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Status Label
        self.status_label = tk.Label(root, text="", fg="purple")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

        # Initialize bot and Reddit client
        self.bot = None
        self.reddit = None

    def load_credentials_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.credentials_file_entry.delete(0, tk.END)
            self.credentials_file_entry.insert(0, file_path)
    
    def load_subreddit_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.subreddit_file_entry.delete(0, tk.END)
            self.subreddit_file_entry.insert(0, file_path)
    
    def start_posting(self):
        credentials_file = self.credentials_file_entry.get()
        subreddit_file = self.subreddit_file_entry.get()
        interval_hours = self.interval_entry.get()
        
        if not credentials_file or not subreddit_file or not interval_hours:
            self.status_label.config(text="Please fill in all fields.", fg="red")
            return

        try:
            interval_hours = float(interval_hours)
            if interval_hours <= 0:
                raise ValueError
        except ValueError:
            self.status_label.config(text="Interval must be a positive number.", fg="red")
            return

        # Load subreddits and check validity
        with open(subreddit_file, "r") as file:
            subreddits = file.read().strip().split(',')
        subreddit_name = random.choice(subreddits).strip()

        if not self.is_valid_subreddit(subreddit_name):
            self.status_label.config(text=f"Invalid subreddit name: {subreddit_name}", fg="red")
            return

        self.status_label.config(text="Posting Started...", fg="purple")
        self.root.update()

        # Initialize bot and Reddit client in the main thread
        self.initialize_bot_and_reddit(credentials_file)

        # Start the posting process in a separate thread
        threading.Thread(target=self.run_posting_process, args=(subreddit_file, interval_hours), daemon=True).start()

    def is_valid_subreddit(self, subreddit_name):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return not subreddit.over18  # This will raise an exception if the subreddit is invalid
        except Exception:
            return False

    def initialize_bot_and_reddit(self, credentials_file):
        # Load credentials and initialize bot and Reddit client
        with open(credentials_file, "r") as file:
            credentials = json.load(file)

        username = credentials["instagram"]["username"]
        password = credentials["instagram"]["password"]

        # Initialize bot and login
        self.bot = Bot()
        self.bot.login(username=username, password=password)

        self.reddit = praw.Reddit(
            client_id=credentials["reddit"]["client_id"],
            client_secret=credentials["reddit"]["client_secret"],
            user_agent=credentials["reddit"]["user_agent"],
            username=credentials["reddit"]["username"],
            password=credentials["reddit"]["password"],
        )

    def run_posting_process(self, subreddit_file, interval_hours):
        # Read subreddit names
        with open(subreddit_file, "r") as file:
            subreddits = file.read().strip().split(',')
        subreddit_name = random.choice(subreddits).strip()

        uploaded = []
        if os.path.exists("data.txt"):
            with open("data.txt", "r") as myfile:
                uploaded = [item.strip() for item in myfile.readlines()]

        def delete_config_folder():
            config_folder = "config"
            if os.path.exists(config_folder):
                shutil.rmtree(config_folder)

        delete_config_folder()

        def upload(link, title):
            url = f"https://best-hashtags.com/hashtag/{subreddit_name}/"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            p1_tags = soup.find_all('p1')
            hashtags = ' '.join(tag.get_text() for tag in p1_tags)

            caption_post = f'{title}\n{hashtags}'
            try:
                self.bot.upload_photo(link, caption=caption_post)
                return True
            except Exception as e:
                print(e)
                return False

        while True:
            for submission in self.reddit.subreddit(subreddit_name).new():
                print("\nChecking Submission At: ", submission.url)
                try:
                    request = requests.get(submission.url)
                except:
                    continue
                url = submission.url
                post_type = ''
                eligible = True
                if url in uploaded:
                    eligible = False
                    print("Post Already Posted", submission.url)

                if not submission.is_self and eligible:
                    if any(ext in url for ext in ["jpg", "png", "jpeg"]):
                        print("Type Detected: Image")
                        try:
                            os.remove("PostContent.jpeg.REMOVE_ME")
                        except:
                            pass
                        try:
                            img_data = request.content
                            with open('PostContent.jpeg', 'wb') as file:
                                file.write(img_data)
                            post_type = 'i'
                        except:
                            continue
                        try:
                            im = Image.open("PostContent.jpeg")
                            im = im.resize((1080, 1080))
                            im.save('PostContent.jpeg')
                        except Exception as e:
                            print(e)
                            continue
                        try:
                            print("Uploading Image...")
                            uploaded.append(submission.url)
                            with open('data.txt', 'w') as f:
                                for item in uploaded:
                                    f.write(f"{item}\n")
                            success = upload('PostContent.jpeg', submission.title)
                            if success:
                                self.update_status("Posting Completed successfully", "green")
                                time.sleep(5)
                                self.update_status(f"Sleeping for {interval_hours} hours", "purple")
                                time.sleep(interval_hours * 3600)
                        except Exception as e:
                            print(e)
            delete_config_folder()

    def update_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramPosterApp(root)
    root.mainloop()
