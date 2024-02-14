import base64
from bs4 import BeautifulSoup
import cloudscraper
import time

scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

words_to_look = {
    'spiser': '',
    'spidser': '',
}

source = "https://www.bog-ide.dk/produkt/134230/jussi-adler-olsen-kvinden-i-buret-paperback/3128299"

sections = []
for word_to_look, word_meaning in words_to_look.items():
    url = f"https://forvo.com/word/{word_to_look}/#da"
    info = scraper.get(url).text
    soup = BeautifulSoup(info, "html.parser")
    danish = soup.find("div", id="language-container-da")

    section = '\t\t\t\t\t<section class="word-section">\n'
    header = f'\t\t\t\t\t\t<h2 class="word-header">{word_to_look}: <span class="word-meaning">{word_meaning}</span></h2>\n'
    section += header
    section += f'\t\t\t\t\t\t<p class="word-link">Виж в ordnet: <a href="https://ordnet.dk/ddo/ordbog?query={word_to_look}" target=_blank>{word_to_look}</a></p>\n'

    if danish:
        word_list = danish.find_all("li", class_ = "pronunciation li-active")
        section += '\t\t\t\t\t\t<ul class="word-results">\n'
        for word in word_list:
            word_container = word.find('div', class_ ="play")
            decoded_audio_path = base64.b64decode(word_container['onclick'].split(",")[1])
            prefix = "https://audio12.forvo.com/mp3/"
            word_link = prefix + decoded_audio_path.decode()
            li = f"\t\t\t\t\t\t\t<li class=\"word-audio\">\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t<audio controls src= '{word_link}'>\n\t\t\t\t\t\t\t\t\t<a href={word_link}>{word_to_look}</a>\n\t\t\t\t\t\t\t\t</audio>\n\t\t\t\t\t\t\t</li>\n"
            section += li
            time.sleep(10)
        section += "\t\t\t\t\t\t</ul>\n\t\t\t\t\t</section>"
    else:
        section += f'\t\t\t\t<h4>Във forvo.com няма открити произношения за <span>{word_to_look}</span>.</h4>\n'
        section += f'\t\t\t\t<p>Това може да се дължи на някоя от следните причини:</p>\n'
        section += '\t\t\t\t<ul>\n'
        section += '\t\t\t\t\t<li>Грешка при изписването на думата. Моля провери как е изписана думата!</li>\n'
        section += '\t\t\t\t\t<li>Произношението може все още да не е добавено във forvo.com</li>\n'
        section += '\t\t\t\t</ul>\n'
        section += f"\t\t\t\t</ul>\n"
        section += f'\t\t\t<p class="word-link">Добави <a href = https://forvo.com/search/{word_to_look}/>{word_to_look}</a> към forvo.com, за бъде добавено произношение.</p></section>'

    sections.append(section)

NEW_LINE = '\n'
html = f"""<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Forvo pronunciations</title>
        <link rel="stylesheet" href="./index.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet"> 
    </head>
    <body>
        <div class="container">
            <header>
                <div class="header">
                    <h1>Welcome to My Website</h1>
                </div> 
            </header>
            <main>
                <div class="main">
                    <h2 class="main-title">Here are the results from your search:</h2>
                    <h4 class="source-link"><a href={source} target=_blank>Click to visit words' source</a></h4>
                    {NEW_LINE.join(sections)}
                </div>
            </main>
            <footer>
                <div class="footer">
                    <h3>TBA</h3>
                </div>
            </footer>
        </div>
    </body>
</html>
"""
with open('docs/index.html', "w", encoding="utf-8") as writer:
    writer.write(html)


# info:
# https://www.google.com/search?client=firefox-b-d&q=python+open+file+in+application
# https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
import os
os.system("start " + 'docs/index.html')
