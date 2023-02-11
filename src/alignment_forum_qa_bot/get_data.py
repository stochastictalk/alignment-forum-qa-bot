import json
import os
from pathlib import Path
import requests


def main():
    download_posts()
    # download_comments()


def get_posts():
    posts_query = "{ posts { results { title author htmlBody } } }"
    response = requests.post("https://www.alignmentforum.org/graphql", json={"query": posts_query})
    return response.json()["data"]["posts"]["results"]


def download_posts():
    posts = get_posts()
    data_dir = Path(os.environ["DATA_DIR"])
    data_dir.mkdir(parents=True, exist_ok=True)
    with (data_dir / "posts.json").open("w") as f:
        json.dump(posts, f, indent=2)


def download_comments():
    comments = get_comments()
    with Path(os.environ["DATA_DIR"], "comments.json").open("w") as f:
        json.dump(comments, f, indent=2)


def get_comments():
    ...


if __name__ == "__main__":
    main()
