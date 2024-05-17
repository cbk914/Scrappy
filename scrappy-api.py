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
import logging

app = Flask(__name__)

# Set up MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['scraping_db']
collection = db['scraped_data']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_allowed(url, user_agent='*'):
    """Check if scraping is allowed by robots.txt."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logging.error(f"Error reading robots.txt for {url}: {e}")
        return False

def scrape_website(url, ignore_robots=False):
    """Scrape the website content."""
    if not ignore_robots and not is_allowed(url):
        raise BadRequest("Scraping disallowed by robots.txt")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {url}: {e}")
        raise InternalServerError("An error occurred while trying to scrape the website.")

def process_website(url, ignore_robots):
    """Process the website and save data to MongoDB."""
    soup = scrape_website(url, ignore_robots)
    if soup:
        paragraphs = soup.find_all('p')
        result = '\n'.join(paragraph.text for paragraph in paragraphs)
        collection.insert_one({'url': url, 'result': result})
        return result

@app.route('/api/scrape', methods=['POST'])
def scrape():
    """API endpoint to scrape a website."""
    data = request.get_json()
    if not data or 'domain' not in data:
        raise BadRequest("Missing 'domain' in request data")

    domain = data['domain']
    evil = data.get('evil', False)
    
    try:
        output = "report.json"
        subprocess.run(["python", "scraper.py", "-d", domain, "-o", output, "-e" if evil else ""], check=True)
        with open(output, "r") as f:
            return jsonify(f.read())
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise InternalServerError("An error occurred while executing the scraper.")
    except Exception as e:
        logging.error(f"Error reading output file: {e}")
        raise InternalServerError("An error occurred while processing the output file.")

if __name__ == '__main__':
    app.run(debug=True)
