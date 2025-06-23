# Visualise Vector

This project fetches vectors from a Weaviate database, reduces their dimensionality using PCA, and visualizes them in 3D.

## Features
- Connects to a Weaviate database using API keys.
- Fetches vectors and properties from a specified collection.
- Reduces dimensionality of vectors to 3D using PCA.
- Visualizes the reduced vectors in a 3D scatter plot.

## Requirements
Ensure you have the following installed:
- Python 3.11 or later
- Required Python libraries (see `requirements.txt`)

## Installation
1. Clone the repository to your local machine:
2. Run: pip install -r requirements.txt
3. Setup a .env file with the follwing content:
```
urlWEAVIATE_URL=<your-weaviate>
WEAVIATE_API_KEY=<your-api-key>
```
im not giving mine ;)

4. Run the script to fetch vectors and visualise it:
python "main.py"


## File Structure
- import requests.py: Main script for fetching, processing, and visualizing vectors.
- requirements.txt: List of dependencies.
- .gitignore: Specifies files to ignore in version control.
Notes
Replace "FAQ" in the script with the actual class name in your Weaviate schema.
Ensure your .env file contains valid credentials for connecting to Weaviate.



License
This project is licensed under the MIT License.