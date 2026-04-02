import requests
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_stackoverflow(topics, limit=100):
    all_data = []
    print(f"Starting StackOverflow Data Collection for {len(topics)} topics...")

    url = "https://api.stackexchange.com/2.3/search/advanced"

    for topic in topics:
        print(f"Fetching: '{topic}'...")
        
        topic_data = []
        page = 1 
        
        while len(topic_data) < limit:
            # Passes the exact dynamic topic string directly to the search query
            params = {
                "page": page,
                "pagesize": 100, 
                "order": "desc",
                "sort": "relevance",
                "q": topic, 
                "site": "stackoverflow",
                "filter": "withbody"         
            }

            try:
                res = requests.get(url, params=params, timeout=10)
                
                if res.status_code == 200:
                    items = res.json().get("items", [])
                    
                    if not items:
                        break # No more pages left
                        
                    for item in items:
                        raw_html = item.get("body", "")
                        clean_text = BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

                        topic_data.append({
                            "topic": topic, 
                            "platform": "StackOverflow",
                            "title": item.get("title"),
                            "text": clean_text,
                            "date": datetime.fromtimestamp(item.get("creation_date")).strftime('%Y-%m-%d %H:%M:%S'),
                            "engagement": item.get("score", 0), 
                            "url": item.get("link")
                        })
                        
                        if len(topic_data) >= limit:
                            break
                            
                    page += 1 
                    time.sleep(1) # Be polite to the API
                    
                elif res.status_code in [400, 429]:
                    print("Rate limit hit. Waiting 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"Error {res.status_code}, retrying...")
                    time.sleep(3)
                    
            except Exception as e:
                print(f"Request Error: {e}")
                break

        if topic_data:
            topic_df = pd.DataFrame(topic_data)
            all_data.append(topic_df)
            print(f"   -> Successfully grabbed {len(topic_df)} posts using query: '{topic}'")
        else:
            print(f"   -> Failed to fetch StackOverflow data for topic: {topic}")
            
        time.sleep(2) 

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        print("\n" + "="*50)
        print(f"StackOverflow Collection Complete!")
        print(f"Total Rows Collected: {len(final_df)}")
        print("="*50)
        return final_df
    else:
        print("Critical Failure: No data collected from StackOverflow.")
        return pd.DataFrame()


# --- Testing Block ---
if __name__ == "__main__":
    # Test with generic search terms that a dynamic pipeline might generate
    test_topics = [
        "RAG LLM", 
        "yolo object detection"
    ]
    
    df = fetch_stackoverflow(test_topics, limit=100)
    
    if not df.empty:
        print("\nPreview of the returned DataFrame:")
        print(df[['topic', 'title', 'engagement']].head())