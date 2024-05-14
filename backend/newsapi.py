from eventregistry import *
import csv
MAX_RESULTS = 10
er = EventRegistry(apiKey = "2f1f8488-4167-4002-a914-03c30828fb5d")
iter = QueryArticlesIter(
    keywords = QueryItems.OR(["Finance"]),
    lang = "eng")
with open('news.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for art in iter.execQuery(er,
            sortBy = "date",
            maxItems = MAX_RESULTS,
            returnInfo = ReturnInfo(
                articleInfo = ArticleInfoFlags(
                    concepts = True,
                    categories = True)
            )):
        title = art.get('title', '')
        body = art.get('body', '')
        url = art.get('url', '')
        writer.writerow([title, url, body])
