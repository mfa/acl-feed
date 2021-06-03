from pprint import pprint

from feedgen.feed import FeedGenerator


def generate_feed(parsed_feed):
    fg = FeedGenerator()
    person = parsed_feed["feed_title"]
    fg.title(f"ACL Antology for {person}")
    fg.author({"name": person})
    slug = parsed_feed["slug"]
    fg.id(slug)
    fg.link(href=f"https://acl-feed.madflex.de/{slug}.atom", rel="self")
    fg.language("en")
    fg.generator(generator="acl-feed", uri="https://acl-feed.madflex.de", version="1")

    for item in parsed_feed.get("feed"):
        fe = fg.add_entry()
        fe.id(item["link"].split("/")[-2])
        fe.title(item["title"])
        fe.link(href="https://www.aclweb.org" + item["link"])
        fe.author({"name": ", ".join(item["authors"])})
        content = "<p>In: " + item["volume"] + "</p>"
        if "abstract" in item:
            content += item["abstract"]
        fe.content(content)

    return fg.atom_str()
