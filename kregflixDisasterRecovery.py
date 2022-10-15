from plexapi.myplex import MyPlexAccount
import plexapi
import traceback
import sqlite3

account = MyPlexAccount('xxx', 'XXX')
plex = account.resource('xxx').connect()
movies = plex.library.section('xxx')
shows = plex.library.section('xxx')

def sortMovieIDByDateReleased(movieData):
    sortedMovieIDs = []
    dictionaryLength = len(movieData)
    counter = 0
    while counter < dictionaryLength:
        sortedMovieIDs.append(min(movieData, key=movieData.get))
        del movieData[(min(movieData, key=movieData.get))]
        counter += 1
    return sortedMovieIDs

def updateSortTitles():
    conn = sqlite3.connect('xxx')
    conn.row_factory = lambda cursor, row: row[0] #returns as list instead of tuple
    cursor = conn.cursor()

    cursor.execute("SELECT SEARCHTITLE FROM TitleUpdates")
    searchTitles = cursor.fetchall()

    cursor.execute("SELECT OUTPUTTITLE FROM TitleUpdates")
    outputTitle = cursor.fetchall()

    cursor.execute("SELECT SKIPTITLE FROM SkipTitles INNER JOIN TitleUpdates ON SkipTitles.SKIPID = TitleUpdates.SKIPID")
    skipTitles = cursor.fetchall()

    conn.close()

    movieData = {}
    for index, title in enumerate(searchTitles):
        search = movies.search(title)

        for movie in search:
            movieData.update({movie.ratingKey: movie.originallyAvailableAt})
            for skipTitle in skipTitles:
                if(skipTitle == movie.title.lower()):
                    del movieData[movie.ratingKey]
                
        movieIDs = sortMovieIDByDateReleased(movieData)
        movieCounter = 1

        for id in movieIDs:
            item = plex.fetchItem(id)
            edits = {'titleSort.value': title+str(movieCounter), 'titleSort.locked':1}
            item.edit(**edits)
            item.reload
            movieCounter += 1
        movieData = {}
        print(outputTitle[index] + ' Sort Titles Updated!')

def updatePosters():
    conn = sqlite3.connect('xxx')
    conn.row_factory = lambda cursor, row: row[0] #returns as list instead of tuple
    cursor = conn.cursor()

    cursor.execute("SELECT SEARCHTITLE FROM PosterUpdates")
    searchTitles = cursor.fetchall()

    cursor.execute("SELECT OUTPUTTITLE FROM PosterUpdates")
    outputTitle = cursor.fetchall()

    cursor.execute("SELECT DBTABLE FROM PosterUpdates")
    dbTables = cursor.fetchall()

    cursor.execute("SELECT SKIPTITLE FROM SkipTitles INNER JOIN PosterUpdates ON SkipTitles.SKIPID = PosterUpdates.SKIPID")
    skipTitles = cursor.fetchall()

    conn.close()

    movieData = {}
    for index, title in enumerate(searchTitles):
        conn = sqlite3.connect('xxx')
        conn.row_factory = lambda cursor, row: row[0] #returns as list instead of tuple
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + dbTables[index])
        posterURLs = cursor.fetchall()
        conn.close()

        search = movies.search(title)

        for movie in search:
            movieData.update({movie.ratingKey: movie.originallyAvailableAt})
            for skipTitle in skipTitles:
                if(skipTitle == movie.title.lower()):
                    del movieData[movie.ratingKey]
                
        movieIDs = sortMovieIDByDateReleased(movieData)
        movieCounter = 1

        for id in movieIDs:
            item = plex.fetchItem(id)
            item.uploadPoster(posterURLs[movieCounter - 1])
            item.reload
            movieCounter += 1

        movieData = {}
        print(outputTitle[index] + ' Posters Updated!')

