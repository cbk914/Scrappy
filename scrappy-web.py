#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import urllib.robotparser

app = Flask(__name__)

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
        return None

def process_website(url, ignore_robots):
    soup = scrape_website(url, ignore_robots)
    if soup:
        paragraphs = soup.find_all('p')
        return '\n'.join(paragraph.text for paragraph in paragraphs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        ignore_robots = bool(request.form.get('ignore_robots'))
        result = process_website(url, ignore_robots)
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
