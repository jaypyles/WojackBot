# STL
import os

# PDM
import praw


class RedditSearcher(praw.Reddit):
    def __init__(self) -> None:
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.password = os.getenv("REDDIT_PASSWORD")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.username = os.getenv("REDDIT_USERNAME")
        super().__init__(
            client_id=self.client_id,
            client_secret=self.client_secret,
            password=self.password,
            user_agent=self.user_agent,
            username=self.username,
        )
