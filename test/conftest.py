import pytest
from playwright.sync_api import sync_playwright, Page


@pytest.fixture()
def context_and_page() -> Page:
    with sync_playwright() as playwright:
        print(f"Launching new incognito browser instance")

        browser = playwright.chromium.launch()

        page = browser.new_page()
        
        yield page
        browser.close()


@pytest.fixture()
def page(context_and_page: Page) -> Page:
    context_and_page.goto("https://www.stageagent.com/shows/")
    return context_and_page


@pytest.fixture()
def mock_musical_id() -> int:
    return 1289
