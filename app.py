from flask import Flask,render_template,request
from newsapi import NewsApiClient
app = Flask(__name__)

newsapi = NewsApiClient(api_key='87eddeebf3f34e009bf55a7b327f8c19')

def get_sources_and_domains():
    all_sources = newsapi.get()['sources']
    sources = []
    domains = []
    for i in all_sources:
        id = i['id']
        domain = i['url'].replace("http://","")
        domain = domain.replace("https://","")
        domain = domain.replace("www.","")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources,domains

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword, sources = sources, domains= domains, language='en',sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,
                                              sources=sources,
                                              domains=domains,
                                              language='en',
                                              sort_by='relevancy',
                                              page_size=no_of_articles)['articles']
        return render_template("home.html", all_articles=all_articles,
                               keyword=keyword)
    else:
        top_headlines = newsapi.get_top_headlines(country="in", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="in",
                                                  language="en",
                                                  page_size=total_results)['articles']
        return render_template("home.html", all_headlines=all_headlines)
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
