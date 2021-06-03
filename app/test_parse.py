from parse import parse_html


def test_parse_html(example_html):
    result = parse_html(example_html, "andreas-madsack")
    assert result["feed_title"] == "Andreas Madsack"

    feed = result["feed"]
    assert len(feed) == 5
    assert feed[0].keys() == {
        "abstract",
        "authors",
        "link",
        "title",
        "volume",
        "volume_link",
        "year",
    }
    assert set(feed[0].get("authors")) == {"Andreas Madsack", "Robert Weißgraeber"}
    assert feed[0]["year"] == "2019"
    assert feed[0]["link"] == "/anthology/W19-4201/"
