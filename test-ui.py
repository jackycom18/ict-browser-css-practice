from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    """功能：验证 1.5 页面的四项精准 CSS 调整、菜单交互与零外部资源。输入：无。输出：无，失败时抛出断言。"""
    external_requests: list[str] = []
    page_errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.on(
            "request",
            lambda request: external_requests.append(request.url)
            if not request.url.startswith("http://127.0.0.1:8110")
            else None,
        )
        page.goto("http://127.0.0.1:8110", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(500)

        assert page.title() == "Paw & Co. — 为生活找一个伙伴"
        primary_button = page.locator(".hero .btn-primary").first
        assert "rgb(229, 72, 63)" in primary_button.evaluate(
            "element => getComputedStyle(element).backgroundColor"
        )

        search = page.locator(".search__input")
        search.focus()
        assert "rgb(229, 72, 63)" in search.evaluate(
            "element => getComputedStyle(element).borderColor"
        )

        card = page.locator(".card").first
        card.hover()
        page.wait_for_timeout(220)
        card_style = card.evaluate(
            "element => ({ shadow: getComputedStyle(element).boxShadow, transform: getComputedStyle(element).transform })"
        )
        assert card_style["shadow"] != "none"
        assert card_style["transform"] != "none"

        care_item = page.locator(".care__item").first
        assert "rgb(229, 72, 63)" in care_item.evaluate(
            "element => getComputedStyle(element).borderLeftColor"
        )

        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("#menuToggle").click()
        assert page.locator(".global-nav__links").evaluate(
            "element => element.classList.contains('is-open')"
        )
        assert page.locator("#menuToggle").get_attribute("aria-expanded") == "true"
        page.locator("#menuToggle").click()
        assert page.locator("#menuToggle").get_attribute("aria-expanded") == "false"

        assert not external_requests, "external requests: " + ", ".join(external_requests)
        assert not page_errors, "page errors: " + "; ".join(page_errors)

        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#top").scroll_into_view_if_needed()
        page.screenshot(path=str(screenshot_dir / "desktop.png"))
        browser.close()


if __name__ == "__main__":
    main()
