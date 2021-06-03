from pathlib import Path

import pytest


@pytest.fixture
def example_html():
    fn = Path(__file__).parent.absolute() / "fixtures/andreas-madsack.html"
    yield fn.open().read()
