import pandas as pd
from IPython.display import display
import re

def extract():
    df_given = pd.read_csv('disney_movies.csv')
    return df_given

def transform(df_given):
    total_missings = df_given.isnull().sum()
    columns_df = df_given.columns.tolist()
    df = df_given
    # print(total_missings != 0) # devuelve True para 'genre' y para 'mpaa_rating' (en estas categorías hay Nones)
    for column in columns_df:
        if total_missings[column] != 0:
            df[column] = df_given[column].fillna('No ' + column)
    
    genres = df['genre'].unique().tolist()
    genres.remove('No genre')
    # df_nogenre = pd.DataFrame(columns = columns_df)
    # for i in range(df.shape[0]):
    #     if df['genre'][i] == 'No genre':
    #         df_nogenre = df_nogenre.append(df.iloc[i], ignore_index = True)
    df_nogenre = df[df['genre'] == 'No genre'] # df with all the 'no genre' films
    df_nogenre = df_nogenre.sort_values(by = 'total_gross', ascending = False).reset_index()
    
    selection = ''
    while selection not in genres: # the input needs to be identical to the given name
        selection = input('Select a movie genre out of the following: ' + str(genres) + ' ')
    
    df_search = pd.DataFrame(columns = columns_df)
    regex_use = re.compile(selection, re.I)
    for i in range(df.shape[0]):
        ocurrencia = re.findall(regex_use, df['genre'][i])
        if ocurrencia != []:
            df_search = df_search.append(df.iloc[i], ignore_index = True)
            # van a quitar la función append de versiones futuras de pandas
    df_search = df_search.sort_values(by = 'total_gross', ascending = False).reset_index()
    return df_search, df_nogenre

def load(df_search, df_nogenre):
    print('The first suggested films for you are the following: ')
    display(df_search.head(10))
    more = ''
    contador = 10
    while more not in ['n', 'N']:
        more = ''
        while more not in ['y', 'n', 'Y', 'N']:
            more = input('Would you like some more suggestions? [Y/N] ')
        if more == 'y' or more == 'Y':
            if not df_search[contador:contador+10].empty:
                display(df_search[contador:contador+10])
                contador += 10
            else:
                print('There are no more available suggestions for the selected genre, but here are other films you may enjoy')
                display(df_nogenre)
                more = 'n'

if __name__ == '__main__':
    df_given = extract()
    df_search, df_nogenre = transform(df_given)
    load(df_search, df_nogenre)