import os
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weaviate_session():
    """
    Returns a Weaviate client instance for interacting with the Weaviate Cloud.
    """
    weaviate_url = os.getenv("WEAVIATE_URL")  # e.g., "rAnD0mD1g1t5.something.weaviate.cloud"
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")  # Your Weaviate Cloud API key

    if not weaviate_url:
        raise ValueError("WEAVIATE_URL is not set")
    if not weaviate_api_key:
        raise ValueError("WEAVIATE_API_KEY is not set")

    # Use authentication if an API key is provided
    auth = AuthApiKey(api_key=weaviate_api_key)

    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=auth,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Weaviate: {e}")
    
    return client

# Step 1: Fetch data from Weaviate using the Python client
def fetch_vectors():
    """
    Fetch vectors and properties from Weaviate using the collections.get() method.
    """
    # Get Weaviate client instance
    client = get_weaviate_session()

    try:
        # Retrieve the collection
        collection = client.collections.get("FAQ")  # Replace "FAQ" with your actual class name

        # Iterate through the objects and extract properties and vectors
        vectors = []
        for item in collection.iterator(include_vector=True):  # Include vectors in the iteration
            print("Properties:", item.properties)
            print("Vector Type:", type(item.vector))
            print("Vector Content:", item.vector)

            # Handle cases where item.vector is a dictionary
            if isinstance(item.vector, dict):
                # Extract the numerical vector (adjust the key as needed)
                numerical_vector = item.vector.get("text2vecweaviate", [])
                if not numerical_vector:
                    raise ValueError("No numerical vector found in item.vector")
                vectors.append(numerical_vector)
            else:
                # Append the vector directly if it's already numerical
                vectors.append(item.vector)

        return np.array(vectors)
    finally:
        # Ensure the client connection is closed
        client.close()

# Step 2: Reduce dimensionality to 3D using PCA
def reduce_to_3d(vectors):
    pca = PCA(n_components=3)
    reduced_vectors = pca.fit_transform(vectors)
    return reduced_vectors

# Step 3: Visualize the 3D vectors
def visualize_3d(vectors_3d):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vectors_3d[:, 0], vectors_3d[:, 1], vectors_3d[:, 2], c='blue', marker='o')
    ax.set_xlabel('PCA 1')
    ax.set_ylabel('PCA 2')
    ax.set_zlabel('PCA 3')
    plt.show()

# Main script
if __name__ == "__main__":
    try:
        # Fetch vectors from Weaviate
        vectors = fetch_vectors()
        
        # Reduce dimensionality to 3D
        vectors_3d = reduce_to_3d(vectors)
        
        # Visualize the reduced vectors
        visualize_3d(vectors_3d)
    except Exception as e:
        print(f"Error: {e}")