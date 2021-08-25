from pathlib import Path

import httpx
import pytest
from generate import generate_feed
from parse import parse_html


@pytest.fixture
def example_html(request):
    if request.param:
        response = httpx.get(
            "https://www.aclweb.org/anthology/people/a/andreas-madsack/"
        )
        data = response.text
    else:
        fn = Path(__file__).parent.absolute() / "fixtures/andreas-madsack.html"
        data = fn.open().read()
    yield data


@pytest.mark.parametrize("example_html", (False, True), indirect=True)
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
    assert feed[0]["link"] == "/W19-4201/"


@pytest.mark.parametrize("example_html", (False, True), indirect=True)
def test_generate_feed(example_html):
    feed_data = parse_html(example_html, "andreas-madsack")
    result = generate_feed(feed_data)
    # FIXME: not the best way to test this
    assert len(result.decode()) == 4169
