from playwright.sync_api import sync_playwright

def scrape_euronews(**context):
    base_url = "https://www.euronews.com/news/asia?page="
    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
        })

        for num in range(1, 6):
            url = base_url + str(num)
            print(f"Parsing page {num}: {url}")
            
            page.goto(url, timeout=120000)
            page.wait_for_load_state("networkidle")

            articles = page.query_selector_all("article")

            for art in articles:
                title_el = art.query_selector("h3.the-media-object__title")
                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                link_el = art.query_selector("a.the-media-object__link")
                link = "https://www.euronews.com" + link_el.get_attribute("href") if link_el else None
                desc_el = art.query_selector(".the-media-object__description")
                description = desc_el.inner_text().strip() if desc_el else None
                date_el = art.query_selector("div.the-media-object__date")
                date = date_el.inner_text().strip() if date_el else None
                all_results.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "date": date
                })

        browser.close()
    with open("/opt/airflow/data/euronews_data.json", "w", encoding="utf-8") as f:
        import json
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    context['ti'].xcom_push(key='euronews_data', value=all_results)
    print(f"Scraped {len(all_results)} articles in total.")
    return all_results
