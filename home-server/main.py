import os
import time
import requests
import argparse
import base64
from datetime import datetime
from openai import OpenAI

# Store API configuration in a dictionary
API_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "2ddadffb-2079-4da2-84bf-6099e1feb2a8",  # <-- Replace with your actual API key
}

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_llm(image_path):
    """Send the image to the LLM and return the yes/no response."""
    # Initialize the client with user-specified API config
    client = OpenAI(
        base_url=API_CONFIG["base_url"],
        api_key=API_CONFIG["api_key"],
    )
    
    # Convert the image to base64
    base64_image = encode_image_to_base64(image_path)
    
    # Make the API call with the base64 image
    response = client.chat.completions.create(
        model="doubao-vision-lite-32k-241015",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is there any human in the image? Your answer should be either yes or no"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/bmp;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )
    
    # Extract the LLM's raw response text
    llm_response = response.choices[0].message.content
    return llm_response

def download_and_analyze(url, save_dir):
    """
    Downloads a BMP image from the specified URL and analyzes it with LLM.
    Only the last 5 downloaded images are kept in the directory.
    
    Args:
        url: URL to download the BMP from
        save_dir: Directory to save the downloaded images
    """
    # Create the results directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Starting BMP download from {url}")
    print(f"Images will be saved to {os.path.abspath(save_dir)}")
    
    try:
        while True:
            # Generate timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.bmp"
            file_path = os.path.join(save_dir, filename)
            
            try:
                # Download the BMP image
                response = requests.get(url, timeout=10)
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Save the image
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                    
                    # Analyze the image with LLM
                    print("Analyzing image with LLM...")
                    llm_result = analyze_image_with_llm(file_path)
                    
                    clean_result = llm_result.strip().lower()
                    if clean_result == "yes":
                        print("LLM Comparison Result: yes")
                    elif clean_result == "no":
                        print("LLM Comparison Result: no")
                    else:
                        print("LLM Comparison Result: failed")
                    
                    # Keep only the last 5 images
                    bmp_files = sorted(
                        f for f in os.listdir(save_dir) if f.lower().endswith(".bmp")
                    )
                    while len(bmp_files) > 5:
                        oldest_file = bmp_files.pop(0)
                        os.remove(os.path.join(save_dir, oldest_file))
                
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
            
            # Since interval is removed, we do not wait; immediately continue downloading
            
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download BMP images and analyze with LLM.")
    parser.add_argument("--url", default="http://192.168.8.189/bmp", help="URL to download BMP from")
    parser.add_argument("--save_dir", default="./results", help="Directory to save downloaded images")
    
    args = parser.parse_args()
    
    download_and_analyze(args.url, args.save_dir)