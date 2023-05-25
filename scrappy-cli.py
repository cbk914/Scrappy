#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import argparse
import urllib.robotparser

def is_allowed(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

def scrape_website(url, ignore_robots=False):
    if not ignore_robots and not is_allowed(url):
        print(f"Scraping is disallowed on {url}")
        return None
    try:
        response = requests.get(url, timeout=3)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

def process_website(url):
    soup = scrape_website(url, args.evil)
    if soup:
        paragraphs = soup.find_all('p')
        return '\n'.join(paragraph.text for paragraph in paragraphs)

def get_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

parser = argparse.ArgumentParser(description='Web scraper')
parser.add_argument('-d', '--domain', help='Domain to scrape')
parser.add_argument('-f', '--file', help='File containing list of domains to scrape')
parser.add_argument('-o', '--output', help='Output file')
parser.add_argument('-e', '--evil', help=argparse.SUPPRESS, action='store_true')

args = parser.parse_args()

urls = []

if args.domain:
    urls.append(args.domain)
elif args.file:
    urls = get_urls_from_file(args.file)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(process_website, urls)

if args.output:
    with open(f"{args.output}.txt", 'w') as txt_file, open(f"{args.output}.html", 'w') as html_file:
        for result in results:
            if result:
                txt_file.write(result + '\n')
                html_file.write('<p>' + result + '</p>\n')
