import os
import requests
import argparse
import base64
from datetime import datetime
from openai import OpenAI
import serial
import time
from custom_config import custom_config

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_llm(image_path, detecting_item):
    """Send the image to the LLM and return the yes/no response."""
    # Initialize the client with user-specified API config
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=custom_config.api_key,
    )
    
    # Convert the image to base64
    base64_image = encode_image_to_base64(image_path)
    
    prompt = f"Is there any {detecting_item} in the image? Your answer should be either yes or no"
    
    # Make the API call with the base64 image
    response = client.chat.completions.create(
        model="doubao-vision-lite-32k-241015",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
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

def download_and_analyze(url, save_dir, detecting_item, serial_instance):
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
                print(f"Downloading realtime camera image as {filename} ...")
                response = requests.get(url, timeout=10)
                print(f"Done with status code: {response.status_code}")
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Save the image
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                    
                    # Analyze the image with LLM
                    print("Analyzing image with LLM...")
                    llm_result = analyze_image_with_llm(file_path, detecting_item)
                    # llm_result = "no"
                    
                    clean_result = llm_result.strip().lower()
                    if clean_result == "yes":
                        print("LLM Comparison Result: yes")
                        send_serial_command(serial_instance, "ledon")
                    elif clean_result == "no":
                        print("LLM Comparison Result: no")
                        send_serial_command(serial_instance, "ledoff")
                    else:
                        print("LLM Comparison Result: failed")
                    
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
            
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")

def send_serial_command(serial_instance, command):
    try:
        serial_instance.write(command.encode("utf-8"))
        print(f"Sent command: {command}")
    except Exception as e:
        print(f"Error turning on LED: {e}")
        
def serial_blink_test(serial_instance):
    while True:
        time.sleep(5)
        send_serial_command(serial_instance=serial_instance, command="ledon")
        time.sleep(5)
        send_serial_command(serial_instance=serial_instance, command="ledoff")
        
        
if __name__ == "__main__":
    serial_instance = serial.Serial()
    serial_instance.port = custom_config.com_port
    serial_instance.baudrate = 115200
    serial_instance.open()
    
    parser = argparse.ArgumentParser(description="Download BMP images and analyze with LLM.")
    parser.add_argument("--url", default="http://192.168.8.189/bmp", help="URL to download BMP from")
    parser.add_argument("--save_dir", default="./results", help="Directory to save downloaded images")
    
    args = parser.parse_args()
    
    detecting_item = custom_config.detecting_item
    print(f"Detecting item: {detecting_item}")
    
    download_and_analyze(args.url, args.save_dir, detecting_item, serial_instance)
    