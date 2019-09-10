# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPError
import pycrfsuite


if __name__ == "__main__":
    base_url = "http://www.thelatinlibrary.com/"
    home_content = urlopen(base_url)
    soup = BeautifulSoup(home_content, "lxml")
    author_page_links = soup.find_all("a")
    author_pages = [ap["href"] for i, ap in enumerate(author_page_links) if i < 49]
    ap_content = list()
    texts = list()
    for ap in author_pages:
        ap_content.append(urlopen(base_url + ap))

    #
    book_links = list()
    for path, content in zip(author_pages, ap_content):
        author_name = path.split(".")[0]
        ap_soup = BeautifulSoup(content, "lxml")
        book_links += ([link for link in ap_soup.find_all("a", {"href": True}) if author_name in link["href"]])
    # print(book_links[0])

    #
    texts = list()
    count = 0
    num_pages = 200
    with open("H:\\TanBoOwn\\Github\\CRF\\crf_train_corpus.txt", "w", encoding="utf-8") as f:
        for i, bl in enumerate(book_links[:num_pages]):
            # print("Getting content " + str(i + 1) + " of " + str(num_pages), end="\r", flush=True)
            try:
                content = urlopen(base_url + bl["href"]).read()
                # texts.append(content)
                # print("Document " + str(count + 1) + " of " + str(len(texts)), end="\r", flush=True)
                textSoup = BeautifulSoup(content, "lxml")
                paragraphs = textSoup.find_all("p", attrs={"class": None})
                prepared = ("".join([p.text.strip().lower() for p in paragraphs[1:-1]]))
                for t in prepared.split("."):
                    part = "".join([c for c in t if c.isalpha() or c.isspace()])
                    if len(part) > 5:
                        f.write(part)
                        f.write("\r\n")
            except HTTPError as err:
                print("Unable to retrieve " + bl["href"] + ".")
                continue
            count += 1







