from pathlib import Path

import httpx
import pytest
from generate import generate_feed_atom
from parse import parse_html


@pytest.fixture
def example_html(request):
    if request.param:
        try:
            response = httpx.get(
                "https://aclanthology.org/people/andreas-madsack/",
                follow_redirects=True,
                headers={"User-Agent": "acl-feed/1 (+https://acl-feed.madflex.de)"},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            pytest.skip(f"aclanthology.org not reachable: {exc}")
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
    assert len(feed) == 6
    assert feed[0].keys() == {
        "abstract",
        "authors",
        "link",
        "title",
        "volume",
        "volume_link",
        "year",
    }
    assert set(feed[-1].get("authors")) == {"Andreas Madsack", "Robert Weißgraeber"}
    assert feed[-1]["year"] == "2017"
    assert feed[-1]["link"] == "/W17-3524/"


@pytest.mark.parametrize("example_html", (False, True), indirect=True)
def test_generate_feed(example_html):
    feed_data = parse_html(example_html, "andreas-madsack")
    result = generate_feed_atom(feed_data)
    # FIXME: not the best way to test this
    assert len(result.decode()) in (5666, 5667)
