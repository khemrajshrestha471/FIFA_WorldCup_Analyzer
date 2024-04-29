import streamlit as st
import pandas as pd
import helper, summarizer

df = pd.read_csv('FIFA-World-Cup-1930-2022-All-Match-Dataset.csv', encoding='ISO-8859-1')

st.sidebar.title("FIFA WorldCup Analyzer")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Home', 'Graph Visualization', 'Overall Analysis')
)

if (user_menu == 'Home'):
    st.title("Welcome to FIFA WorldCup Analyzer")
    match_year = helper.list_of_match_years(df)

    match_year.insert(0, "Pick a Year")

    selected_year = st.selectbox("Select Year", match_year)

    match_held_country, match_names, winner_country = helper.get_country_name_by_year(df, selected_year)


    match_names.insert(0, "Pick Match")

    countries_took_part, max_played, max_count, min_played, min_count = helper.extract_countries_list(df, selected_year)

    if(selected_year != "Pick a Year" and selected_year != " "):
        st.title("History of FIFA WorldCup of the year " + selected_year)
        st1 = "FIFA WorldCup " + selected_year + " was held in " + match_held_country + ". "
        st.write(st1)
        st2 = "The winner of FIFA WorldCup " + selected_year + " was " + winner_country + ". "
        st.write(st2)

        st3 = "The List of countries that took part in world cup " + selected_year + " were " + str(countries_took_part) + ". "
        st.write(st3)
        st4 = "The Country that played for the maximun number of times on " + selected_year + " world cup was " + str(max_played) + " and the total times was " + str(max_count) + ". "
        st.write(st4)
        st5 = "The Country that played for the minimum number of times on " + selected_year + " was " + str(min_played) + " and the total times was " + str(min_count) + ". "
        st.write(st5)

        countries_took_part.insert(0, "Pick Country")
        country_total_match_played = st.selectbox("Pick country to see number of matches played", countries_took_part)

        country_played_match, each_country_played_number = helper.calculate_games_played(df, selected_year, country_total_match_played)

        # st.write(each_country_played_number)

        formatted_strings = []

        for country, matches in each_country_played_number.items():
            formatted_string = f"{country} played {matches} match" if matches == 1 else f"{country} played {matches} matches"
            formatted_strings.append(formatted_string)

        result_country_match_played = ", ".join(formatted_strings)




        if(country_total_match_played != "Pick Country" and country_total_match_played != ""):
            st6 = str(country_total_match_played) + " played total of " + str(country_played_match) + " matches on " + selected_year + " World Cup. "
            st.write(st6)

            selected_match = st.selectbox("", match_names)

            if (selected_match != "Pick Match" and selected_match != ""):

                city_name, stadium_name, match_date, score, home_team, away_team, home_team_score, away_team_score, penalties_score, home_team_penalty_score, away_team_penalty_score, stage_name = helper.return_city_name(df, match_held_country, selected_match)

                st7 = "This was the " + stage_name + " game. "
                st.write(st7)

                st8 = "The match of " + selected_match + " was held in the city " + city_name + ". "
                st.write(st8)

                st9 = "The name of stadium was " + stadium_name + ". "
                st.write(st9)

                st10 = "The date of this match held was " + match_date + ". "
                st.write(st10)

                st11 = "The Score was " + str(score) + ", that means " + home_team + " scored " + str(home_team_score) + " and " + away_team + " scored " + str(away_team_score) + ". "
                st.write(st11)

                if(home_team_score == away_team_score):
                    st12 = "The match was draw and penalty was taken and the score of penalty was " + penalties_score + ", that means " + home_team + " scored " + str(home_team_penalty_score) + " and " + away_team + " scored " + str(away_team_penalty_score) + ". "
                    st.write(st12)

                    if(home_team_penalty_score > away_team_penalty_score):
                        st13 = home_team + " won the match. "
                        st.write(st13)
                        text_to_be_summarized = st1 + st2 + st3 + st4 + st5 + st6 + st7 + st8 + st9 + st10 + st11 + st12 + st13 + result_country_match_played
                    else:
                        st14 = away_team + " won the match. "
                        st.write(st14)
                        text_to_be_summarized = st1 + st2 + st3 + st4 + st5 + st6 + st7 + st8 + st9 + st10 + st11 + st12 + st14 + result_country_match_played
                else:
                    if(home_team_score > away_team_score):
                        st15 = home_team + " won the match. "
                        st.write(st15)
                        text_to_be_summarized = st1 + st2 + st3 + st4 + st5 + st6 + st7 + st8 + st9 + st10 + st11 + st15 + result_country_match_played
                    else:
                        st16 = away_team + " won the match. "
                        st.write(st16)
                        text_to_be_summarized = st1 + st2 + st3 + st4 + st5 + st6 + st7 + st8 + st9 + st10 + st11 + st16 + result_country_match_played
                
                prompt_qst = """ Based on this, answer the question """
                question_area = st.text_area("Ask the Question Here", height=30)
                submit_button = st.button("Submit")
                if(submit_button and question_area):
                    answer_text = summarizer.generate_gemini_answer(text_to_be_summarized, prompt_qst, question_area)
                    st.write(answer_text)

                summarize = st.button("Summarize the History")

                if(summarize):
                    prompt = """ Generate detailed summary based on this paragraph in either single or multiple paragraph """
                    
                    summarized_text = summarizer.generate_gemini_content(text_to_be_summarized, prompt)
                    if (summarized_text):
                        st.subheader("Summary of FIFA WorldCup " + selected_year + " between " + home_team + " Vs " + away_team + "!") 
                        st.write(summarized_text)
                







if(user_menu == 'Graph Visualization'):
    st.title("FIFA WorldCup Graph Visualization")
    st.write("Choose two year for line graph visualization")
