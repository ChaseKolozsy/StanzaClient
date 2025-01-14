import httpx
import asyncio

BASE_URL = "http://localhost:5004"

language_abreviations = {
    "Hungarian": "hu",
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Italian": "it",
    "Romanian": "ro",
    "Russian": "ru",
    "Swedish": "sv",
    "Portuguese": "pt",
    "Polish": "pl",
    "Czech": "cs",
    "Bulgarian": "bg",
    "Dutch": "nl",
    "Norwegian": "no",
    "Turkish": "tr",
    "Catalan": "ca",
    "Finnish": "fi",
    "Greek": "el",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Thai": "th",
    "Korean": "ko",
    "Swahili": "sw",
    "Albanian": "sq",
    "Estonian": "et",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Croatian": "hr",
    "Slovenian": "sl",
    "Somali": "so",
    "Afrikaans": "af",
    "Bosnian": "bs",
    "Danish": "da",
    "Flemish": "vls",  # Corrected duplicate
    "Hebrew": "he",
    "Hindi": "hi",
    "Urdu": "ur",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Malay": "ms",
    "Tagalog": "tl",
    "Serbian": "sr",
    "Ukrainian": "uk",
    "Welsh": "cy",
    "Irish": "ga",
    "Icelandic": "is",
    "Maltese": "mt",
    "Macedonian": "mk",
    "Georgian": "ka",
    "Armenian": "hy",
    "Khmer": "km",
    "Lao": "lo",
    "Sinhala": "si",
    "Nepali": "ne",
    "Pashto": "ps",
    "Amharic": "am",
    "Yoruba": "yo",
    "Zulu": "zu"
}

class StanzaClient:
    def __init__(self):
        self.current_language = None
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def select_language(self, language):
        self.current_language = language
        return True

    async def process_text(self, text):
        if not self.current_language:
            raise ValueError("Language not selected")
        
        endpoint = BASE_URL + "/process"
        data = {
            "language": self.current_language,
            "text": text
        }
        response = await self.client.post(endpoint, json=data)
        return response

# Create a singleton instance
_client = StanzaClient()

# Keep the existing interface but make process_text async
def select_language(language):
    return _client.select_language(language)

async def process_text(text):
    return await _client.process_text(text)

# Update the example code to use async
if __name__ == "__main__":
    import json

    async def main():
        # Call the select_language endpoint
        select_language_response = select_language("hu")
        if select_language_response:
            print("Language selected successfully")
        else:
            print("Failed to select language")
        
        # Call the process_text endpoint
        process_text_response = await process_text("Valakinek vagy valaminek a ismerete, vagy megismerése.")
        if process_text_response.status_code == 200:
            print(json.dumps(process_text_response.json(), indent=4, ensure_ascii=False))
        else:
            print("Failed to process text")

    # Run the async main function
    asyncio.run(main())