from playwright.sync_api import Page, Locator


def goto_show_page(page: Page, show_id: int) -> Page:    
    page.goto(f"https://www.stageagent.com/shows/{show_id}/")
    return page


def get_musical_name(page: Page) -> str:
    """
    For a page title such as "Wicked (Musical) Plot & Characters | StageAgent"
    get the first half before " (Musical) ".
    """
    return page.title().split(" (Musical) ")[0]


def get_normalized_show_name(page: Page) -> str:
    """
    Show names such as "Les Misérable" have unique characters (accents, whitespace, etc).
    Instead of coming up with a normalization process, we're using the excerpt from the URL that stageagent.com already uses.

    Example: "https://stageagent.com/shows/musical/1289/wicked" -> [..., "wicked"] -> "wicked"
    """
    return page.url.split("/")[-1]


def goto_characters_page(page: Page, show_id: int, show_name: str, category: str = "musical") -> Page:
    page.goto(f"https://www.stageagent.com/shows/{category}/{show_id}/{show_name}/characters")
    return page


def get_character_table_locator(page: Page) -> Locator:
    return page.locator('div[id="characters"]')


def get_character_listing_list(page: Page) -> list:
    return page.locator('div.character-listing').all()


def get_character_url(character_listing: Locator) -> str:
    return "https://www.stageagent.com" + character_listing.locator('div.actor-name>span').inner_html().split("\"")[1]
