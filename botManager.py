# botManager.py

from bots import tokens

class BotManager:
    def __init__(self):
        """
        Initialize the BotManager using bot data from bots.py.
        """
        self.bot_data = tokens  # Load tokens directly from bots.py
        self.last_used_index = 0
        self.request_count = 0  # Track the number of requests

    def get_next_bot(self):
        """
        Switch to the next bot in a round-robin fashion after every 3 requests.
        Returns the bot's name, CSRF token, cookie, and user-agent.
        """
        if not self.bot_data:
            print("No bots available in bot data.")
            return None, None, None, None

        # Check if we should switch the bot (after 2 requests)
        if self.request_count >= 2:
            self.last_used_index = (self.last_used_index + 1) % len(self.bot_data)
            self.request_count = 0  # Reset request count after switching bot

        bot_info = self.bot_data[self.last_used_index]
        bot_name = bot_info["bot"]
        csrf_token = bot_info["csrf"]
        cookie = bot_info["cookie"]
        useragent = bot_info["user-agent"]

        # Print which bot is in use
        print(f"Using bot: {bot_name}")

        # Increment the request count
        self.request_count += 1

        return bot_name, csrf_token, cookie, useragent
