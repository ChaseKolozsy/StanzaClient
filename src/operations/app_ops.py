import requests

BASE_URL = "http://localhost:5004"

def select_language(language):
    endpoint = BASE_URL + "/select_language"
    data = {"language": language}
    response = requests.post(endpoint, json=data)
    return response

def process_text(text):
    endpoint = BASE_URL + "/process"
    data = {"text": text}
    response = requests.post(endpoint, json=data)
    return response

if __name__ == "__main__":
    # Call the select_language endpoint
    select_language_response = select_language("hu")
    if select_language_response.status_code == 200:
        print("Language selected successfully")
    else:
        print("Failed to select language")
    
    # Call the process_text endpoint
    process_text_response = process_text("Hogy feldolgozni kell ezt a szveget?")
    if process_text_response.status_code == 200:
        print(process_text_response.json())
    else:
        print("Failed to process text")