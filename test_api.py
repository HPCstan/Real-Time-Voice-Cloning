import requests
import os

url = "http://localhost:8000/clone"
file_path = "samples/p240_00000.mp3"
text = "This is a test of the real-time voice cloning API. It sounds pretty good!"

with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"text": text}
    print(f"Sending request to {url}...")
    response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open("test_output.wav", "wb") as f:
        f.write(response.content)
    print("Success! Generated audio saved to test_output.wav")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
