#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 23:50:39 2025

@author: lucaszhang
"""

import requests
from flask import Flask, request

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1420254786166718564/fR9iEXWowndL67YhXUPDfH6cpWwE_YnDybVURXVtRNfRUEoeUZ2agHswTBB8ZXUp9nWX"

def parse_command(content):
    parts = content[len("!embed "):].split(" ")
    data = {}
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            data[key] = value
    return data

def build_embed(data):
    embed = {}
    if "title" in data:
        embed["title"] = data["title"]
    if "text" in data:
        embed["description"] = data["text"]
    if "date" in data:
        embed["footer"] = {"text": data["date"]}
    if "author" in data:
        embed["author"] = {"name": data["author"]}
    if "icon_url" in data:
        embed.setdefault("author", {})["icon_url"] = data["author_icon"]
        embed["thumbnail"] = {"url": data["icon_url"]}
    if "image_url" in data:
        embed["image"] = {"url": data["image"]}
    return embed

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.json
    content = json_data.get("content", "")
    if not content.startswith("-news"):
        return {"status": "ignored"}
    data = parse_command(content)
    embed = build_embed(data)
    requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    return {"status": "sent"}

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
