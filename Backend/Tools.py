import requests
from bs4 import BeautifulSoup

def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q{query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all("span", class_="BNeawe")
        if results:
            return results[0].text
        return "No results Found."
    except Exception as e:
        return f"Error during search: {str(e)}"