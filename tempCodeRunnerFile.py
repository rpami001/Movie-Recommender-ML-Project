
# dfs = []
# for file in csv_files:
#     df = pd.read_csv(file)
#     dfs.append(df)
# all_movies = pd.concat(dfs)

# movies = all_movies.drop_duplicates(subset=['movie_name'], keep='first')
# movies.to_csv('combined_movies.csv', index=False)