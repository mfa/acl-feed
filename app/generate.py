from pprint import pprint

from feedgen.feed import FeedGenerator


def generate_feed(parsed_feed):
    fg = FeedGenerator()
    person = parsed_feed["feed_title"]
    fg.title(f"{person} (ACL Antology)")
    fg.author({"name": person})
    slug = parsed_feed["slug"]
    fg.id(f"https://aclanthology.org/people/{slug[0]}/{slug}/")
    fg.link(href=f"https://acl-feed.madflex.de/{slug}.atom", rel="self")
    fg.language("en")
    fg.generator(generator="acl-feed", uri="https://acl-feed.madflex.de", version="1")

    return fg


def generate_feed_atom(parsed_feed):
    fg = generate_feed(parsed_feed)

    for item in reversed(parsed_feed.get("feed", [])):
        fe = fg.add_entry()
        fe.id("https://aclanthology.org/" + item["link"].split("/")[-2])
        fe.title(item["title"])
        fe.link(href="https://aclanthology.org" + item["link"])
        fe.author({"name": ", ".join(item["authors"])})
        content = "<p>In: " + item["volume"] + "</p>"
        if "abstract" in item:
            content += item["abstract"]
        fe.content(content, type="html")

    return fg.atom_str()


def generate_feed_rss(parsed_feed):
    fg = generate_feed(parsed_feed)
    slug = parsed_feed["slug"]
    fg.link(href=f"https://acl-feed.madflex.de/{slug}.rss", rel="self")
    fg.description(".")

    for item in reversed(parsed_feed.get("feed", [])):
        fe = fg.add_entry()
        _id = "https://aclanthology.org/" + item["link"].split("/")[-2]
        fe.id(_id)
        fe.guid(_id, permalink=True)
        fe.title(item["title"])
        fe.link(href="https://aclanthology.org" + item["link"])
        fe.author({"name": ", ".join(item["authors"])})
        content = "<p>In: " + item["volume"] + "</p>"
        if "abstract" in item:
            content += item["abstract"]
        fe.content(content, type="html")

    return fg.rss_str()