def updateMiscSortTitles():
    #fast five because it doesn't have furious in the title
    search = movies.search('fast five')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'titleSort.value': 'fast and furious5', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('Fast Five Sort Title Updated!')

    #f9 because fast and furious naming conventions are non existant
    search = movies.search('f9')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'titleSort.value': 'fast and furious9', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('F9: The Fast Saga Sort Title Updated!')

    #jason goes to hell to put it with friday the 13th
    search = movies.search('jason goes to hell')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'title.value': 'Friday the 13th: Jason Goes to Hell: The Final Friday', 'titleSort.value': 'friday the 13th9', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('Jason Goes to Hell: The Final Friday Sort Title Updated!')

    #jason x to put it with friday the 13th
    search = movies.search('jason x')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'title.value': 'Friday the 13th: Jason X', 'titleSort.value': 'friday the 13th10', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('Jason X Sort Title Updated!')

    #freddy's dead to put it with nightmare on elm street
    search = movies.search('freddy\'s dead')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'title.value': 'A Nightmare on Elm Street: Freddy\'s Dead: The Final Nightmare', 'titleSort.value': 'nightmare on elm street6', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('Freddy\'s Dead: The Final Nightmare Sort Title Updated!')

    #new nightmare to put it with nightmare on elm street
    search = movies.search('new nightmare')
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    edits = {'title.value': 'A Nightmare on Elm Street: New Nightmare', 'titleSort.value': 'nightmare on elm street7', 'titleSort.locked':1}
    item.edit(**edits)
    item.reload
    print('New Nightmare Sort Title Updated!')

def updateMiscPosters(movieTitle):
    conn = sqlite3.connect('xxx')
    conn.row_factory = lambda cursor, row: row[0] #returns as list instead of tuple
    cursor = conn.cursor()
    cursor.execute("SELECT URL FROM Misc WHERE TITLE = ?", (movieTitle,)) #case sensitive search
    posterURLs = cursor.fetchall()
    conn.close()

    movieData = {}
    search = movies.search(movieTitle)
    id = search[0].ratingKey
    item = plex.fetchItem(id)
    item.uploadPoster(posterURLs[0])
    item.reload

    print( movieTitle + ' Poster Updated!')


#updateSortTitles()
#updatePosters()


#***********************************#
#                                   #
#            TESTING                #
#                                   #
#***********************************#
def sortTest(searchTitle, sortTitle, outputTitle, skipTitles = []):
    movieData = {}
    search = movies.search(searchTitle)

    for movie in search:
        if(skipTitles):
            for title in skipTitles:
                if(title != movie.title.lower()):
                    movieData.update({movie.ratingKey: movie.originallyAvailableAt})
        else:
            movieData.update({movie.ratingKey: movie.originallyAvailableAt})       

    movieIDs = sortMovieIDByDateReleased(movieData)
    movieCounter = 1

    for id in movieIDs:
        item = plex.fetchItem(id)
        edits = {'titleSort.value': sortTitle+str(movieCounter), 'titleSort.locked':1}
        item.edit(**edits)
        item.reload
        movieCounter += 1

    print( outputTitle + ' Sort Titles Updated!')

def posterTest(searchTitle, outputTitle, dbTable, skipTitles = []):
    conn = sqlite3.connect('xxx')
    conn.row_factory = lambda cursor, row: row[0] #returns as list instead of tuple
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + dbTable)
    posterURLs = cursor.fetchall()
    conn.close()

    movieData = {}
    search = movies.search(searchTitle)

    for movie in search:
        if(skipTitles):
            for title in skipTitles:
                if(title != movie.title.lower()):
                    movieData.update({movie.ratingKey: movie.originallyAvailableAt})
        else:
            movieData.update({movie.ratingKey: movie.originallyAvailableAt}) 

    movieIDs = sortMovieIDByDateReleased(movieData)
    movieCounter = 1

    for id in movieIDs:
        item = plex.fetchItem(id)
        item.uploadPoster(posterURLs[movieCounter - 1])
        item.reload
        movieCounter += 1

    print( outputTitle + ' Posters Updated!')



sortTest('pirates of the caribbean', 'pirates of the caribbean', 'pirates of the caribbean')
posterTest('pirates of the caribbean', 'pirates of the caribbean', 'PiratesOfTheCaribbean')
#updateMiscSortTitles()

#TODO
#death wish
#sharknado
#star wars - real order - probably use its own function
#texas chainsaw massacre
#vhs
#bad boys
#jackass
#hellraiser
#the hobbit
#hostel
#naked gun