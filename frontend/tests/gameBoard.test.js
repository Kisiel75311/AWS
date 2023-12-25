const {test, expect} = require('@playwright/test');

test.describe('GameBoard Component Tests', () => {
    test.beforeEach(async ({page}) => {
        await page.goto('http://10.0.1.2:8080/'); // Adres URL Twojego projektu Vue.js
    });

    test('Should display initial game state', async ({page}) => {
        await expect(page.locator('h1')).toContainText(''); // Początkowy stan wiadomości
        await expect(page.locator('h2')).toContainText('Aktualny gracz: '); // Początkowy stan aktualnego gracza
        const cells = page.locator('.cell');
        await expect(cells).toHaveCount(9); // Sprawdź, czy są 3x3 komórki
    });

    test('Should start new game on button click', async ({page}) => {
        await page.click('button:has-text("Start New Game")');
        await expect(page.locator('h2')).toContainText('Aktualny gracz: X'); // Załóżmy, że X zaczyna grę
    });

    test('Should make a move and update the board', async ({page}) => {
        await page.click('button:has-text("Start New Game")');
        // Click on the first cell in the top row
        const firstCell = page.locator('.cell').nth(0);
        await firstCell.click();
        // Po kliknięciu sprawdź, czy komórka jest zablokowana (disabled) i zawiera 'X'
        await expect(firstCell).toHaveAttribute('disabled');
        await expect(firstCell).toContainText('X');
    });


    test('Should reset the game', async ({page}) => {
        await page.click('button:has-text("Start New Game")');
        await page.click('.cell:has-text("")');
        await page.click('button:has-text("Reset Game")');
        // Sprawdź, czy wszystkie komórki są puste po resecie
        const cells = page.locator('.cell');
        for (let i = 0; i < 9; i++) {
            await expect(cells.nth(i)).toContainText('');
        }
    });

});
