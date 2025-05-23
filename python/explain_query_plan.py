import asyncio
import sys
from pyppeteer import launch


# Загружаем HTML страницу с последующей подгрузкой JavaScript
async def fetch_html(url):
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Устанавливаем поддержку русского языка
    await page.setExtraHTTPHeaders({'Accept-Language': 'ru-RU,ru;q=0.9'})
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'language', {get: () => 'ru-RU'});
        Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru']});
    }''')

    await page.goto(url, waitUntil='networkidle0')
    content = await page.content()
    print(content)
    await browser.close()


asyncio.new_event_loop().run_until_complete(fetch_html(sys.argv[1]))
