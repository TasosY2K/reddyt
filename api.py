import praw

reddit = praw.Reddit(client_id="5Dg5FEH91oN7pSwuC5Qt-Q",
                     client_secret="_hWUNMN5rqzvBYvV7kafJYrTgb7CVQ", user_agent="reddyt by u/owdev")


def get_top(length=3) -> list:
    return [k.title for k in reddit.subreddit("Showerthoughts").hot(limit=length)]
