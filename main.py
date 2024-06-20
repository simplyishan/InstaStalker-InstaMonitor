import requests
import logging
import instaloader
import json
import sys
import os
import time

class Foundation:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.load_credentials()
        self.load_proxies()

    def load_credentials(self):
        try:
            with open('credentials.json', 'r', encoding='utf-8') as cred_file:
                credentials = json.load(cred_file)
                self.instagram_username = credentials.get('instagram_username')
                self.instagram_password = credentials.get('instagram_password')
                self.discord_webhook_url = credentials.get('discord_webhook_url')
                self.target_username = credentials.get('target_username')
                self.monitoring_interval_hours = credentials.get('monitoring_interval_hours', 1)
                print("Loaded credentials:")
                print(f"Instagram Username: {self.instagram_username}")
                print(f"Target Username: {self.target_username}")
                print(f"Monitoring Interval: {self.monitoring_interval_hours} hours")
        except FileNotFoundError:
            self.logger.error("Credentials file not found.")
            sys.exit(1)

    def load_proxies(self):
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as file:
                self.proxies = [line.strip() for line in file if line.strip()]
        else:
            self.proxies = []

    def ensure_proxies_work(self):
        valid_proxies = []
        for proxy in self.proxies:
            if self.check_proxy(proxy):
                valid_proxies.append(proxy)
        self.proxies = valid_proxies

    def check_proxy(self, proxy):
        try:
            response = requests.get("https://www.instagram.com", proxies={"http": proxy, "https": proxy}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def send_discord_notification(self, message):
        payload = {
            "content": message
        }
        try:
            response = requests.post(self.discord_webhook_url, json=payload)
            if response.status_code != 204:
                self.logger.error(f"Failed to send notification to Discord: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Exception occurred while sending notification to Discord: {e}")
            return False
        return True

    def scrape_instagram_data(self):
        L = instaloader.Instaloader()
        if self.proxies:
            L.context._session.proxies.update({"http": self.proxies[0], "https": self.proxies[0]})
        try:
            L.login(self.instagram_username, self.instagram_password)
        except instaloader.exceptions.BadCredentialsException:
            print("Invalid credentials, please check your credentials.json.")
            return
        except instaloader.exceptions.ConnectionException as e:
            print(f"Connection error: {e}")
            return
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("Two-factor authentication required. Please log in manually first.")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

        try:
            profile = instaloader.Profile.from_username(L.context, self.target_username)
            return {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography or 'No biography',
                "followers": profile.followers,
                "following": profile.followees,
                "posts": profile.mediacount,
                "recent_posts": [{
                    "post": post.url,
                    "likes": post.likes,
                    "comments": post.comments
                } for post in list(profile.get_posts())[:5]]
            }
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile with username '{self.target_username}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def upload_instagram_data_to_discord(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = file.read()
                payload = {
                    "content": "Instagram data uploaded:",
                    "file": data
                }
                response = requests.post(self.discord_webhook_url, json=payload)
                if response.status_code != 204:
                    self.logger.error(f"Failed to upload Instagram data to Discord: {response.status_code}")
                    return False
                return True
        except FileNotFoundError:
            self.logger.error(f"File not found: {filename}")
            return False
        except Exception as e:
            self.logger.error(f"Exception occurred while uploading Instagram data to Discord: {e}")
            return False

    def monitor_instagram(self):
        last_data = None
        while True:
            current_data = self.scrape_instagram_data()
            if not current_data:
                time.sleep(self.monitoring_interval_hours * 3600)
                continue

            if last_data:
                changes = []
                for key in current_data:
                    if current_data[key] != last_data[key]:
                        changes.append(key)
                if changes:
                    message = f"Changes detected in {', '.join(changes)} for user {self.target_username}."
                    print(message)
                    if not self.send_discord_notification(message):
                        print("Failed to send notification to Discord.")
                else:
                    print(f"No changes detected for user {self.target_username} in the last {self.monitoring_interval_hours} hours.")
            else:
                print("Monitoring started.")
                self.send_discord_notification("Monitoring started for Instagram account: " + self.target_username)
                filename = f"{self.target_username}_instagram_data.json"
                data = self.scrape_instagram_data()
                if data:
                    with open(filename, "w", encoding='utf-8') as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    print(f"Initial data saved to {filename}")
                    if not self.upload_instagram_data_to_discord(filename):
                        print("Failed to upload initial data to Discord.")
                else:
                    print("Failed to fetch initial data.")

            last_data = current_data
            time.sleep(self.monitoring_interval_hours * 3600)

if __name__ == "__main__":
    foundation = Foundation()
    foundation.ensure_proxies_work()
    foundation.monitor_instagram()
