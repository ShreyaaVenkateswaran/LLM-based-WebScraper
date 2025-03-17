from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key="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")

def scrape_news_article(url):
    """Scrape the text content of a news article."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from paragraphs (customize based on the website structure)
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])
    return article_text

def summarize_text(text):
    """Summarize the text using Groq API."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Use a suitable model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": f"Summarize the following news article in 3 sentences:\n{text}"}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        try:
            # Scrape the article
            article_text = scrape_news_article(url)
            # Summarize the article
            summary = summarize_text(article_text)
            return render_template("index.html", summary=summary, url=url)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)