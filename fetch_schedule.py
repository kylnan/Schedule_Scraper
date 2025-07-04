import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
import os

LOGIN_URL = "https://moms.cvnacorp.com/location/373/resources"
JSON_OUTPUT_PATH = os.path.join(os.getcwd(), "carvana_schedule.json")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🌐 Navigating to login page...")
        await page.goto(LOGIN_URL)

        print("🔐 Please log in manually.")
        await page.wait_for_selector("div.EmployeeFilter__Container-sc-1ydutyf-0.kBQJJN", timeout=180000)
        print("✅ Logged in and schedule panel loaded.")

        print("📋 Scraping schedule data...")
        events = await page.evaluate("""
            () => {
                const rows = document.querySelectorAll('[data-testid="EmployeeScheduleRow"]');
                const output = [];
                rows.forEach(row => {
                    const name = row.querySelector("h3")?.innerText;
                    const shifts = Array.from(row.querySelectorAll('[data-testid^="EmployeeShift"]')).map(shift => {
                        return {
                            date: shift.getAttribute("data-testid").split("-")[1],
                            time: shift.innerText
                        };
                    });
                    output.push({ name, shifts });
                });
                return output;
            }
        """)

        with open(JSON_OUTPUT_PATH, "w") as f:
            json.dump(events, f, indent=2)

        print(f"💾 Schedule saved to {JSON_OUTPUT_PATH}")
        await browser.close()

asyncio.run(run())
