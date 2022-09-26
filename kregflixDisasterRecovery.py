from plexapi.myplex import MyPlexAccount
import plexapi
import traceback
import sqlite3

account = MyPlexAccount('ACCOUNT_NAME', 'PASSWORD')
plex = account.resource('SERVER_NAME').connect()
movies = plex.library.section('MOVIE_SECTION_NAME')
shows = plex.library.section('TV_SECTION_NAME')

def sortMovieIDByDateReleased(movieData):
    sortedMovieIDs = []
    dictionaryLength = len(movieData)
    counter = 0
    while counter < dictionaryLength:
        sortedMovieIDs.append(min(movieData, key=movieData.get))
        del movieData[(min(movieData, key=movieData.get))]
        counter += 1
    return sortedMovieIDs

def updateSortTitle(searchTitle, sortTitle, outputTitle):
    movieData = {}
    search = movies.search(searchTitle)
    for movie in search:
        movieData.update({movie.ratingKey: movie.originallyAvailableAt})
    movieIDs = sortMovieIDByDateReleased(movieData)
    movieCounter = 1
    for id in movieIDs:
        item = plex.fetchItem(id)
        edits = {'titleSort.value': sortTitle+str(movieCounter), 'titleSort.locked':1}
        item.edit(**edits)
        item.reload
        movieCounter += 1
    print( outputTitle + ' Sort Titles Updated!\r\n')

def updatePosters(searchTitle,sortTitle,outputTitle, dbTable):
    conn = sqlite3.connect('DB_PATH')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + dbTable)
    posterURLs = cursor.fetchall()
    conn.close()

    movieData = {}
    search = movies.search(searchTitle)
    for movie in search:
        movieData.update({movie.ratingKey: movie.originallyAvailableAt})
    movieIDs = sortMovieIDByDateReleased(movieData)
    movieCounter = 1
    for id in movieIDs:
        item = plex.fetchItem(id)
        item.uploadPoster(posterURLs[movieCounter - 1])
        item.reload
        movieCounter += 1
    print( outputTitle + ' Posters Updated!\r\n')

def updateMiscSortTitles():
    #fast five because it doesn't have furious in the title
    search = movies.search('fast five')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'titleSort.value': 'fast and furious5', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('Fast Five Sort Title Updated!\r\n')

updateSortTitle('harry potter', 'harry potter', 'Harry Potter')
updateSortTitle('furious', 'fast and furious', 'Fast and Furious')
updateSortTitle('transformers', 'transformers', 'Transformers')
updateSortTitle('twilight', 'twilight', 'Twilight')
updateSortTitle('resident evil', 'resident evil', 'Resident Evil')
updateMiscSortTitles()

updatePosters('harry potter', 'harry potter', 'Harry Potter', 'HarryPotter')