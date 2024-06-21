import requests

BASE_URL = "http://localhost:5004"

def select_language(language):
    endpoint = BASE_URL + "/select_language"
    data = {"language": language}
    response = requests.post(endpoint, json=data)
    return response.json()

def process_text(text):
    endpoint = BASE_URL + "/process"
    data = {"text": text}
    response = requests.post(endpoint, json=data)
    return response.json()

if __name__ == "__main__":
    # Call the select_language endpoint
    select_language_response = select_language("hu")
    print(select_language_response)
    
    # Call the process_text endpoint
    process_text_response = process_text("Hogy feldolgozni kell ezt a szveget?")
    print(process_text_response)