import subprocess

def start_mongodb():
    # Uncomment for unsecure database connections (NOT RECOMMENDED)
    # subprocess.run(["mongod"])
    subprocessrun(["mongod --tlsMode requireTLS --tlsCertificateKeyFile /etc/ssl/mongodb.pem"])

if __name__ == "__main__":
    start_mongodb()