import httpx
import asyncio
import time
import json
from typing import List

# Update ENDPOINTS to include all machines and ports
ENDPOINTS = [
    "http://localhost:5004",
    "http://localhost:5005",
    "http://10.0.0.138:5004",
    "http://10.0.0.138:5005",
    "http://10.0.0.115:5004",
    "http://10.0.0.115:5005"
]

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
        self.client = httpx.AsyncClient(timeout=30.0)
        self.current_endpoint = 0
        self.endpoint_health = {endpoint: True for endpoint in ENDPOINTS}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def select_language(self, language):
        self.current_language = language
        return True

    async def _try_endpoint(self, endpoint, data):
        """Attempt to use an endpoint and mark it as unhealthy if it fails"""
        try:
            response = await self.client.post(f"{endpoint}/process", json=data)
            self.endpoint_health[endpoint] = True
            return response
        except Exception as e:
            self.endpoint_health[endpoint] = False
            raise e

    async def process_text(self, text: str):
        if not self.current_language:
            raise ValueError("Language not selected")
        
        # Find next healthy endpoint
        attempts = 0
        while attempts < len(ENDPOINTS):
            endpoint = ENDPOINTS[self.current_endpoint]
            self.current_endpoint = (self.current_endpoint + 1) % len(ENDPOINTS)
            
            if self.endpoint_health[endpoint]:
                try:
                    data = {
                        "language": self.current_language,
                        "text": text
                    }
                    return await self._try_endpoint(endpoint, data)
                except Exception as e:
                    attempts += 1
                    continue
            else:
                attempts += 1
                
        raise Exception("No healthy endpoints available")

# Create a singleton instance
_client = StanzaClient()

# Keep the existing interface but make process_text async
def select_language(language):
    return _client.select_language(language)

async def process_text(text):
    return await _client.process_text(text)

async def test_processing():
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
        "A kovács vasat kalapál.",
        "A programozó kódot ír.",
        "A művész galériában kiállít.",
        "A sportoló edzésen vesz részt.",
        "A tudós kísérleteket végez.",
        "Az építész házat tervez.",
        "A könyvtáros könyveket rendez.",
        "A pincér ételt szolgál fel.",
        "A boltos árut pakol.",
        "A bankár pénzt számol.",
        "A sofőr buszt vezet.",
        "A vadász erdőben jár.",
        "A halász hálót vet.",
        "A bíró ítéletet hoz.",
        "A farmer földet művel.",
        "A méhész mézet gyűjt.",
        "A hegymászó csúcsra tör.",
        "A búvár mélybe merül.",
        "A fotós képeket készít.",
        "A cukrász tortát díszít.",
        "A villanyszerelő vezetéket szerel.",
        "A kéményseprő kéményt tisztít.",
        "A varrónő gépet használ.",
        "A műszerész alkatrészt cserél.",
        "A kozmetikus arcot fest.",
        "A masszőr izmokat lazít.",
        "A díszlettervező színpadot épít.",
        "A tolmács nyelveket beszél.",
        "A meteorológus időjárást jósol.",
        "A régész leleteket keres.",
        "A botanikus növényeket vizsgál.",
        "A zoológus állatokat figyel.",
        "A geológus kőzeteket elemez.",
        "A csillagász távcsövet használ.",
        "A koreográfus táncot tanít.",
        "A karmester zenekart vezényel.",
        "A szobrász követ farag."
    ]

    select_language("hu")
    start_time = time.time()
    results = []

    print(f"Processing {len(hungarian_phrases)} Hungarian phrases...")
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
                results.append(response.json())
        except Exception as e:
            print(f"Error processing phrase: {str(e)}")

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"\nProcessing Summary:")
    print(f"Total phrases processed: {len(hungarian_phrases)}")
    print(f"Total processing time: {processing_time:.2f} seconds")
    print(f"Average time per phrase: {processing_time/len(hungarian_phrases):.2f} seconds")
    print(f"Phrases per second: {len(hungarian_phrases)/processing_time:.2f}")
    return results

async def test_endpoints():
    """Test if all endpoints are accessible"""
    healthy_endpoints = 0
    for endpoint in ENDPOINTS:
        try:
            test_payload = {"language": "hu", "text": "test"}
            response = await _client.client.post(f"{endpoint}/process", json=test_payload)
            if response.status_code == 200:
                healthy_endpoints += 1
                print(f"✅ Endpoint {endpoint} is healthy")
            else:
                print(f"⚠️ Endpoint {endpoint} returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing endpoint {endpoint}: {str(e)}")
    
    print(f"\nFound {healthy_endpoints} healthy endpoints out of {len(ENDPOINTS)}")
    return healthy_endpoints > 0

async def main():
    if await test_endpoints():
        results = await test_processing()
        #for result in results:
        #    print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("Failed to verify endpoints. Please check if servers are running correctly.")

if __name__ == "__main__":
    asyncio.run(main())