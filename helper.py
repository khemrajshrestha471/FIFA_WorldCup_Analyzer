import numpy as np


def list_of_match_years(df):
    # Initialize an empty set to store unique years
    unique_years = set()

    # Initialize an empty list to store the extracted unique years
    match_year = []

    # Iterate over each element in the 'tournament Name' column
    for name in df['tournament Name']:
        # Split the string by whitespace and retrieve the first element (index 0)
        year = name.split()[0]
        
        # Check if the year is not already in the set
        if year not in unique_years:
            # Append the unique year to the match_year list
            match_year.append(year)
            
            # Add the year to the set of unique years
            unique_years.add(year)
    
    return match_year


def get_country_name_by_year(df, year):
    country_name = None
    match_name_list = []
    winner_country = None
    
    filtered = df[df['tournament Name'].str.split().str[0] == year]
    
    if len(filtered) > 0:
        country_name = filtered['Country Name'].values[0]
        match_name_list = filtered['Match Name'].tolist()
        winner_country = filtered['Winner'].values[0]
    
    return country_name, match_name_list, winner_country


def return_city_name(df, country, match):
    filtered = df[(df['Country Name'] == country) & (df['Match Name'] == match)]
    if len(filtered) > 0:
        return filtered['City Name'].values[0], filtered['Stadium Name'].values[0], filtered['Match Date'].values[0], filtered['Score'].values[0], filtered['Home Team Name'].values[0], filtered['Away Team Name'].values[0], filtered['Home Team Score'].values[0], filtered['Away Team Score'].values[0], filtered['Score Penalties'].values[0], filtered['Home Team Score Penalties'].values[0], filtered['Away Team Score Penalties'].values[0], filtered['Stage Name'].values[0]


def extract_countries_list(df, year):
    # Initialize a list to store country names
    country_list = []

    # Initialize a dictionary to store the count of each country
    country_counts = {}

    # Filter the DataFrame by the provided year
    df_filtered = df[df['tournament Name'].str.split().str[0] == year]

    # Iterate through the 'Match Country' column of the filtered DataFrame
    for match_country in df_filtered['Match Name']:
        # Split the string based on the 'v' character
        countries = match_country.split(' v ')
        # Iterate through the split countries
        for country in countries:
            # Add the country name to the list if it's not already present
            if country not in country_list:
                country_list.append(country)
            # Increment the count of the country in the dictionary
            country_counts[country] = country_counts.get(country, 0) + 1

    # Sort the country list in ascending order
    country_list.sort()

    # Find the country that appears the maximum and minimum times
    max_country = None
    min_country = None
    max_count = 0
    min_count = float('inf')
    for country, count in country_counts.items():
        if count > max_count:
            max_country = country
            max_count = count
        if count < min_count:
            min_country = country
            min_count = count

    return country_list, max_country, max_count, min_country, min_count




def calculate_games_played(df, year, country):
    # Initialize a count to store the number of games played by the country
    games_played = 0
    # Initialize a dictionary to store the count of matches played by each country
    matches_played_by_country = {}

    # Filter the DataFrame by the provided year
    df_filtered = df[df['tournament Name'].str.split().str[0] == year]

    # Iterate through the 'Match Country' column of the filtered DataFrame
    for match_country in df_filtered['Match Name']:
        # Split the string based on the 'v' character
        countries = match_country.split(' v ')
        # Increment the count of matches played by each country in the match
        for country_in_match in countries:
            if country_in_match in matches_played_by_country:
                matches_played_by_country[country_in_match] += 1
            else:
                matches_played_by_country[country_in_match] = 1
        # Check if the provided country is in the list of countries for this match
        if country in countries:
            # Increment the count of games played by the country
            games_played += 1

    return games_played, matches_played_by_country


def total_country_name(df):
    unique_country_set = set()
    for match_country in df['Match Name']:
        countries = match_country.split(' v ')
        unique_country_set = unique_country_set.union(set(countries))
    return sorted(list(unique_country_set))


def calculate_games_played_each_year(df, year, country):
    # Initialize a count to store the number of games played by the country
    games_played = 0

    # Filter the DataFrame by the provided year
    df_filtered = df[df['tournament Name'].str.split().str[0] == year]

    # Iterate through the 'Match Country' column of the filtered DataFrame
    for match_country in df_filtered['Match Name']:
        # Split the string based on the 'v' character
        countries = match_country.split(' v ')
        # Check if the provided country is in the list of countries for this match
        if country in countries:
            # Increment the count of games played by the country
            games_played += 1

    return games_played


def calculate_final_reach(df, year, country):
    final_participation = 0

    df_filtered = df[df['tournament Name'].str.split().str[0] == year]

    for index, row in df_filtered.iterrows():
        if row['Stage Name'] == 'final':
            countries = row['Match Name'].split(' v ')
            if country in countries:
                final_participation = 1

    return final_participation


def list_country_played_with_frequency(df, year):
    # Initialize a dictionary to store the count of games played by each country
    games_played_by_country = {}

    # Filter the DataFrame by the provided year
    df_filtered = df[df['tournament Name'].str.split().str[0] == year]

    # Iterate through the 'Match Name' column of the filtered DataFrame
    for match_country in df_filtered['Match Name']:
        # Split the string based on the ' v ' character
        countries = match_country.split(' v ')
        # Iterate through each country in the match
        for country in countries:
            # Check if the country is already in the dictionary, if not, add it
            if country not in games_played_by_country:
                games_played_by_country[country] = 1
            else:
                # Increment the count of games played by the country
                games_played_by_country[country] += 1

    # Convert the dictionary to a list of tuples
    games_played_list = list(games_played_by_country.items())
    
    # Sort the list based on the number of games played (second element of the tuple) and country name
    sorted_games_played_list = sorted(games_played_list, key=lambda x: (x[1], x[0]), reverse=True)

    # Return the sorted list
    return sorted_games_played_list