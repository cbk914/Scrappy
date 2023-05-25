#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
# app.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from pymongo import MongoClient
from werkzeug.exceptions import BadRequest, InternalServerError
import subprocess

app = Flask(__name__)

# Set up MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['scraping_db']
collection = db['scraped_data']

def is_allowed(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

def scrape_website(url, ignore_robots=False):
    if not ignore_robots and not is_allowed(url):
        return None
    try:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        raise InternalServerError("An error occurred while trying to scrape the website.")

def process_website(url, ignore_robots):
    soup = scrape_website(url, ignore_robots)
    if soup:
        paragraphs = soup.find_all('p')
        result = '\n'.join(paragraph.text for paragraph in paragraphs)
        # Insert the result into the MongoDB collection
        collection.insert_one({'url': url, 'result': result})
        return result

@app.route('/api/scrape', methods=['POST'])
def scrape():
    domain = request.json.get('domain')
    evil = request.json.get('evil', False)
    output = "report.json"
    subprocess.run(["python", "scraper.py", "-d", domain, "-o", output, "-e" if evil else ""])
    with open(output, "r") as f:
        return jsonify(f.read())

if __name__ == '__main__':
    app.run(debug=True)