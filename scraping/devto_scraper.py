import requests
import pandas as pd
import time

def fetch_devto(topics, limit=100):
    """
    Fetches articles from Dev.to using their official public API.
    """
    all_data = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"Starting Dev.to (Blog Platform) Data Collection for {len(topics)} topics...")

    # The official public API endpoint
    url = "https://dev.to/api/articles"

    for topic in topics:
        print(f"Fetching: '{topic}'...")
        
        topic_data = []
        page = 1
        
        while len(topic_data) < limit:
            # API parameters for search and pagination
            params = {
                "q": topic,         # Search query
                "per_page": 100,    # Max results per page
                "page": page        # Current page number
            }
            
            try:
                res = requests.get(url, headers=headers, params=params, timeout=10)
                
                if res.status_code == 200:
                    articles = res.json()
                    
                    if not articles:
                        break # No more articles found for this topic
                        
                    for article in articles:
                        title = article.get("title", "")
                        desc = article.get("description", "")
                        
                        topic_data.append({
                            "topic": topic,
                            "platform": "Dev.to", 
                            "title": title,
                            "text": f"{title}. {desc}", # Combine title and description
                            "date": article.get("published_at"),
                            "engagement": article.get("public_reactions_count", 0), 
                            "url": article.get("url") # Official URL
                        })
                        
                        if len(topic_data) >= limit:
                            break
                            
                    page += 1
                    time.sleep(1) # Polite API delay
                    
                elif res.status_code == 429:
                    print("Rate limit hit. Waiting 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"Error {res.status_code}, retrying...")
                    time.sleep(3)
                    break # Exit retry loop on hard errors
                    
            except Exception as e:
                print(f"Request Error: {e}")
                break

        if topic_data:
            topic_df = pd.DataFrame(topic_data)
            all_data.append(topic_df)
            print(f"   -> Successfully grabbed {len(topic_df)} articles using query: '{topic}'")
        else:
            print(f"   -> Failed to fetch Dev.to data for topic: {topic}. Query might be too niche.")
            
        time.sleep(2) # Politeness delay between topics

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        print("\n" + "="*50)
        print(f"Dev.to Collection Complete!")
        print(f"Total Rows Collected: {len(final_df)}")
        print("="*50)
        return final_df
    else:
        print("Critical Failure: No data collected from Dev.to.")
        return pd.DataFrame()


# --- Testing Block ---
if __name__ == "__main__":
    test_topics = [
        "RAG LLM", 
        "yolo object detection"
    ]
    
    df = fetch_devto(test_topics, limit=100)
    
    if not df.empty:
        print("\nPreview of the returned DataFrame:")
        print(df[['topic', 'title', 'engagement']].head())