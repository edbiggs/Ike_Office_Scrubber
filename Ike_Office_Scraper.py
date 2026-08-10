import ScraperTools as st
import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────── Debug Mode ────────────────

debug_mode = False
debug_xpath = "//div[contains(@id,'ipf_spanLength')]//div[contains(@class,'c-Input')]/span"

# ──────────────── Config ────────────────
job_name ="Paytes-Bells Crossroad"

username = os.getenv("IKE_USERNAME")
password = os.getenv("IKE_PASSWORD")

data_extraction = True

calculate_final_sag = True

reel_id_insertion = False
reel_id_file = "Ike_Office_Scrubber/PTS_BCR_ReelIDs.csv"

# ────────────────────── Main Script ─────────────────────────


def main():

    print("START")

    scraper = st.ScraperTools()

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
                scraper.debug(pole_id)
                break
            elif data_extraction == True:
                missing_data, found_data = scraper.get_pole_data(pole_id)
                if calculate_final_sag == True:
                    scraper.calculate_final_sag(pole_id, found_data)



    print("FINISH")
    scraper.driver.quit()


main()
