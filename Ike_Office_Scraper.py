import ScraperTools


# ──────────────── Debug Mode ────────────────

debug_mode = False

debug_field_name = "Reel ID"
debug_xpath = ("//div[@title='Reel ID']"
               "/following-sibling::div[contains(@class, 'c-CollectionField__Value')]"
               "//textarea")
debug_data_type = "value"

# ────────────────────── Main Script ─────────────────────────


def main():

    print("START")

    scraper = ScraperTools.ScraperTools()

    scraper.get_url()

    scraper.login()

    scraper.get_project()

    output = {}

    for pole_id in scraper.get_pole_id_list():

        scraper.get_next_pole(pole_id)

        if debug_mode == True:
            try:
                scraper.debug(debug_field_name, debug_xpath,
                              debug_data_type, pole_id)
            except:
                print("Debug configuration error: Check debug variables")
        else:
            pass
            # scraper.get_field_data(pole_id)
            scraper.insert_reel_id(pole_id)

    if output:
        scraper.generate_missing_fields_report(output)

    print("FINISH")
    scraper.driver.quit()


main()
