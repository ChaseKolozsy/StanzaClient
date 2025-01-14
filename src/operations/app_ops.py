import httpx
import asyncio
import time
import json

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

async def test_concurrent_processing():
    # Hungarian test phrases
    hungarian_phrases = [
        "A kutya az ember legjobb barátja.",           # The dog is man's best friend
        "Esik az eső a mezőn.",                        # It's raining in the field
        "A macska az asztalon alszik.",                # The cat is sleeping on the table
        "Minden reggel kávét iszom.",                  # I drink coffee every morning
        "A gyerekek a parkban játszanak.",             # The children are playing in the park
        "A nap szépen süt ma.",                        # The sun is shining beautifully today
        "A madarak az égen repülnek.",                 # The birds are flying in the sky
        "Az idő gyorsan telik.",                       # Time passes quickly
        "A könyv az asztalon van.",                    # The book is on the table
        "A virágok tavasszal nyílnak.",                # Flowers bloom in spring
        "Az autó az út szélén parkol.",                # The car is parked by the road
        "A tanár magyarázza a leckét."                 # The teacher explains the lesson
    ]

    async def process_single_phrase(phrase):
        try:
            response = await process_text(phrase)
            if response.status_code == 200:
                result = response.json()
                print(f"\nPhrase: {phrase}")
                print(json.dumps(result, indent=4, ensure_ascii=False))
                return result
            else:
                print(f"Failed to process phrase: {phrase}")
                return None
        except Exception as e:
            print(f"Error processing phrase: {phrase}")
            print(f"Error: {str(e)}")
            return None

    # First select Hungarian language
    select_language_response = select_language("hu")
    if not select_language_response:
        print("Failed to select Hungarian language")
        return

    print("Processing 12 Hungarian phrases concurrently...")
    start_time = time.time()

    # Process all phrases concurrently
    tasks = [process_single_phrase(phrase) for phrase in hungarian_phrases]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    processing_time = end_time - start_time

    # Print summary
    successful = len([r for r in results if r is not None])
    print(f"\nProcessing Summary:")
    print(f"Total phrases processed: {len(hungarian_phrases)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(hungarian_phrases) - successful}")
    print(f"Total processing time: {processing_time:.2f} seconds")
    print(f"Average time per phrase: {processing_time/len(hungarian_phrases):.2f} seconds")

async def main():
    await test_concurrent_processing()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())