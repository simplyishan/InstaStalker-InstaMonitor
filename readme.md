# InstaMonitor/InstaStalker

InstaMonitor/InstaStalker is a Python-based tool designed for monitoring Instagram accounts and notifying changes via Discord webhook. This tool fetches Instagram profile data, detects changes in follower counts, posts, and other metrics, and notifies the user through Discord.

## Features

- **Instagram Account Monitoring:** Tracks changes in follower count, following count, and posts.
- **Discord Integration:** Sends notifications to Discord webhooks on detected changes.
- **Proxy Support:** Optionally supports proxies to avoid IP blocking issues.
- **Error Handling:** Logs errors and exceptions for troubleshooting.
- **Initial Data Upload:** Uploads initial Instagram data to Discord when monitoring starts.

## Technologies Used

- **Language:** Python
- **Modules:** instaloader, requests, json, logging
- **Data Storage:** JSON files
- **Integration:** Discord webhooks for notifications

## How to Use

1. **Install Required Modules:**
   - Make sure you have Python installed.
   - Install the required modules using pip:
     ```bash
     pip install instaloader
     ```

2. **Setup:**
   - Add your Instagram account credentials (`instagram_username` and `instagram_password`) to `credentials.json`:
     ```json
     {
       "instagram_username": "your_instagram_username",
       "instagram_password": "your_instagram_password",
       "discord_webhook_url": "your_discord_webhook_url",
       "time_interval_hours": 1
     }
     ```
     Note: It's recommended to use an alternative account for monitoring to avoid any issues with your main account.

   - Replace `"your_discord_webhook_url"` with your actual Discord webhook URL.
   - Set the `time_interval_hours` parameter in `credentials.json` to specify the monitoring interval in hours. You can also specify intervals in fractions of an hour (e.g., `0.5` for 30 minutes).

3. **Run the Program:**
   - Execute the `main.py` script to start monitoring:
     ```bash
     python main.py
     ```

4. **Disclaimer:**
   - If anything happens to your main Instagram account due to the use of this tool, the developer (Simplyishan) holds no responsibility.

## Author

- **Author:** Simplyishan
- **Instagram:** [_simplyishan](https://instagram.com/_simplyishan)
- **Email:** ishannnhere@gmail.com

## Contact

For issues, feedback, or feature requests, please contact Simplyishan via email or Instagram.

## Future Updates

- **Multiple Account Monitoring:** Ability to monitor multiple Instagram accounts simultaneously.
- **Fallback Notifications:** Notify via email if Discord notifications fail.
- **Enhanced Security:** Store credentials in a highly encrypted format (e.g., MongoDB).
