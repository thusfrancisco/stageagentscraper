from playwright.sync_api import Page, Locator


def goto_musical_page(page: Page, musical_id: int) -> Page:    
    page.goto(f"https://www.stageagent.com/shows/{musical_id}/")
    return page


def get_musical_name(page: Page) -> str:
    """
    For a page title such as "Wicked (Musical) Plot & Characters | StageAgent"
    get the first half before " (Musical) ".
    """
    return page.title().split(" (Musical) ")[0]


def get_normalized_musical_name(page: Page) -> str:
    """
    Musical names such as "Les Misérable" have unique characters (accents, whitespace, etc).
    Instead of coming up with a normalization process, we're using the excerpt from the URL that stageagent.com already uses.
    """
    return page.url.split("/")[-1]


def goto_characters_page(page: Page, musical_id: int, musical_name: str) -> Page:
    page.goto(f"https://www.stageagent.com/shows/musical/{musical_id}/{musical_name}/characters")
    return page


def get_character_table_locator(page: Page) -> Locator:
    return page.locator('div[id="characters"]')


def get_character_listing(page: Page) -> Locator:
    return page.locator('div.character-listing')


def get_inner_href_from_locator(page: Page) -> Locator:
    return page.locator('div.character-listing').locator('a[href]')
