import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#########################################
#########################################
# Graphing code

def make_genres_graph(year=None):
    fig, ax = plt.subplots()
    filtered_df =  df[df["year"] == year] if year else df
    genre_df = filtered_df.groupby("genres")["user_id"].count().sort_values(ascending=False).to_frame("count")
    sns.barplot(
        data=genre_df, 
        x="count", 
        y=genre_df.index, 
        orient="h",
        ax=ax
    )
    ax.set_title(f"Quantity of Movie Ratings per Genre{f" in {year}" if year else ""}")
    ax.set_xlabel("Count") 
    ax.set_ylabel("Genre")
    return fig, ax

def make_best_genres_graph(year):
    filtered_df =  df[df["year"] == year] if year else df
    top_genres_df = filtered_df.groupby("genres")["rating"].mean().nlargest(5)
    fig, ax = plt.subplots()

    sns.barplot(
        data=top_genres_df, 
        orient="h", 
        palette=sns.color_palette(),
        ax=ax
    )

    ax.set_title(f"Highest-Rated Movie Genres{f" in {year}" if year else ""}")
    ax.set_xlabel("Rating (0-5)")
    ax.set_ylabel("Genre")

    plt.xlim(3)
    ax.set_xticks(range(3, 5))
    for bar in ax.containers:
        ax.bar_label(bar, fmt=" %.1f")
    return fig, ax

def make_ratings_graph(genre=None):
    fig, ax = plt.subplots()
    filtered_df =  df[df["genres"] == genre] if genre else df
    year_df = filtered_df.groupby("year")["rating"].mean()

    sns.lineplot(data=year_df, ax=ax)

    ax.set_title(f"Average Movie Rating{f" for {genre} " if genre else ""} per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rating (0-5)")
    ax.set_yticks(range(2, 6))

    return fig, ax

def get_top_movies(minimum_rating_count=50, count=5):
    minimum_rated_movies = df.value_counts("title")[df.value_counts("title") >= minimum_rating_count].index
    top_movies = df[df["title"].isin(minimum_rated_movies)].groupby("title")["rating"].mean().nlargest(count).to_frame("average_rating")
    return top_movies

#########################################
#########################################

st.set_page_config(
    page_title="Movie Ratings Data",
    page_icon="🧐",
    layout="wide"
)

st.title("Movie Ratings Data")

df = pd.read_csv("Week-03-EDA-and-Dashboards/exercise/ayesha_ilyas_dashboard/data/cleaned_movie_ratings.csv") 

columns = st.columns(spec=[.5, .5], gap="medium")

with columns[0]:

    st.header("Top Rated Movies")

    # select minimum rating count
    # number of top results to display

    minimum_ratings = [50, 150, 500, 100]
    rating_selection = st.segmented_control(
        "Minimum rating count:",
        minimum_ratings,
        selection_mode="single",
        default=minimum_ratings[0]
    )

    result_count = [3, 5, 10, 15]
    result_count_selection = st.segmented_control(
        "Number of results to display:",
        result_count,
        selection_mode="single",
        default=result_count[2]
    )

    st.markdown(f"The top `{result_count_selection}` movies that have at least `{rating_selection}` ratings.")

    top_movies_df = get_top_movies(rating_selection, result_count_selection)
    st.dataframe(top_movies_df, column_config={
        "title": "Title",
        "average_rating": st.column_config.NumberColumn("Average Rating", format="%.1f")
    })
    

with columns[1]:
    st.header("Overall Data")

    tab1, tab2, tab3 = st.tabs(["Average rating by year", "Genre breakdown", "Highest rated genres"])
    genre_options = sorted(df["genres"].unique())
    year_options = sorted(df["year"].unique())

    with tab1:
        genre_selection = st.selectbox("Genre", genre_options, index=None, placeholder="Show data for all genres")
        fig1, _ = make_ratings_graph(genre_selection)
        st.pyplot(fig1)
    with tab2:
        year_selection1 = st.selectbox("Year", year_options, index=None, placeholder="Show data across all years", key="tab2")
        fig2, _ = make_genres_graph(year_selection1)
        st.pyplot(fig2)
    with tab3:
        year_selection2 = st.selectbox("Year", year_options, index=None, placeholder="Show data across all years", key="tab3")
        fig3, _ = make_best_genres_graph(year_selection2)
        st.pyplot(fig3)


