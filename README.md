# Scrappy

This set of scripts is designed to scrape websites for URLs. It respects the robots.txt file of each website unless explicitly told not to. The scraped data is stored in a MongoDB database. The scraper can be interacted with through a console, web interface or an API.

# Installation

Clone the repository to your local machine.

Install the required Python packages. You can do this by navigating to the directory containing requirements.txt and running the following command:

  pip install -r requirements.txt
  
Make sure you have MongoDB installed and running on your machine. If you don't, you can download it from the official MongoDB website and follow the instructions there to install it.

# Execution

To run the backend script directly, use the following command:

python scrappy-cli.py -d [domain] -o [output file] -e

Replace [domain] with the domain you want to scrape and [output file] with the name of the file you want to output the results to. The -e flag is optional and tells the scraper to ignore the robots.txt file.

To run the web interface, use the following command:

  python scrappy-web.py
  
Then, open a web browser and navigate to localhost:5000.

To run the API, use the following command:

  python scrappy-api.py
  
Then, you can send POST requests to localhost:5000/scrap with a JSON body containing the domain you want to scrape and whether or not to ignore the robots.txt file. For example:

{
    "domain": "example.com",
    "evil": true
}

Docker

If you have Docker installed, you can build and run the application using Docker. Navigate to the directory containing the Dockerfile and run the following commands:

docker build -t scrappy .
docker run -p 5000:5000 scrappy

Then, you can access the web interface or API in the same way as described above.

YAML file for reNgine
You can use the provided YAML file to add this tool to reNgine, an automated reconnaissance framework. Just add the YAML file to the tools directory of your reNgine installation.

Please note that these instructions assume a Unix-like environment and may need to be adjusted for other environments. Also, please replace placeholders (like [domain] and [output file]) with your actual data.
