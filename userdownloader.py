import praw
import requests
import os
from urllib.parse import urlparse
from pathlib import Path

# Replace these with your actual Reddit API credentials
# You can google how to set this up.
client_id = ""
client_secret = ""
user_agent = "Mozilla/5.0"  # or whatever you want, it doesn't matter.

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent
)

# List of valid image extensions
valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]


def is_valid_image_url(url):
    """Check if the URL has a valid image extension."""
    parsed_url = urlparse(url)
    return any(
        parsed_url.path.lower().endswith(ext) for ext in valid_extensions
    )


def download_image(url, filename):
    """Download an image from a URL and save it to a file."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")


def main():
    # Get username input from the user
    username = input("Enter the Reddit username: ").strip()
    limit = int(input("Enter limit: "))

    # Create a directory for downloads
    download_dir = Path(f"{username}_images")
    download_dir.mkdir(exist_ok=True)

    user = reddit.redditor(username)
    downloaded_count = 0

    try:
        for submission in user.submissions.new(limit=limit):
            if is_valid_image_url(submission.url):
                file_extension = os.path.splitext(
                    urlparse(submission.url).path
                )[1]
                filename = download_dir / f"{submission.id}{file_extension}"

                download_image(submission.url, filename)
                downloaded_count += 1

        print(f"Successfully downloaded {downloaded_count} to {download_dir}")

    except praw.exceptions.PRAWException as e:
        print(f"A PRAW exception occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
