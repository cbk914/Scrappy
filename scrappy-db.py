import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_mongodb():
    """Start MongoDB with TLS for secure connections."""
    try:
        # Uncomment the line below for unsecure database connections (NOT RECOMMENDED)
        # subprocess.run(["mongod"])

        # Secure connection
        subprocess.run(
            ["mongod", "--tlsMode", "requireTLS", "--tlsCertificateKeyFile", "/etc/ssl/mongodb.pem"],
            check=True
        )
        logging.info("MongoDB started successfully with TLS.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start MongoDB: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    start_mongodb()
