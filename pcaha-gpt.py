from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import csv

# Define Global Variables
url_root = "https://games.pcaha.ca/teams/"
team_file = "teams.csv"
csv_file_root = "game_schedule_"
csv_columns = ['date', 'number', 'league', 'flight', 'game_time', 'arena', 'notes', 'home_team', 'home_score', 'away_team', 'away_score']


def clean_output(value):
    """
    Cleans webscraped content by replacing html formatting in CSV format,
    and removes the stupid middle dot.
    :param value: Response object from get_schedule()
    :return clean_value: string
    """
    clean_value = str(value).replace(u"\u0020\u00b7\u0020", "-").replace(r'\n', ';')
    return clean_value


def get_schedule(driver, team_code):
    """
    Establishes connection and queries website.
    :param driver: Selenium WebDriver instance
    :param team_code: Unique team identifier
    :return: List of game dictionaries
    """
    url = url_root + team_code
    driver.get(url)

    games = []
    # Find the table with the schedule
    table = driver.find_element(By.XPATH, "//table[@class='table']")

    for row in table.find_elements(By.XPATH, ".//tr"):
        details = clean_output([td.text for td in row.find_elements(By.XPATH, ".//td[1]")])
        matchup = clean_output([td.text for td in row.find_elements(By.XPATH, ".//td[2]")])

        game_details = details.lstrip("['").rstrip("']").split(';')
        matchup = matchup.lstrip("['").rstrip("']").split(';')

        if len(game_details) < 4:
            game_details.append('')

        number = game_details[0].split("-")[0]
        date = game_details[0].split("-")[1]
        league = game_details[0].split("-")[2]
        flight = game_details[0].split("-")[3]
        game_time = game_details[1]
        arena = game_details[2]
        notes = game_details[3]
        home_team = matchup[0]

        if matchup[1].isnumeric():
            home_score = matchup[1]
            away_score = matchup[3]
            away_team = matchup[4]
        else:
            away_team = matchup[2]
            home_score = '-'
            away_score = '-'

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

    return games


def write_csv(file_name, games):
    """
    Writes data in dictionary to a CSV file based on CSV Header and dictionaries Key/Value Pair.
    :param file_name: Output CSV filename
    :param games: List of game dictionaries
    :return: None
    """
    file_name = str(file_name).replace(" ", "_")
    csv_file = csv_file_root + file_name + ".csv"

    try:
        with open(csv_file, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in games:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def main():
    """
    Main function to iterate through teams and fetch schedules.
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    try:
        with open(team_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    team_name = row[0]
                    team_id = row[1]

                    games = get_schedule(driver, team_id)
                    write_csv(team_name, games)
                    line_count += 1

            print(f'Processed {line_count - 1} teams.')
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
