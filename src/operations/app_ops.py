import httpx
import asyncio
import time
import json
from typing import List

# Update BASE_URL to be a list of endpoints
ENDPOINTS = ["http://localhost:5004", "http://localhost:5005"]

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
        self.current_endpoint = 0
        self.batch_size = 1000  # Maximum batch size

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def select_language(self, language):
        self.current_language = language
        return True

    async def process_text(self, text: str):
        if not self.current_language:
            raise ValueError("Language not selected")
        
        endpoint = ENDPOINTS[self.current_endpoint] + "/process"
        self.current_endpoint = (self.current_endpoint + 1) % len(ENDPOINTS)
        
        data = {
            "language": self.current_language,
            "text": text
        }
        response = await self.client.post(endpoint, json=data)
        return response

    async def process_batch(self, texts: List[str]):
        if not self.current_language:
            raise ValueError("Language not selected")
        
        endpoint = ENDPOINTS[self.current_endpoint] + "/batch_process"
        self.current_endpoint = (self.current_endpoint + 1) % len(ENDPOINTS)
        
        data = {
            "language": self.current_language,
            "texts": texts
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

async def test_processing(mode: str = "single"):
    hungarian_phrases = [
        "A kutya az ember legjobb barátja.",
        "Esik az eső a mezőn.",
        "A macska az asztalon alszik.",
        "Minden reggel kávét iszom.",
        "A gyerekek a parkban játszanak.",
        "A nap szépen süt ma.",
        "A madarak az égen repülnek.",
        "Az idő gyorsan telik.",
        "A könyv az asztalon van.",
        "A virágok tavasszal nyílnak.",
        "Az autó az út szélén parkol.",
        "A tanár magyarázza a leckét.",
        "A szél erősen fúj.",
        "A hal úszik a vízben.",
        "Az óra a falon lóg.",
        "A diákok figyelnek az órán.",
        "A telefon az asztalon csörög.",
        "A vonat késve érkezik.",
        "A levél lassan hullik.",
        "Az orvos betegeket fogad.",
        "A szakács finom ételt készít.",
        "A mérnök új hidat tervez.",
        "A festő képet fest.",
        "A kertész virágokat ültet.",
        "A pék friss kenyeret süt.",
        "A postás leveleket hoz.",
        "A színész szerepet tanul.",
        "A zenész hangszeren játszik.",
        "A pilóta repülőt vezet.",
        "A tűzoltó tüzet olt.",
        "A rendőr forgalmat irányít.",
        "A szerelő autót javít.",
        "A fodrász hajat vág.",
        "A szabó ruhát varr.",
        "A cipész cipőt készít.",
        "A kovács vasat kalapál."
    ]

    select_language("hu")
    start_time = time.time()
    batch_results = []
    single_results = []

    if mode == "batch":
        print(f"Processing {len(hungarian_phrases)} Hungarian phrases in batch mode...")
        try:
            response = await _client.process_batch(hungarian_phrases)
            if response.status_code == 200:
                batch_results = response.json()
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")

    else:  # single mode
        print(f"Processing {len(hungarian_phrases)} Hungarian phrases in single mode...")
        # Create tasks for all phrases
        tasks = [_client.process_text(phrase) for phrase in hungarian_phrases]
        
        # Execute all tasks concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for phrase, response in zip(hungarian_phrases, responses):
            try:
                if isinstance(response, Exception):
                    print(f"Error processing phrase: {str(response)}")
                    continue
                    
                if response.status_code == 200:
                    single_results.append(response.json())
            except Exception as e:
                print(f"Error processing phrase: {str(e)}")

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"\nProcessing Summary:")
    print(f"Mode: {mode}")
    print(f"Total phrases processed: {len(hungarian_phrases)}")
    print(f"Total processing time: {processing_time:.2f} seconds")
    print(f"Average time per phrase: {processing_time/len(hungarian_phrases):.2f} seconds")
    return batch_results, single_results

async def test_endpoints():
    """Test if both endpoints are accessible"""
    try:
        # Test single process endpoint with minimal valid payload
        test_payload = {"language": "hu", "text": "test"}
        response = await _client.client.post(ENDPOINTS[0] + "/process", json=test_payload)
        if response.status_code != 200:
            print(f"Warning: /process endpoint returned status {response.status_code} on {ENDPOINTS[0]}")
            
        # Test batch process endpoint with minimal valid payload
        batch_payload = {"language": "hu", "texts": ["test"]}
        response = await _client.client.post(ENDPOINTS[1] + "/batch_process", json=batch_payload)
        if response.status_code != 200:
            print(f"Warning: /batch_process endpoint returned status {response.status_code} on {ENDPOINTS[1]}")
            
    except Exception as e:
        print(f"Error testing endpoints: {str(e)}")
        return False
    return True

async def main():
    # First test if endpoints are available
    if await test_endpoints():
        # Test both modes
        print("Testing single mode:")
        batch_results, single_results = await test_processing(mode="single")
        
        print("\nTesting batch mode:")
        batch_results, single_results = await test_processing(mode="batch")
        #for result in batch_results:
        #    print(json.dumps(result, indent=4, ensure_ascii=False))
        #for result in single_results:
        #    print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("Failed to verify endpoints. Please check if servers are running correctly.")

if __name__ == "__main__":
    asyncio.run(main())