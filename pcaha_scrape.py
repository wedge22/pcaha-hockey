from selenium import webdriver
import csv

# Define Global Variables
url = "https://games.pcaha.ca/teams/4326"
csv_file = "game_schedule.csv"
games = []

""" 
Define CSV Columns. You can re-order these to your liking, just make sure the header matches the dictionary value,
in the get_schedule() function. Order of this list determines write order in the CSV file.
"""
csv_columns = ['date', 'number', 'league', 'flight', 'game_time', 'arena', 'notes', 'home_team', 'home_score',
               'away_team', 'away_score']


def clean_output(value):
    """
    Cleans webscraped content by replacing html formatting in CSV format,
    and removes the stupid middle dot.
    :param value: Response object from get_schedule()
    :return clean_value: string
    """
    clean_value = str(value).replace(u"\u0020\u00b7\u0020", "-").replace(r'\n', ';')

    return clean_value


def get_schedule():
    """
    Establishes connection and queries website.
    :return: Null
    """
    # create a new Firefox session
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)

    # After opening the url above, Selenium finds the table with the schedule
    table = driver.find_element_by_xpath("//table[@class='table']")

    # Iterate through the table rows and identify the table data properties
    # Run clean_output to remove html entities
    for row in table.find_elements_by_xpath(".//tr"):
        details = clean_output([td.text for td in row.find_elements_by_xpath(".//td[1]")])
        matchup = clean_output([td.text for td in row.find_elements_by_xpath(".//td[2]")])

        # Format output into array by removing unnecessary characters
        # and splitting into components
        game_details = details.lstrip("['").rstrip("']").split(';')
        matchup = matchup.lstrip("['").rstrip("']").split(';')

        # Determine if the array has additional notes about the game
        # If notes aren't found, create empty string to prevent Index error
        if len(game_details) < 4:
            game_details.append('')

        # Assign variables to data
        number = game_details[0].split("-")[0]
        date = game_details[0].split("-")[1]
        league = game_details[0].split("-")[2]
        flight = game_details[0].split("-")[3]
        game_time = game_details[1]
        arena = game_details[2]
        notes = game_details[3]
        home_team = matchup[0]
        home_score = matchup[1]
        away_team = matchup[4]
        away_score = matchup[3]

        # Add data to dictionary
        games.append(
            {'date': date,
             'number': number,
             'league': league,
             'flight': flight,
             'game_time': game_time,
             'arena': arena,
             'notes': notes,
             'home_team': home_team,
             'home_score': home_score,
             'away_team': away_team,
             'away_score': away_score}
        )

    # Close connection to website
    driver.quit()


def write_csv():
    """
    Writes data in dictionary to a CSV file based on CSV Header and dictionaries Key/Value Pair.
    :return Null:
    """
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in games:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def main():
    get_schedule()
    write_csv()
    exit()


if __name__ == "__main__":
    main()
