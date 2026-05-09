import time
import ScraperTools


# ──────────────── Debug Mode ────────────────

debug_mode = False

# ────────────────────── Main Script ─────────────────────────


def main():

    print("START")

    scraper = ScraperTools.ScraperTools()

    scraper.get_url()

    scraper.login()

    scraper.get_project()

    missing_data = {}

    for pole_id in scraper.get_pole_id_list():

        scraper.get_next_pole(pole_id)

        if debug_mode == True:
            scraper.debug(pole_id)
        else:
            missing_fields, page = scraper.check_missing_fields(pole_id)

            if missing_fields:
                missing_data[pole_id] = missing_fields

    if missing_data:
        scraper.generate_missing_fields_report(missing_data)

    print("FINISH")
    scraper.driver.quit()


main()
