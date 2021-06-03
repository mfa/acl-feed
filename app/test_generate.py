from generate import generate_feed
from parse import parse_html


def test_generate_feed(example_html):
    feed_data = parse_html(example_html, "andreas-madsack")
    result = generate_feed(feed_data)
    assert result.decode().startswith(
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en"><id>andreas-madsack</id><title>ACL Antology for Andreas Madsack</title>'
    )
