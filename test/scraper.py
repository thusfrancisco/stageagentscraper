from src.scraper import *
from playwright.sync_api import Page


def test_begin_page(page: Page):
    assert page.title() == "Theatre Shows | Guides for Theatre | StageAgent"


def test_goto_show_page(page: Page, mock_show_id: int):
    assert goto_show_page(page, show_id=mock_show_id).title() == "Wicked (Musical) Plot & Characters | StageAgent"


def test_get_normalized_show_name(page: Page, mock_show_id: int):
    page = goto_show_page(page, show_id=mock_show_id)

    assert get_normalized_show_name(page) == "wicked"


def test_goto_characters_page(page: Page, mock_show_id: int):
    page = goto_show_page(page, show_id=mock_show_id)
    normalized_musical_name = get_normalized_show_name(page)

    page = goto_characters_page(page, show_id=mock_show_id, show_name=normalized_musical_name)

    assert f"stageagent.com/shows/musical/{mock_show_id}/{normalized_musical_name}/characters" in page.url
    assert page.title() == "Wicked (Musical) Characters | StageAgent"


def test_get_character_table_locator(page: Page, mock_show_id: int):
    page = goto_show_page(page, show_id=mock_show_id)
    normalized_musical_name = get_normalized_show_name(page)

    page = goto_characters_page(page, show_id=mock_show_id, show_name=normalized_musical_name)

    assert get_character_table_locator(page).inner_html()


def test_get_character_listing(page: Page, mock_show_id: int):
    page = goto_show_page(page, show_id=mock_show_id)
    normalized_musical_name = get_normalized_show_name(page)

    page = goto_characters_page(page, show_id=mock_show_id, show_name=normalized_musical_name)
    
    character_listing = get_character_listing_list(page)

    # Assert the characters list isn't empty, and that each character_listing contains some HTML.
    assert len(character_listing) > 0
    for character in character_listing:
        assert character.inner_html() != ""


def test_get_character_url(page: Page, mock_show_id: int):
    page = goto_show_page(page, show_id=mock_show_id)
    normalized_musical_name = get_normalized_show_name(page)

    page = goto_characters_page(page, show_id=mock_show_id, show_name=normalized_musical_name)
    
    character_listing = get_character_listing_list(page)
    character_urls = list(map(get_character_url, character_listing))

    assert "https://www.stageagent.com/characters/2987/wicked/galinda-glinda" in character_urls
