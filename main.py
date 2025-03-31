#! /usr/bin/env python3

import requests
import os
import time
import subprocess

def read_webhook_url():
    path = os.environ.get("WEBHOOK_URL_PATH", "webhook.conf")
    with open(path, "r") as f:
        return f.read().strip()

def read_application_logs():
    path = os.environ.get("APPLICATION_LOGS_PATH", "/var/log/directory.log")
    process = subprocess.Popen(
        ['tail', '-f', '-n', '0', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    try:
        while True:
            line = process.stdout.readline()
            if line:
                yield line.rstrip()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()

def send_discord_message(message):
    data = {
        "content": message
    }
    response = requests.post(read_webhook_url(), json=data)
    if response.status_code == 204:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Failed to send message: {response.status_code}")

def is_error(line):
    return "ERROR" in line

def main():
    print("Starting up and reading logs...")
    try:
        # Loop indefinitely reading latest application logs
        logs = read_application_logs()
        for line in logs:
            if is_error(line):
                send_discord_message(f"Error on directory: {line}")
    except Exception as e:
        print(f"Error: {e}")
        send_discord_message(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()