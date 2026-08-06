import ScraperTools as st
import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────── Debug Mode ────────────────

debug_mode = False



# ──────────────── Config ────────────────
job_name ="Paytes-Bells Crossroad"

username = os.getenv("IKE_USERNAME")
password = os.getenv("IKE_PASSWORD")

data_extraction = True


reel_id_insertion = False
reel_id_file = "Ike_Office_Scrubber\PTS_BCR_ReelIDs.csv"

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

                scraper.get_all_data(pole_id)


            elif data_extraction == True:
                scraper.get_all_data(pole_id)


    print("FINISH")
    scraper.driver.quit()


main()
