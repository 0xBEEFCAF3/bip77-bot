#! /usr/bin/env python3

import requests
import os

def read_webhook_url():
    path = os.environ.get("WEBHOOK_URL_PATH", "webhook.txt")
    with open(path, "r") as f:
        return f.read().strip()

def send_discord_message(message):
    data = {
        "content": message
    }
    response = requests.post(read_webhook_url(), json=data)
    if response.status_code == 204:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Failed to send message: {response.status_code}")


def main():
    send_discord_message("foo!")


if __name__ == "__main__":
    main()