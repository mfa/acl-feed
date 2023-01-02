from bs4 import BeautifulSoup


def parse_meta(data):
    meta = {"authors": []}
    for item in data.children:
        if item.name == "strong":
            meta["title"] = item.text
            meta["link"] = item.find("a")["href"]
        if item.name == "a":
            if "/people/" in item["href"]:
                meta["authors"].append(item.text)
            else:
                meta["volume"] = item.text
                meta["volume_link"] = "https://www.aclweb.org" + item["href"]
    return meta


def parse_html(html_data, slug):
    soup = BeautifulSoup(html_data, "lxml")

    title = " ".join([i.text for i in soup.find(id="title").find_all("span")])

    main_column = soup.find(id="main").find_all("div", class_="col-lg-9")[0]
    feed = []
    element = {}
    year = ""

    for item in main_column.children:
        if item.name == "h4":
            year = item.text
        elif item.name == "p":
            if element:
                feed.append(element)
            children = list(item.children)
            badges = children[0]
            meta = children[-1]
            element = parse_meta(meta)
            element["year"] = year
        elif item.name == "div" and "card" in item["class"]:
            element["abstract"] = item.text
    if element:
        feed.append(element)

    return {"feed_title": title, "feed": feed, "slug": slug}
