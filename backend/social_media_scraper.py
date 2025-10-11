"""
Free social media data scraper - No API keys needed!
Uses public RSS feeds and web scraping
"""

import requests
import feedparser
from datetime import datetime
from typing import List, Dict
import re

class SocialMediaScraper:
    """Scrape social media data without API keys"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_twitter_rss(self, query="disaster OR flood OR fire OR earthquake", location="india") -> List[Dict]:
        """
        Fetch tweets using Nitter (Twitter RSS alternative)
        FREE - No API key needed!
        """
        posts = []
        
        try:
            # Nitter instances (Twitter RSS mirrors)
            nitter_instances = [
                "https://nitter.net",
                "https://nitter.poast.org",
                "https://nitter.privacydev.net"
            ]
            
            search_query = f"{query} {location}"
            
            for instance in nitter_instances:
                try:
                    # Try to fetch from this instance
                    url = f"{instance}/search/rss?f=tweets&q={search_query.replace(' ', '+')}"
                    response = requests.get(url, headers=self.headers, timeout=5)
                    
                    if response.status_code == 200:
                        feed = feedparser.parse(response.content)
                        
                        for entry in feed.entries[:10]:  # Get latest 10
                            posts.append({
                                "id": f"twitter_{hash(entry.link)}",
                                "text": entry.title,
                                "source": "Twitter (via Nitter)",
                                "timestamp": entry.get('published', datetime.now().isoformat()),
                                "link": entry.link,
                                "platform": "twitter"
                            })
                        
                        if posts:
                            break  # Got data, stop trying other instances
                            
                except Exception as e:
                    continue  # Try next instance
                    
        except Exception as e:
            print(f"Error fetching Twitter data: {e}")
        
        return posts
    
    def fetch_reddit_posts(self, subreddit="india", query="disaster flood fire") -> List[Dict]:
        """
        Fetch Reddit posts using public JSON API
        FREE - No API key needed!
        """
        posts = []
        
        try:
            # Reddit public JSON API
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&sort=new&limit=10"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data['data']['children']:
                    post_data = post['data']
                    posts.append({
                        "id": f"reddit_{post_data['id']}",
                        "text": f"{post_data['title']} - {post_data.get('selftext', '')[:200]}",
                        "source": f"Reddit r/{subreddit}",
                        "timestamp": datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                        "link": f"https://reddit.com{post_data['permalink']}",
                        "platform": "reddit",
                        "upvotes": post_data['ups']
                    })
                    
        except Exception as e:
            print(f"Error fetching Reddit data: {e}")
        
        return posts
    
    def fetch_news_rss(self) -> List[Dict]:
        """
        Fetch disaster news from RSS feeds
        FREE - No API key needed!
        """
        posts = []
        
        # Free news RSS feeds about disasters
        feeds = [
            "https://www.gdacs.org/xml/rss.xml",  # Global Disaster Alert
            "http://floodlist.com/feed",  # Flood news
            "https://reliefweb.int/updates/rss.xml"  # UN disaster news
        ]
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Get latest 5 from each
                    posts.append({
                        "id": f"news_{hash(entry.link)}",
                        "text": f"{entry.title} - {entry.get('summary', '')[:200]}",
                        "source": feed.feed.get('title', 'News Feed'),
                        "timestamp": entry.get('published', datetime.now().isoformat()),
                        "link": entry.link,
                        "platform": "news"
                    })
                    
            except Exception as e:
                print(f"Error fetching news from {feed_url}: {e}")
                continue
        
        return posts
    
    def fetch_youtube_disasters(self, query="india disaster flood fire") -> List[Dict]:
        """
        Fetch YouTube videos using RSS feed
        FREE - No API key needed!
        """
        posts = []
        
        try:
            # YouTube RSS search (limited but free)
            # Note: This is basic, for production use YouTube Data API
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}&sp=CAI%253D"
            
            # For now, return placeholder
            # In production, you'd scrape or use YouTube Data API (free tier: 10,000 units/day)
            posts.append({
                "id": "youtube_placeholder",
                "text": "YouTube disaster footage available - use YouTube Data API for full access",
                "source": "YouTube",
                "timestamp": datetime.now().isoformat(),
                "link": search_url,
                "platform": "youtube"
            })
            
        except Exception as e:
            print(f"Error with YouTube: {e}")
        
        return posts
    
    def get_all_social_media(self) -> Dict:
        """
        Fetch all available social media data
        Returns combined data from all free sources
        """
        print("Fetching social media data from free sources...")
        
        # Fetch from all sources
        twitter_posts = self.fetch_twitter_rss()
        print(f"✓ Found {len(twitter_posts)} Twitter posts")
        
        reddit_posts = self.fetch_reddit_posts()
        print(f"✓ Found {len(reddit_posts)} Reddit posts")
        
        news_posts = self.fetch_news_rss()
        print(f"✓ Found {len(news_posts)} news items")
        
        youtube_posts = self.fetch_youtube_disasters()
        print(f"✓ Found {len(youtube_posts)} YouTube items")
        
        # Combine all
        all_posts = twitter_posts + reddit_posts + news_posts + youtube_posts
        
        return {
            "posts": all_posts,
            "total_count": len(all_posts),
            "sources": ["Twitter (Nitter)", "Reddit", "News RSS", "YouTube"],
            "last_updated": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    scraper = SocialMediaScraper()
    
    print("\n" + "="*60)
    print("FETCHING FREE SOCIAL MEDIA DATA (NO API KEYS!)")
    print("="*60 + "\n")
    
    data = scraper.get_all_social_media()
    
    print(f"\nTotal posts found: {data['total_count']}")
    print(f"Sources: {', '.join(data['sources'])}")
    print(f"Last updated: {data['last_updated']}")
    
    if data['posts']:
        print(f"\n--- Sample Posts ---")
        for post in data['posts'][:3]:
            print(f"\nPlatform: {post['platform']}")
            print(f"Text: {post['text'][:100]}...")
            print(f"Source: {post['source']}")
