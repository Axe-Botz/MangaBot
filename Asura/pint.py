import os
import requests
from pyrogram import Client, filters

from Asura import asura as app

# Handler for receiving messages
@app.on_message(filters.command("img"))
def handle_search(_, message):
    # Get the search query from the message
    query = message.text.split(" ", 1)[1]
    
    # Fetch photos from Pinterest
    photos = fetch_pinterest_photos(query)
    
    # Send the photos as a reply to the message
    for photo in photos:
        app.send_photo(message.chat.id, photo)
        

def fetch_pinterest_photos(query):
    # Format the query to use in the Pinterest URL
    formatted_query = query.replace(" ", "+")
    url = f"https://www.pinterest.com/search/pins/?q={formatted_query}"
    
    # Send a GET request to Pinterest
    response = requests.get(url)
    
    # Extract the image URLs from the response HTML
    image_urls = extract_image_urls(response.text)
    
    # Download the images and return their paths
    return download_images(image_urls)


def extract_image_urls(html):
    # Extract the image URLs using a regular expression or HTML parser
    # Customize this part based on Pinterest's HTML structure
    
    # Example using regular expression:
    import re
    pattern = r'"images":\["(https:\/\/i\.pinimg\.com\/\d+x\/.*?\.jpg)"\]'
    matches = re.findall(pattern, html)
    return matches


def download_images(image_urls):
    # Create a directory to store the downloaded images
    os.makedirs("pinterest_images", exist_ok=True)
    
    # Download and save each image
    image_paths = []
    for url in image_urls:
        response = requests.get(url)
        filename = url.split("/")[-1]
        file_path = f"pinterest_images/{filename}"
        with open(file_path, "wb") as f:
            f.write(response.content)
        image_paths.append(file_path)
    
    return image_paths
