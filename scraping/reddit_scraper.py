import requests
import pandas as pd
import time
from datetime import datetime

def fetch_reddit(topics, limit=100):
    """
    Fetches and processes posts from Reddit for a given list of topics.
    
    Args:
        topics (list): A list of topic strings to search for.
        limit (int): Maximum number of posts to retrieve per topic. Default is 100.
        
    Returns:
        pd.DataFrame: A clean pandas DataFrame containing data for all topics.
                      Returns an empty DataFrame if collection fails.
    """
    url = "https://www.reddit.com/search.json"
    
    # Custom User-Agent to prevent Reddit from instantly blocking the script
    headers = {
        "User-Agent": "python:projectdatacollector:v1.0 (by /u/your_reddit_username)"
    }

    all_data = [] # Will hold individual DataFrames for each topic

    print(f"Starting Reddit Data Collection for {len(topics)} topics...")

    # Iterate through each topic in the provided list
    for topic in topics:
        print(f"Fetching: '{topic}'...")
        
        # Define search parameters for the Reddit API
        params = {
            "q": topic,
            "limit": limit,
            "sort": "relevance", # Ensure we get the most highly discussed content
            "t": "all"           # Search across all time, not just recent
        }

        topic_data = [] # Temporarily holds dictionaries for the current topic
        
        # Retry mechanism: Attempt to fetch up to 3 times per topic
        for attempt in range(3):  
            try:
                res = requests.get(url, headers=headers, params=params, timeout=10)

                # 200 OK: Successfully retrieved data
                if res.status_code == 200:
                    data_json = res.json()
                    posts = data_json.get("data", {}).get("children", [])
                    
                    for p in posts:
                        d = p.get("data", {})
                        
                        # Clean and format the date from Unix timestamp to YYYY-MM-DD HH:MM:SS
                        raw_date = d.get("created_utc")
                        formatted_date = datetime.fromtimestamp(raw_date).strftime('%Y-%m-%d %H:%M:%S') if raw_date else None

                        # Append the extracted fields to our temporary list
                        topic_data.append({
                            "topic": topic,
                            "platform": "Reddit",
                            "title": d.get("title"),
                            "text": d.get("selftext") or d.get("title"), # Fallback to title if post body is empty
                            "date": formatted_date,
                            "engagement": d.get("score"),
                            "url": "https://reddit.com" + d.get("permalink", "")
                        })
                    
                    break # Break out of the retry loop if successful
                    
                # 429 Too Many Requests: Rate limited by Reddit
                elif res.status_code == 429:
                    print(f"Rate limited by Reddit. Waiting 10 seconds...")
                    time.sleep(10)
                    
                # Other errors (e.g., 403 Forbidden, 500 Server Error)
                else:
                    print(f"Error {res.status_code}, retrying...")
                    time.sleep(3)

            except Exception as e:
                print(f"Request Error: {e}")
                time.sleep(3)

        # If data was successfully collected for this topic, convert to DataFrame and store
        if topic_data:
            topic_df = pd.DataFrame(topic_data)
            all_data.append(topic_df)
            print(f"   -> Successfully grabbed {len(topic_df)} posts.")
        else:
            print(f"   -> Failed to fetch Reddit data for topic: {topic}")

        # Politeness delay to avoid overloading Reddit's servers
        time.sleep(2) 

    # Combine all topic DataFrames into one master DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        print("\n" + "="*50)
        print(f"Reddit Collection Complete!")
        print(f"Total Rows Collected: {len(final_df)}")
        print("="*50)
        return final_df
    else:
        print("Critical Failure: No data collected from Reddit.")
        return pd.DataFrame()


# --- Testing Block ---
if __name__ == "__main__":
    test_topics = [
        "Retrieval-Augmented Generation RAG implementation",
        "YOLO11s object detection deployment"
    ]
    
    # Run the function
    df = fetch_reddit(test_topics, limit=100)
    
    # Preview the cleaned data in the terminal
    if not df.empty:
        print("\nPreview of the returned DataFrame:")
        print(df[['topic', 'title', 'date', 'engagement']].head())
