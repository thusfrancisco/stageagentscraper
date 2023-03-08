from src.scraper import *
from playwright.sync_api import Page


def test_begin_page(page: Page):
    assert page.title() == "Theatre Shows | Guides for Theatre | StageAgent"


def test_goto_musical_page(page: Page, mock_musical_id: int):
    assert goto_musical_page(page, musical_id=mock_musical_id).title() == "Wicked (Musical) Plot & Characters | StageAgent"


def test_get_normalized_musical_name(page: Page, mock_musical_id: int):
    page = goto_musical_page(page, musical_id=mock_musical_id)

    assert get_normalized_musical_name(page) == "wicked"


def test_goto_characters_page(page: Page, mock_musical_id: int):
    page = goto_musical_page(page, musical_id=mock_musical_id)
    normalized_musical_name = get_normalized_musical_name(page)

    page = goto_characters_page(page, musical_id=mock_musical_id, musical_name=normalized_musical_name)

    print(mock_musical_id, normalized_musical_name)
    assert f"stageagent.com/shows/musical/{mock_musical_id}/{normalized_musical_name}/characters" in page.url
    assert page.title() == "Wicked (Musical) Characters | StageAgent"


def test_get_character_table_locator(page: Page, mock_musical_id: int):
    page = goto_musical_page(page, musical_id=mock_musical_id)
    normalized_musical_name = get_normalized_musical_name(page)

    page = goto_characters_page(page, musical_id=mock_musical_id, musical_name=normalized_musical_name)

    assert get_character_table_locator(page).inner_html()


def test_get_character_listing(page: Page, mock_musical_id: int):
    page = goto_musical_page(page, musical_id=mock_musical_id)
    normalized_musical_name = get_normalized_musical_name(page)

    page = goto_characters_page(page, musical_id=mock_musical_id, musical_name=normalized_musical_name)
    for character in get_character_listing(page).all():
        print(character.locator('a[href]'))

    assert get_character_listing(page).all_inner_texts() == ""
