import pytest
from python_sidecar.xhs.feeds import list_feeds, search_feeds

SAMPLE_FEEDS_SNAPSHOT = """\
link "card" [ref=e1]
link "card" [ref=e2]
link "card" [ref=e3]
textbox "搜索" [ref=e4]
"""


@pytest.mark.asyncio
async def test_list_feeds_parses_cards(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_FEEDS_SNAPSHOT
    feeds = await list_feeds()
    assert len(feeds) == 3


@pytest.mark.asyncio
async def test_search_feeds_fills_keyword(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_FEEDS_SNAPSHOT
    feeds = await search_feeds("美食")
    assert len(feeds) == 3
    mock_agent_browser["fill"].assert_called_with("@e4", "美食")
