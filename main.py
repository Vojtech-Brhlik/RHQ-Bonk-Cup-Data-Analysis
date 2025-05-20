#!/usr/bin/python3.10
# coding=utf-8

#################################################################
#                                                               #
#                                                               #
#                  Data Analysis for RHQ Bonk Cup               #
#                    -------------------------                  #
#                                                               #
#     Author: Vojtech Brhlik                                    #
#     Date:   April 2025                                        #
#                                                               #
#################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clear_graph(df: pd.DataFrame):
    """Function clears graph of all unwanted values specified for each line

    Args:
        df (pd.DataFrame): Dataframe to clear
    """
    #remove all VS maps
    df = df[~df['name'].str.match(r'^(RHQ BONK CUP)( -)? (VS)?.*')]
    #remove all snekula maps
    df = df[~df['name'].str.match(r'^(SNEKULA).*')]
    #remove all maps made by someone else
    df = df[~df['name'].str.match(r'.* (?i)(by) .*$')]
    #remove all snekegrounds
    df = df[~df['name'].str.match(r'^(?i)(snekeground) .*$')]
    #remove Phil-622 maps since that was from different event (F1 maps)
    df = df[~df['author_nickname'].str.match('Phil-622', na=False)]

    #people use different nicknames, so we use the latest nickname for every login (for example switch eLconn15 to speq.x)
    df['author_nickname'] = df['author_login'].map(df.groupby('author_login')['author_nickname'].first())
    return(df)    

df = clear_graph(pd.read_excel("Karma_RHQBonkCup.xlsx"))

############################ MAP PER MAPPER ############################
mapper_count = df['author_nickname'].value_counts()
mapper_count.head(10).plot(kind='bar', figsize=(10, 6), title='Top 10 mappers by map count', zorder=3)

plt.xlabel('Mapper')
plt.ylabel('Map count')
plt.grid(axis='y', linestyle='--', linewidth=1, zorder=0)
plt.tight_layout()  
plt.savefig('mapCount.png')
plt.close()

############################ MAPPER RATING ############################
#only count mappers with 5 or more maps
valid_authors = mapper_count[mapper_count >= 5].index
authors_df = df[df['author_nickname'].isin(valid_authors)]
#only count maps with 5 or more votes
authors_df = authors_df[authors_df['number_of_votes'] >= 5]

authors_df['average_karma'] = (authors_df['average_karma'] + 1.0)*5.0

avgs_df = authors_df.groupby(authors_df['author_nickname'])['average_karma'].mean()
avgs_df = avgs_df.sort_values(ascending=False)

avgs_df.head(10).plot(kind='bar', 
                      figsize=(10,6), 
                      title="Top 10 mappers by average rating", 
                      zorder=3,
                      yticks=np.arange(0, 11, 1)
                    )

plt.xlabel('Mapper')
plt.ylabel('Rating')
plt.grid(axis='y', linestyle='--', linewidth=1, zorder=0)
plt.tight_layout()  
plt.figtext(0.2, 
            0.01, 
            "Counting mappers with 5+ maps\n and maps with 5+ votes", 
            ha="center", 
            fontsize=10, 
            bbox={"alpha":0.5, "pad":5}
        )
plt.savefig('mapperRating.png')
plt.close()

############################ MAPPER RATING OF TOP 10 MAPPERS BY MAP COUNT ############################
top_mappers = mapper_count.head(10).index
print("MAPPER RATING OF TOP 10 MAPPERS BY MAP COUNT")
for mapper in top_mappers:
    print(mapper, avgs_df[mapper])
    
############################ MAP COUNT OF TOP 10 MAPPERS BY MAP RATING ############################
top_mappers = avgs_df.head(10).index
print("\n\n\nMAP COUNT OF TOP 10 MAPPERS BY MAP RATING")
for mapper in top_mappers:
    print(mapper, mapper_count[mapper])
    
    
############################ INDIVIDUAL MAPS ############################
print("\n\n\nWORST MAP WITH 5+ VOTES")
df = df[df['number_of_votes'] >= 5]
min_rating = df['average_karma'].min()
lowest_maps = df.loc[df['average_karma'] == min_rating]
print(lowest_maps[['name', 'author_nickname']].to_string(index=False))

print("\n\n\nBEST MAP WITH 5+ VOTES")
df = df[df['number_of_votes'] >= 5]
max_rating = df['average_karma'].max()
highest_maps = df.loc[df['average_karma'] == max_rating]
print(highest_maps[['name', 'author_nickname']].to_string(index=False))