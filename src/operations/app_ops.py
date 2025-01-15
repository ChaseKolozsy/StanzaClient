import httpx
import asyncio
import time
import json
from typing import List
import traceback

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
    "Flemish": "vls",
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
    "Zulu": "zu",
    "AncientGreek": "grc",
    "Basque": "eu",
    "Belarusian": "be",
    "ClassicalChinese": "lzh",
    "Coptic": "cop",
    "Faroese": "fo",
    "Galician": "gl",
    "Gothic": "got",
    "Marathi": "mr",
    "Naija": "pcm",
    "NorthSami": "sme",
    "OldChurchSlavonic": "cu",
    "OldEastSlavic": "orv",
    "OldFrench": "fro",
    "Persian": "fa",
    "Sanskrit": "sa",
    "ScottishGaelic": "gd",
    "SwedishSign Language": "swl",
    "TurkishGerman": "qtd",
    "Uyghur": "ug",
    "WesternArmenian": "hyw",
    "Wolof": "wo"
}

class StanzaClient:
    def __init__(self):
        self.current_language = None
        self.client = httpx.AsyncClient(timeout=60.0)
        self.current_endpoint = 0
        self.endpoint_health = {endpoint: True for endpoint in ENDPOINTS}
        self.batch_size = 12000

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def select_language(self, language):
        self.current_language = language
        return True

    async def process_batch(self, texts: List[str]):
        """Process multiple texts in a single batch request"""
        if not self.current_language:
            raise ValueError("Language not selected")
        
        # Split the texts evenly across all healthy endpoints
        healthy_endpoints = [ep for ep in ENDPOINTS if self.endpoint_health[ep]]
        if not healthy_endpoints:
            raise Exception("No healthy endpoints available")
            
        # Calculate chunk size for even distribution
        chunk_size = len(texts) // len(healthy_endpoints)
        chunks = [texts[i:i + chunk_size] for i in range(0, len(texts), chunk_size)]
        
        # If we have any remainder due to uneven division, add to last chunk
        if len(texts) % len(healthy_endpoints) != 0:
            chunks[-1].extend(texts[len(healthy_endpoints) * chunk_size:])
        
        # Create tasks for parallel processing
        tasks = []
        for endpoint, chunk in zip(healthy_endpoints, chunks):
            data = {
                "language": self.current_language,
                "texts": chunk
            }
            tasks.append(self.client.post(f"{endpoint}/batch_process", json=data))
        
        try:
            # Process all chunks in parallel
            responses = await asyncio.gather(*tasks)
            
            # Combine results from all endpoints
            all_results = []
            for response in responses:
                if response.status_code == 200:
                    chunk_results = response.json()
                    all_results.extend(chunk_results)
                else:
                    print(f"Error response: {response.status_code}")
            
            return all_results
            
        except Exception as e:
            print(f"Error in parallel processing: {str(e)}")
            raise

# Create a singleton instance
_client = StanzaClient()

# Keep the existing interface but make process_text async
def select_language(language):
    return _client.select_language(language)

async def test_processing():

    hungarian_phrases = []

    select_language("hu")
    start_time = time.time()
    results = []

    print(f"Processing {len(hungarian_phrases)} Hungarian phrases using batch processing...")
    
    # Split phrases into batches
    batch_size = _client.batch_size
    batches = [hungarian_phrases[i:i + batch_size] 
               for i in range(0, len(hungarian_phrases), batch_size)]
    
    # Process each batch
    for i, batch in enumerate(batches, 1):
            try:
                batch_results = await process_batch(batch)
                results.extend(batch_results)
                print(f"Processed batch {i}/{len(batches)} "
                    f"({len(batch)} phrases)")
            except Exception as e:
                print(f"Error processing batch {i}: {str(e)}")
                traceback.print_exc()

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"\nProcessing Summary:")
    print(f"Total phrases processed: {len(hungarian_phrases)}")
    print(f"Number of batches: {len(batches)}")
    print(f"Batch size: {batch_size}")
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
        for result in results:
            print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("Failed to verify endpoints. Please check if servers are running correctly.")

# Add new batch interface
async def process_batch(texts: List[str]):
    return await _client.process_batch(texts)

if __name__ == "__main__":
    asyncio.run(main())