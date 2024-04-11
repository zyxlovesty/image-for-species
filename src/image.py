from duckduckgo_search import DDGS
from fastcore.all import *
from fastdownload import download_url
import pandas as pd
import os

# Initialize DDGS
ddgs = DDGS()

# Load the dataset
df = pd.read_csv('src/50_trails 3.csv')

# Extract unique species names from the 'trail_species' column
species_list = set()
for species_str in df['trail_species']:
    species_list.update([species.strip() for species in species_str.split(',')])

# Convert the set to a sorted list to maintain consistency
sorted_species_list = sorted(species_list)

# Function to search and download the first image of each species
def download_species_images(species_names, download_dir='src/assets'):
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)
    
    for species in species_names:
        try:
            print(f"Searching for '{species}' images...")
            urls = L(ddgs.images(keywords=species, max_results=1)).itemgot('image')
            if urls:
                # Construct a file name and download the first image
                file_name = f"{species.replace(' ', '_')}.jpg"
                dest_path = os.path.join(download_dir, file_name)
                download_url(urls[0], dest_path, show_progress=False)
                print(f"Downloaded image for {species}")
            else:
                print(f"No images found for {species}")
        except Exception as e:
            print(f"Error downloading image for {species}: {e}")

# Example: Download images for the first 5 species in the list
# Adjust the slice as needed or remove it to download images for all species
download_species_images(sorted_species_list)
