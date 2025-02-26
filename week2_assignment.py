import requests

# NewsAPI Settings
api_key = "1742c16089274bb0bd036e19cf1e9a78"
base_url = "https://newsapi.org/v2/everything"

articles = []

def get_news(query="python", language="en", page_size=5):
    """
    Retrieves news from NewsAPI with a specific query.
    It returns the returned data in JSON format.
    """
    parameters = {
        "q": query,
        "language": language,
        "pageSize": page_size,
        "apiKey": api_key
    }
    try:
        response = requests.get(base_url, params=parameters)
        data = response.json()

        if data.get("status") == "ok":
            return data.get("articles", [])
        else:
            print("API received an unexpected response: ", data)
            return []
    except Exception as e:
        print("An error occurred while pulling news: ", str(e))
        return []

def create_article(article_data):
    """
    Adds a new news article to the local articles list.
    article_data is expected as a dictionary.
    Example: {"title": "New Article", "author": "Melih"}
    """
    articles.append(article_data)
    print(f"Article added: {article_data['title']}")

def read_articles():
    """
    Lists the news articles in the local articles list.
    """
    if not articles:
        print("No articles added yet.")
        return
    
    print("Available articles:")
    for idx, art in enumerate(articles, start=1):
        print(f"{idx}. {art.get('title', 'No title')} - {art.get('author', 'No author information')}")

def update_article(old_title, new_data):
    """
    Finds and updates news with a specific title (old_title).
    new_data contains the fields to update as a dictionary.
    Example: {'title': 'Updated title'}
    """
    for art in articles:
        if art.get("title") == old_title:
            art.update(new_data)
            print(f"The article titled '{old_title}' has been updated.")
            return
    print(f"Article titled '{old_title}' not found.")

def delete_article(title):
    """
    Deletes news with a specific title from the local list.
    """
    global articles
    new_articles = [art for art in articles if art.get("title") != title]
    if len(new_articles) < len(articles):
        articles = new_articles
        print(f"Deleted the article titled '{title}'.")
    else:
        print(f"Article titled '{title}' not found.")

def search_articles(keyword):
    """
    Searches the local list for articles containing keyword in the title or description.
    """
    results = []
    for art in articles:
        title = (art.get("title") or "").lower()
        description = (art.get("description") or "").lower()  # Use empty string if description None
        if keyword.lower() in title or keyword.lower() in description:
            results.append(art)
    
    print(f"Articles matching keyword '{keyword}':")
    if results:
        for idx, art in enumerate(results, start=1):
            print(f"{idx}. {art.get('title')} - {art.get('author')}")
    else:
        print("No matching articles found.")

def main():
    # 1) Pull news from API
    print("News from API is being pulled...")
    fetched_articles = get_news(query="python", language="en", page_size=5)
    print(f"Fetched {len(fetched_articles)} articles from API.\n")
    
    # 2) Add captured news to local list (CREATE operation)
    for art in fetched_articles:
        article_data = {
            "title": art.get("title", "No Title"),
            "description": art.get("description", "No Description"),
            "author": art.get("author", "Unknown Author"),
            "url": art.get("url", "No URL")
        }
        create_article(article_data)
    
    # 3) List current articles (READ operation)
    print("\n--- Listing Articles After Creation ---")
    read_articles()
    
    # 4) Example update (UPDATE operation)
    if articles:
        old_title = articles[0]["title"]
        update_article(old_title, {"title": "Updated Title", "author": "Melih Akdogan"})
    
    print("\n--- Listing Articles After Update ---")
    read_articles()
    
    # 5) Delete an article (DELETE operation)
    delete_article("Updated Title")
    
    print("\n--- Listing Articles After Deletion ---")
    read_articles()
    
    # 6) Search operation
    search_keyword = "python"
    print("\n--- Search Operation ---")
    search_articles(search_keyword)
    
    # Keep the terminal open until Enter is pressed
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()


                                   
        
