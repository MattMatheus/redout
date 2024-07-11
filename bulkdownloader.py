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

reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent
)

valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]


def is_valid_image_url(url):
    parsed_url = urlparse(url)
    return any(
        parsed_url.path.lower().endswith(ext) for ext in valid_extensions
    )


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")


def process_user(username):
    download_dir = Path(f"{username}_images")
    download_dir.mkdir(exist_ok=True)

    user = reddit.redditor(username)
    downloaded_count = 0

    try:
        for submission in user.submissions.new(limit=None):
            if is_valid_image_url(submission.url):
                file_extension = os.path.splitext(
                    urlparse(submission.url).path
                )[1]
                filename = download_dir / f"{submission.id}{file_extension}"

                download_image(submission.url, filename)
                downloaded_count += 1

        print(
            f"Downloaded {downloaded_count} images for {username} to {download_dir}"
        )
    except praw.exceptions.PRAWException as e:
        print(f"A PRAW exception occurred for user {username}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred for user {username}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for user {username}: {e}")


def main():
    username_file = input(
        "Enter the path to the file containing usernames: "
    ).strip()

    try:
        with open(username_file, "r") as file:
            usernames = [line.strip() for line in file if line.strip()]

        print(f"Found {len(usernames)} usernames in the file.")

        for username in usernames:
            print(f"\nProcessing user: {username}")
            process_user(username)

        print("\nFinished processing all users.")
    except FileNotFoundError:
        print(f"Error: The file '{username_file}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


if __name__ == "__main__":
    main()
