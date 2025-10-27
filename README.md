# Video Games & Player Engagement Analysis

## Project Overview

This project analyzes video game data to explore relationships between game ratings, community engagement (number of ratings), Metacritic scores, playtime, genres, platforms, and release dates. Data was collected from the RAWG API and Wikipedia, cleaned, merged, and analyzed using Python libraries (Pandas, Matplotlib, Seaborn).

## Data Sources

* **RAWG Video Games Database API:** Provided primary metadata for 40 highly-rated games released between 2020-2024 (name, rating, ratings\_count, released, metacritic, genres, playtime, platforms).
    * *Endpoint:* `https://api.rawg.io/api/games`
* **Wikipedia:** The "List of best-selling video games" page was scraped using BeautifulSoup to gather sales figures, developer names, and release years for top-selling titles.
    * *URL:* `https://en.wikipedia.org/wiki/List_of_best-selling_video_games`

## Process

1.  **Data Collection:** Fetched data from the RAWG API (top 40 rated, 2020-2024) and scraped the top 40 entries from the Wikipedia table.
2.  **Data Cleaning:**
    * Handled missing values (imputed median for `metacritic`, 0 for `playtime`).
    * Parsed dates and extracted release years.
    * Converted scraped `sales_millions` and `release_year` to numeric types.
    * Removed duplicates.
3.  **Data Merging:**
    * Attempted an inner join on normalized game names.
    * Due to limited matches (<10), the analysis primarily used the cleaned API dataset.
    * A *synthetic* `sales_millions` column (based on `ratings_count`) was created for visualization purposes.
4.  **Analysis & Visualization:** Conducted EDA and generated plots including:
    * Rating distribution histogram.
    * Rating vs. Ratings Count scatter plot.
    * Correlation heatmap.
    * Top 10 rated games bar chart.
    * Game releases over time line chart.
    * Platform/Genre treemaps and sunburst charts.
    * Scatter/Box plots for ratings by platform/genre/sales.

## Key Findings

* The analyzed sample (biased towards recent, high ratings) shows an average rating of 4.63.
* A very weak positive correlation (0.072) exists between RAWG rating and the number of ratings (`ratings_count`) in this dataset.
* A weak positive correlation (0.275) was found between RAWG rating and Metacritic score.
* Adventure (18) and Action (17) are the most frequent genres in the sample.
* PC is the most common platform.
* The highest-rated game in the dataset is "Winter Memories" (Rating 4.83, 6 ratings).

## Visualizations Generated

* Distribution of Game Ratings & Rating vs Community Engagement 
* Top 10 Highest Rated Games 
* Correlation Between Game Metrics 
* Game Releases Over Time 
* Genre Distribution by Platform (Treemap/Sunburst)
* Ratings by Platform/Genre (Scatter/Box plots)

## Limitations

* **Sampling Bias:** API query focused on recent, highly-rated games.
* **Merge Issues:** Name variations hindered joining API and scraped sales data accurately. Synthetic sales data was used as a proxy.
* **Low Engagement:** Some top-rated games have very few ratings, limiting conclusions about popularity vs. rating.
* **Data Cleaning Approximations:** Median imputation for Metacritic and setting missing playtime to 0.

## Future Work

* Improve data merging using fuzzy matching or external IDs.
* Expand data collection via API pagination for a larger sample.
* Incorporate more robust sales or engagement metrics (e.g., Steam player counts).
* Perform more granular analysis within specific genres/platforms.
* Analyze playtime data more thoroughly.

## Files

* `videogames.ipynb`: Jupyter notebook containing the analysis code.
* `api_games.csv`: Cleaned data extracted from the RAWG API.
* `scraped_games.csv`: Cleaned data scraped from Wikipedia.
* `visualization_*.png`: Saved static visualization files.
