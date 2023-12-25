import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Use 'headless=True' for headless mode
        yield browser
        browser.close()


def test_game_flow(browser):
    page = browser.new_page()
    page.goto('http://localhost:8080/')  # Adjust the URL to your Vue.js app

    # Start a new game
    page.click('text=Start New Game')

    # Make moves to lead X to win
    winning_moves = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
    for row, col in winning_moves:
        page.click(f'button:has-text(""):nth-of-type({row * 3 + col + 1})')

    # Verify X won
    assert "X" in page.inner_text('h1')

    # Reset the game
    page.click('text=Reset Game')

    # Verify the game is reset
    assert "New game started." in page.inner_text('h1')

    page.close()


def test_multiple_independent_games(browser):
    page = browser.new_page()
    page.goto('http://localhost:8080/')  # Adjust the URL to your Vue.js app

    # Start Game 1 and make moves
    page.click('text=Start New Game')
    page.click('button:has-text(""):nth-of-type(1)')
    page.click('button:has-text(""):nth-of-type(5)')

    # Start Game 2 and make different moves
    page.click('text=Start New Game')
    page.click('button:has-text(""):nth-of-type(9)')
    page.click('button:has-text(""):nth-of-type(2)')

    # Add assertions as needed to verify the state of both games

    page.close()

# Add definitions for other tests here
