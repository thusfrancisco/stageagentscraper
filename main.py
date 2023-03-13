from src.scraper import *
import pandas as pd
import time
import traceback
import os

"""
0. Create 3 data structures:
- Musicals.
- Characters.

1. Get all musical names

2. For each musical name, get the list of characters

3. Add 2 columns to df Musicals:
- Number of male characters.
- Number of female characters.

"""


def test_scrape(page: Page):
    list_of_shows = list()
    columns = ["id", "name", "number_of_characters", "number_of_male_characters", "number_of_female_characters"]
    
    with open("data/shows.csv", "a") as f:
        f.write(",".join(columns))
        f.close()

    for show_id in range(2149, 15000):
        goto_show_page(page, show_id=show_id)

        try:
            normalized_show_name = get_normalized_show_name(page)
            
            time.sleep(2)
            if normalized_show_name == "":
                print(f"No show exists with ID {show_id}.")
                continue
            print(show_id, normalized_show_name)

            page = goto_characters_page(page, show_id=show_id, show_name=normalized_show_name)
            character_list = get_character_listing_list(page)

            number_of_characters = len(character_list)
            number_of_male_characters = 0
            number_of_female_characters = 0
            
            for character in character_list:
                if "Male" in character.inner_html():
                    number_of_male_characters += 1
                elif "Female" in character.inner_html():
                    number_of_female_characters += 1

            record = [show_id, normalized_show_name, number_of_characters, number_of_male_characters, number_of_female_characters]
            print(record)

            with open("data/shows.csv", "a") as f:
                f.write("\n" + ",".join(str(x) for x in record))
                f.close()

            list_of_shows.append(record)
            time.sleep(9)

        except Exception as e:
            with open("error_logs.txt", "a") as f:
                f.write(traceback.format_exc())
                f.close()

    shows = pd.DataFrame(data=list_of_shows, columns=columns)

    shows.to_csv("data/shows.csv", index=False)


def test_filter_shows():
    shows = pd.read_csv("data/shows_0.csv")
    shows = shows.loc[(shows["number_of_male_characters"] <= 9) & (shows["number_of_female_characters"] >= 6)]
    if os.path.exists("data/filtered_shows.csv"):
        shows.to_csv("data/filtered_shows.csv", index=False, mode="a", header=False)
    else:
        shows.to_csv("data/filtered_shows.csv", index=False)
