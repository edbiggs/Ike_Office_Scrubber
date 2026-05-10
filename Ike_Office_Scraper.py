import time
import ScraperTools


# ──────────────── Debug Mode ────────────────

debug_mode = True

debug_field_name = "Pole ID"
debug_xpath = "//div[@title='ID']"
"[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
"/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
"//div[contains(@class,'is-dirty')]"
"//textarea"
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
            missing_fields, page = scraper.check_missing_fields(pole_id)

            if missing_fields:
                output[pole_id] = missing_fields

    if output:
        scraper.generate_missing_fields_report(output)

    print("FINISH")
    scraper.driver.quit()


main()
