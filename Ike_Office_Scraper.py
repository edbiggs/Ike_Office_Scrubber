import ScraperTools as tools
import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────── Debug Mode ────────────────

debug_mode = False
debug_xpath = "//div[contains(@id,'spanLength')]//span"

# ──────────────── Config ────────────────
job_name ="polecat creek - caroline pines"

username = os.getenv("IKE_USERNAME")
password = os.getenv("IKE_PASSWORD")

data_extraction = False

calculate_final_sag = True

reel_id_insertion = True
reel_id_file = "Ike_Office_Scrubber/PCC_CAP_ReelIDs.csv"
# ────────────────────── Main Script ─────────────────────────


def main():

    print("START")

    scraper = tools.ScraperTools()

    scraper.get_url()

    scraper.login(username, password)

    scraper.get_project(job_name)


    if reel_id_insertion == True:
        scraper.create_reel_id_map(reel_id_file)
        scraper.insert_reel_id()

    else:
        for pole_id in scraper.get_pole_id_list():
            scraper.get_next_pole(pole_id)

            if debug_mode == True:
                scraper.debug(debug_xpath)
                break

            elif data_extraction == True:
                missing_data, found_data = scraper.get_pole_data(pole_id)
                scraper.export_missing_fields(job_name)

                if calculate_final_sag == True:
                    scraper.export_final_sag(job_name)

    print("FINISH")
    scraper.driver.quit()

main()
