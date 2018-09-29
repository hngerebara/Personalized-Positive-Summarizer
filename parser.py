
from goose import Goose
import cPickle as pickle
import feedparser

g = Goose()

def save(db):
    """
    save the database
    """
    pickle.dump(db, open("data/db.pickle", "w"), -1)
    
def load():
    """
    load the database
    """
    try:
        db = pickle.load(open("data/db.pickle"))
	
    except:
        print "Unable to load database!"
        db = {}
    return db

def get_urls(feed_url, n=12):
    """
    extract urls from rss feed
    """
    feed = feedparser.parse(feed_url)
    urls = []
    for e in feed.entries:
        urls.append(e.link)

        if len(urls) >= n:
            break

    return urls

def reload_data(feeds):
    """
    refresh the database
    """
    db = {}
    for cat in feeds:
        urls = get_urls(feeds[cat], n=50)
        for url in urls:
            a = g.extract(url)
            title = a.title
            text = a.cleaned_text
            if not cat in db:
                db[cat] = {}
            db[cat][url] = (title, text)

    save(db)

def get_db():
    """
    load and returns the db to
    web application
    """
    db = load()
    return db

def test():
    print "Building the database. May take few minutes....."
    feeds = {"ent": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
             "tech": "http://feeds.bbci.co.uk/news/technology/rss.xml",
		"sci": "http://www.bbc.co.uk/science/0/rss.xml",
		"nature": "http://feeds.bbci.co.uk/nature/rss.xml",
		"uk": "http://feeds.bbci.co.uk/news/uk/rss.xml",
		"world": "http://feeds.bbci.co.uk/news/world/rss.xml",
		"latest": "http://feeds.bbci.co.uk/news/system/latest_published_content/rss.xml",
		"africa": "http://feeds.bbci.co.uk/news/world/africa/rss.xml",
		"football": "http://feeds.bbci.co.uk/sport/0/football/rss.xml?edition=uk",
		"tennis": "http://feeds.bbci.co.uk/sport/0/tennis/rss.xml?edition=uk",
		"allsports": "http://feeds.bbci.co.uk/sport/0/rss.xml?edition=uk"
}
    reload_data(feeds)

if __name__ == '__main__':
    test()
