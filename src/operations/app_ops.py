import httpx
import asyncio
import time
import json
from typing import List
import traceback
import logging

# Update ENDPOINTS to include all machines and ports
ENDPOINTS = [
    "http://localhost:5004",
    "http://localhost:5005",
    "http://localhost:5006",
    "http://localhost:5007",
    "http://localhost:5008",
    "http://localhost:5009",
    "http://localhost:5010",
    "http://localhost:5011",
    "http://localhost:5012",
    "http://localhost:5013",
    "http://10.0.0.138:5004",
    "http://10.0.0.138:5006",
    "http://10.0.0.115:5004",
    "http://10.0.0.115:5005",
    "http://10.0.0.115:5006",
    "http://10.0.0.115:5007",
    "http://10.0.0.115:5008",
    "http://10.0.0.115:5009",
    "http://10.0.0.115:5010",
    "http://10.0.0.115:5011",
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
        self.chunk_delay = 0.05  # 50ms delay between chunks
        self.batch_delay = 0.1   # 100ms delay between main batches

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
        response = await self.client.post("/process", json={"text": text})
        return response.json()
        

    async def process_batch(self, texts: List[str]):
        if not self.current_language:
            raise ValueError("Language not selected")
        
        healthy_endpoints = [ep for ep in ENDPOINTS if self.endpoint_health[ep]]
        if not healthy_endpoints:
            raise Exception("No healthy endpoints available")
        
        # Identify priority endpoint and other endpoints
        priority_endpoint_1 = "http://10.0.0.115:5004"
        priority_endpoint_2 = "http://10.0.0.115:5005"
        priority_endpoint_3 = "http://10.0.0.115:5006"
        priority_endpoint_4 = "http://10.0.0.115:5007"
        priority_endpoint_5 = "http://10.0.0.115:5008"
        priority_endpoint_6 = "http://10.0.0.115:5009"
        priority_endpoint_7 = "http://10.0.0.115:5010"
        priority_endpoint_8 = "http://10.0.0.115:5011"
        priority_endpoint_9 = "http://10.0.0.138:5004"
        priority_endpoint_10 = "http://10.0.0.138:5006"
        other_endpoints = [ep for ep in healthy_endpoints if ep != priority_endpoint_1 and ep != priority_endpoint_2]
        
        # Calculate chunk sizes
        total_texts = len(texts)
        priority_texts_1 = int(total_texts * 0.08676) or 1.0
        priority_texts_2 = int(total_texts * 0.08676) or 1.0
        priority_texts_3 = int(total_texts * 0.08676) or 1.0
        priority_texts_4 = int(total_texts * 0.08676) or 1.0
        priority_texts_5 = int(total_texts * 0.08676) or 1.0
        priority_texts_6 = int(total_texts * 0.08676) or 1.0
        priority_texts_7 = int(total_texts * 0.08676) or 1.0
        priority_texts_8 = int(total_texts * 0.08676) or 1.0
        priority_texts_9 = int(total_texts * 0.08676) or 1.0
        priority_texts_10 = int(total_texts * 0.08676) or 1.0
        remaining_texts = total_texts - priority_texts_1 - priority_texts_2  # Remaining for other endpoints
        base_chunk_size_others = remaining_texts // len(other_endpoints) if other_endpoints else 0
        remainder_others = remaining_texts % len(other_endpoints) if other_endpoints else 0
        
        # Prepare chunks
        chunks = []
        endpoints = []
        start = 0
        
        # Add chunk for priority endpoint 1 if it's healthy
        if priority_endpoint_1 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_1])
            endpoints.append(priority_endpoint_1)
            start += priority_texts_1
        
        # Add chunk for priority endpoint 2 if it's healthy
        if priority_endpoint_2 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_2])
            endpoints.append(priority_endpoint_2)
            start += priority_texts_2
        
        # Add chunk for priority endpoint 3 if it's healthy
        if priority_endpoint_3 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_3])
            endpoints.append(priority_endpoint_3)
            start += priority_texts_3
        
        # Add chunk for priority endpoint 4 if it's healthy
        if priority_endpoint_4 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_4])
            endpoints.append(priority_endpoint_4)
            start += priority_texts_4
        
        # Add chunk for priority endpoint 5 if it's healthy
        if priority_endpoint_5 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_5])
            endpoints.append(priority_endpoint_5)
            start += priority_texts_5

        # Add chunk for priority endpoint 6 if it's healthy
        if priority_endpoint_6 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_6])
            endpoints.append(priority_endpoint_6)
            start += priority_texts_6
        
        # Add chunk for priority endpoint 7 if it's healthy
        if priority_endpoint_7 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_7])
            endpoints.append(priority_endpoint_7)
            start += priority_texts_7
        
        # Add chunk for priority endpoint 8 if it's healthy
        if priority_endpoint_8 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_8])
            endpoints.append(priority_endpoint_8)
            start += priority_texts_8

        # Add chunk for priority endpoint 9 if it's healthy
        if priority_endpoint_9 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_9])
            endpoints.append(priority_endpoint_9)
            start += priority_texts_9

        # Add chunk for priority endpoint 10 if it's healthy
        if priority_endpoint_10 in healthy_endpoints:
            chunks.append(texts[start:start + priority_texts_10])
            endpoints.append(priority_endpoint_10)
            start += priority_texts_10
        
        # Add chunks for other endpoints
        for i, endpoint in enumerate(other_endpoints):
            chunk_size = base_chunk_size_others + (1 if i < remainder_others else 0)
            end = start + chunk_size
            chunks.append(texts[start:end])
            endpoints.append(endpoint)
            start = end

        async def process_chunk_with_retry(endpoint: str, chunk: List[str], chunk_id: int, max_retries: int = 3):
            retries = 0
            last_exception = None
            
            while retries < max_retries:
                try:
                    data = {
                        "language": self.current_language,
                        "texts": chunk
                    }
                    
                    # Exponential backoff: 0.5s, 1s, 2s
                    if retries > 0:
                        await asyncio.sleep(0.5 * (2 ** (retries - 1)))
                        logging.info(f"Retry {retries} for chunk {chunk_id} on endpoint {endpoint}")
                    
                    response = await self.client.post(f"{endpoint}/batch_process", json=data)
                    
                    if response.status_code == 200:
                        logging.info(f"Completed sub-batch {chunk_id} on endpoint {endpoint}")
                        return response.json()
                    
                    last_exception = Exception(f"HTTP {response.status_code}")
                    
                except Exception as e:
                    last_exception = e
                    logging.error(f"Error (attempt {retries + 1}) processing sub-batch {chunk_id} on {endpoint}: {str(e)}")
                
                retries += 1
            
            # If all retries failed, try to redistribute to another endpoint
            try:
                alternate_endpoints = [ep for ep in healthy_endpoints if ep != endpoint]
                if alternate_endpoints:
                    fallback_endpoint = alternate_endpoints[0]  # Pick first available alternate
                    logging.info(f"Redistributing chunk {chunk_id} to {fallback_endpoint} after {endpoint} failed")
                    return await process_chunk_with_retry(fallback_endpoint, chunk, chunk_id, max_retries=1)
            except Exception as e:
                logging.error(f"Failed to redistribute chunk {chunk_id}: {str(e)}")
            
            logging.error(f"All retries failed for chunk {chunk_id} on {endpoint}")
            raise last_exception

        # Process all chunks in parallel with retry logic
        tasks = [
            process_chunk_with_retry(endpoint, chunk, i)
            for i, (endpoint, chunk) in enumerate(zip(endpoints, chunks))
        ]
        
        try:
            all_results = []
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle results and any exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logging.error(f"Chunk {i} failed completely: {str(result)}")
                else:
                    all_results.extend(result)
            
            if not all_results:
                raise Exception("All chunks failed processing")
            
            logging.info(f"Completed processing batch of {len(texts)} texts across {len(healthy_endpoints)} endpoints")
            return all_results
            
        except Exception as e:
            logging.error(f"Error in parallel processing: {str(e)}")
            raise

# Create a singleton instance
_client = StanzaClient()

# Keep the existing interface but make process_text async
def select_language(language):
    return _client.select_language(language)

async def test_processing():
    hungarian_phrases = []

    with open("out.txt", "r") as f:
        for line in f.readlines():
            hungarian_phrases.append(line.strip())

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
    #for result in results:
    #    print(json.dumps(result, indent=4, ensure_ascii=False))
    #return results

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

# Add new batch interface
async def process_batch(texts: List[str]):
    return await _client.process_batch(texts)

async def process_text(text: str):
    return await _client.process_text(text)

if __name__ == "__main__":
    asyncio.run(main())