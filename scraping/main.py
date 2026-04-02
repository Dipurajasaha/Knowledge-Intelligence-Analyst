import os 
import pandas as pd
from config import Config
from utils import prepare_dataset
import requests

# Import dataset
from reddit_scraper import fetch_reddit
from stackoverflow_scraper import fetch_stackoverflow
from devto_scraper import fetch_devto


def generate_topics(domain: str) -> list:
    """
    Calls the LongCat LLM API to dynamically generate a list of 
    highly specific, technical topics based on the target domain.
    """
    print(f"\n[INFO] Contacting LongCat LLM to generate topics for domain: '{domain}'...")
    
    if not Config.LONGCAT_API_KEY:
        print("[ERROR] LongCat API Key missing. Falling back to default topics.")
        return ["RAG LLM", "YOLO object detection"]

    # Standard REST API structure for LLM text generation
    # (Adjust the endpoint URL if LongCat uses a specific base URL)
    endpoint = "https://api.longcat.chat/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {Config.LONGCAT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt Engineering: We force the LLM to output a clean, comma-separated string
    prompt = f"""
    You are an expert data analyst generating search terms for a web scraper. 
    I need a list of {Config.TOPIC_COUNT} popular, widely discussed, and practical topics within the domain of '{domain}'. 
    
    CRITICAL INSTRUCTIONS:
    1. The topics MUST have high search volume on developer sites like Reddit and StackOverflow. Focus on mainstream tools, common implementation challenges, or trending frameworks.
    2. Avoid hyper-niche, extreme, or overly academic terms. 
    3. Length: 2 to 4 words maximum per topic.
    4. Format: Natural search keywords (e.g., "RAG pipeline implementation", "YOLO object detection", "LLM fine-tuning").
    5. Diversity: Do not repeat the same primary keyword across the topics.
    
    Return ONLY a comma-separated list of the {Config.TOPIC_COUNT} topics, with no quotes, bullet points, or extra text.
    """


    payload = {
        "model": Config.LONGCAT_MODEL,
        "messages": [
            {"role": "system", "content": "You output strict, comma-separated lists only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=150)
        
        if response.status_code == 200:
            # Extract the raw text from the LLM response
            raw_text = response.json()["choices"][0]["message"]["content"]
            
            # Split the comma-separated string into a clean Python list
            topics = [t.strip() for t in raw_text.split(",") if t.strip()]
            
            print(f"[SUCCESS] LLM Generated {len(topics)} topics: {topics}")
            return topics
        else:
            print(f"[ERROR] LLM API returned Status Code: {response.status_code}")
            print(f"Details: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Failed to connect to LongCat API: {e}")

    # Safety fallback so your pipeline doesn't crash if the API goes down
    print("[WARN] Using fallback topics due to API failure.")
    return ["RAG LLM implementation", "YOLO object detection", "Graph Neural Networks"]



def main():
    print("="*60)
    print("Starting Knowledge Extraction Pipeline")
    print("="*60)

    # Retrieve target domain from environment configuration and generate search topics
    domain = Config.DOMAIN
    topics = generate_topics(domain)
    
    print("\n[INFO] Dispatching scrapers for configured platforms...")
    limit = Config.MAX_RECORDS
    all_raw_data = []

    # Iterate through the platforms defined in the environment variables
    # and route the topics to the corresponding scraping function
    for platform in Config.PLATFORMS:
        platform_name = platform.lower()
        
        if "reddit" in platform_name:
            df_reddit = fetch_reddit(topics, limit=limit)
            if not df_reddit.empty:
                all_raw_data.append(df_reddit)
                
        elif "stackoverflow" in platform_name:
            df_so = fetch_stackoverflow(topics, limit=limit)
            if not df_so.empty:
                all_raw_data.append(df_so)
                
        elif "devto" in platform_name or "medium" in platform_name:
            df_devto = fetch_devto(topics, limit=limit)
            if not df_devto.empty:
                all_raw_data.append(df_devto)
        else:
            print(f"[WARN] No matching scraper module found for '{platform}'. Skipping.")

    # Halt execution if all network requests failed or returned empty
    if not all_raw_data:
        print("[ERROR] Pipeline aborted. No data retrieved from any platform.")
        return

    # Merge individual platform dataframes into a single raw dataset
    raw_dataset = pd.concat(all_raw_data, ignore_index=True)
    print(f"\n[INFO] Aggregated {len(raw_dataset)} total raw records across all platforms.")

    print("\n[INFO] Initializing data sanitization and schema enforcement...")
    clean_dataset = prepare_dataset(raw_dataset)

    # Validate final output and persist to disk
    if not clean_dataset.empty:
        output_file = os.path.join(Config.RAW_DATA_DIR, "raw_dataset.csv")
        clean_dataset.to_csv(output_file, index=False)
        print("\n" + "="*60)
        print(f"[SUCCESS] Pipeline execution complete.")
        print(f"[SUCCESS] Extracted raw dataset persisted to: {output_file}")
        print("="*60)
    else:
        print("[ERROR] Dataset is empty post-cleaning. Verify text normalization logic.")

if __name__ == "__main__":
    main()