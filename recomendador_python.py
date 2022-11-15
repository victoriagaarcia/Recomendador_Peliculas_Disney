# se importan las librerías necesarias
import pandas as pd
from IPython.display import display
import re

# este recomendador sigue la estructura de una ETL

def extract():
    df_given = pd.read_csv('disney_movies.csv') # se extraen los datos del csv en forma de dataframe
    return df_given

def transform(df_given):
    total_missings = df_given.isnull().sum() # se obtiene el total de valores nulos
    columns_df = df_given.columns.tolist() # se saca una lista con los nombres de las columnas
    df = df_given
    # print(total_missings != 0) # devuelve True para 'genre' y para 'mpaa_rating' (en estas categorías hay Nones)
    for column in columns_df:
        if total_missings[column] != 0: # se cogen las columnas en las que haya valores nulos
            df[column] = df_given[column].fillna('No ' + column) # se reemplaza cada valor nulo por un 'no existe' dependiendo de la columna
    
    genres = df['genre'].unique().tolist() # se saca una lista con todos los posibles géneros
    genres.remove('No genre') # se elimina la opción de 'género no definido' de los posibles géneros
    df_nogenre = df[df['genre'] == 'No genre'] # se obtiene el dataframe que contiene todas las películas con 'género no definido'
    df_nogenre = df_nogenre.sort_values(by = 'total_gross', ascending = False).reset_index() 
    # se ordena el dataframe de películas sin género en base al éxito que tuvieron (dinero ganado)
    
    selection = ''
    while selection not in genres: # el input introducido con el género deseado ha de ser idéntico al género incluido en la lista de opciones
        selection = input('Select a movie genre out of the following: ' + str(genres) + ' ')
    
    df_search = pd.DataFrame(columns = columns_df) # se crea un nuevo dataframe con las mismas columnas que el dataframe para poder modificarlo
    regex_use = re.compile(selection, re.I) # se emplea regex ignorando las mayúsculas en la búsqueda
    for i in range(df.shape[0]): # se busca a lo largo de todas las filas del dataframe
        ocurrencia = re.findall(regex_use, df['genre'][i]) # se busca la selección con el método 'findall' de re
        if ocurrencia != []: # si 'findall' devuelve alguna ocurrencia
            df_search = df_search.append(df.iloc[i], ignore_index = True) # se añade la fila con el género seleccionado al dataframe de búsqueda
            # van a quitar la función append de versiones futuras de pandas
    df_search = df_search.sort_values(by = 'total_gross', ascending = False).reset_index() # se ordena el dataframe de búsqueda en base al éxito
    return df_search, df_nogenre

def load(df_search, df_nogenre):
    print('The first suggested films for you are the following: ')
    display(df_search.head(10)) # se ofrecen las 10 primeras recomendaciones de películas
    more = ''
    contador = 10
    while more not in ['n', 'N']: # se continúa preguntando por recomendaciones hasta que se especifique que no se quieren más
        more = ''
        while more not in ['y', 'n', 'Y', 'N']: # se continúa preguntando si la respuesta no es válida
            more = input('Would you like some more suggestions? [Y/N] ')
        if more == 'y' or more == 'Y': # si se indica que sí, se ofrecen 10 recomendaciones más
            if not df_search[contador:contador+10].empty:
                display(df_search[contador:contador+10])
                contador += 10 # se guarda que se han mostrado 10 recomendaciones más, para futuras recomendaciones
            else:
                print('There are no more available suggestions for the selected genre, but here are other films you may enjoy')
                # si no quedan recomendaciones del género seleccionado, se muestran las películas de género no definido
                display(df_nogenre)
                more = 'n'

if __name__ == '__main__':
    df_given = extract() # se sacan los datos del csv 
    df_search, df_nogenre = transform(df_given) # se transforman los datos para obtener los dataframes con los que queremos trabajar
    load(df_search, df_nogenre) # se muestran las recomendaciones pedidas empleando los dataframes creados