import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("dark_background")
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Dashboard")
st.markdown("### Explore Netflix content trends interactively")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")

    # Clean date column
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())
type_filter = st.sidebar.selectbox("Select Type", type_options)

country_list = sorted(df["country"].dropna().unique().tolist())
country_options = ["All"] + country_list
country_filter = st.sidebar.selectbox("Select Country", country_options)

rating_options = ["All"] + sorted(df["rating"].dropna().unique().tolist())
rating_filter = st.sidebar.selectbox("Select Rating", rating_options)

# Apply filters
df_filtered = df.copy()

if type_filter != "All":
    df_filtered = df_filtered[df_filtered["type"] == type_filter]

if country_filter != "All":
    df_filtered = df_filtered[df_filtered["country"] == country_filter]

if rating_filter != "All":
    df_filtered = df_filtered[df_filtered["rating"] == rating_filter]

# KPI cards
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(df_filtered))
col2.metric("Movies", (df_filtered["type"] == "Movie").sum())
col3.metric("TV Shows", (df_filtered["type"] == "TV Show").sum())

# Show filtered data
st.subheader("Filtered Data Preview")
st.dataframe(df_filtered.head(10), use_container_width=True)

# Layout for charts
col_left, col_right = st.columns(2)

# Plot 1: Content added over time
with col_left:
    st.subheader("Content Added Over Time")

    year_counts = df_filtered["year_added"].dropna().value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    if not year_counts.empty:
        ax.set_facecolor("#0E1117")       
        fig.patch.set_facecolor("#0E1117")
        year_counts.plot(kind="line", marker="o", ax=ax)
        ax.set_xlabel("Year Added")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
    ax.set_title("Titles Added by Year")
    st.pyplot(fig)

# Plot 2: Top genres
with col_right:
    st.subheader("Top Genres")

    df_genre = df_filtered.copy()
    df_genre["listed_in"] = df_genre["listed_in"].str.split(", ")
    df_genre = df_genre.explode("listed_in").reset_index(drop=True)
    df_genre["listed_in"] = df_genre["listed_in"].str.strip()

    top_genres = df_genre["listed_in"].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    if not top_genres.empty:
        ax2.set_facecolor("#0E1117")        
        fig2.patch.set_facecolor("#0E1117")
        sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax2)
        ax2.set_xlabel("Count")
        ax2.set_ylabel("Genre")
    ax2.set_title("Top 10 Genres")
    st.pyplot(fig2)

# Plot 3: Top countries
st.subheader("Top Countries")

top_countries = df_filtered["country"].dropna().value_counts().head(10)

fig3, ax3 = plt.subplots(figsize=(10, 5))
if not top_countries.empty:
    ax3.set_facecolor("#0E1117")
    fig3.patch.set_facecolor("#0E1117")
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax3)
    ax3.set_xlabel("Count")
    ax3.set_ylabel("Country")
ax3.set_title("Top 10 Countries")
st.pyplot(fig3)

# Plot 4: Rating distribution
st.subheader("Content Ratings")

rating_counts = df_filtered["rating"].dropna().value_counts().head(10)

fig4, ax4 = plt.subplots(figsize=(10, 5))
if not rating_counts.empty:
    sns.barplot(x=rating_counts.values, y=rating_counts.index, ax=ax4)
    ax4.set_xlabel("Count")
    ax4.set_ylabel("Rating")
ax4.set_title("Top Content Ratings")
st.pyplot(fig4)

# Footer insight
st.markdown("---")
st.markdown(
    """
    **Dashboard Summary:**  
    This dashboard helps explore Netflix content by type, country, rating, release trends, genres, and regional distribution.
    """
)