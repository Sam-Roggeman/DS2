# Assignment 2 : MicroServices

## Microservices:

1. gui
2. users_persistent
3. users
4. friends_persistent
5. friends
6. playlists_persistent
7. playlists
8. songs_persistent
9. songs
10. feed_persistent
11. feed

## GUI

### Description

This is the service that handles the main interface between the user and the application.
It is a web application that is built using the Flask framework.
It is responsible for the following:

1. Fetching the pages of the application for the user
2. Main service that the user interacts with
3. Passing the user input to the appropriate microservice by sending requests to the microservice's API
4. Endpoints:
    1. /login Inteface for the login page, passes the user input to the users microservice.
    2. /register Interface for the register page, passes the user input to the users microservice.
    3. /add_friend Redirects to /friends page, passes the user input to the friends microservice
    4. /friends passes Interface for friends, fetches output from the friends microservice
    5. /create_playlist Redirects to /playlists, passes the user input to the playlists microservice
    6. /add_song_to/<int: playlist_id> Redirects to /playlists/<int: playlist_id> passes the user input to the playlists
       microservice
    7. /playlists Interface for the playlists, fetches from the playlists microservice
    8. /playlists/<int: playlist_id> Interface for the playlist, passes the user input to the playlists microservice
    9. / Interface for feed, fetches from the feed microservice
    10. /catalogue Interface for the catalogue of songs, fetches from the songs microservice
    11. /invite_user_to/<int: playlist_id> Redirects to /playlists/<int: playlist_id>, passes the user input to the
        playlists microservice
    12. /logout Redirects to /

## Users Persistent

### Description

This is the service that holds the database of the users.
It is responsible for the following:

1. Creating the database "users"
2. Creating the tables
    1. users (username,password)
3. Hosting the database

## Users

### Description

This is the service that handles the user data and anything related to it.
It uses the users_persistent service to store and retrieve the data.
It opens a connection with the database on the users_persistent service and passes a query.
It is responsible for the following:

1. Creating a new user /users/register/
    1. Checking in the database if the username already exists
    2. Adding the user to the database
2. Logging in a user /users/login/
    1. Checking in the database if the username exists
    2. Checking in the database if the password matches the username
3. Checking if a user exists /users/exists/
    1. Checking in the database if the username exists
4. Endpoints:
    1. POST /users/register/
        1. input string username: username of the user
        2. input string password: password of the user
        3. returns boolean: True on success, False otherwise
    2. POST /users/login/
        1. input string username: username of the user
        2. input string password: password of the user
        3. returns boolean: True on success, False otherwise
    3. GET /users/exists/
        1. input string username: username of the user
        2. returns boolean: True on existence, False otherwise

## Friends_Persistent

### Description

This is the service that holds the database of the friends.
It is responsible for the following:

1. Creating the database "friends"
2. Creating the tables
    1. friends (username,username_friend)
3. Hosting the database

## Friends

### Description

This is the service that handles the friends data and anything related to it.
It uses the friends_persistent service to store and retrieve the data.
It opens a connection with the database on the friends_persistent service and passes a query.
It is responsible for the following:

1. Adding a friend
    1. Checking in the database if the friend is already added
    2. Checking in the database if the friend exists -> /users/exists/
    3. Checking in the database if the user exists -> /users/exists/
    4. Adding the friend to the database
2. Retrieving a friendlist
    1. Checking in the database if the user exists -> /users/exists/
    2. Retrieving the friendlist from the database
3. Endpoints:
    1. POST /friends/add/
        1. input string username1: username of user 1
        2. input string username2: username of user 2
        3. returns boolean: True on success, False otherwise
    2. GET /friends/
        1. input string username: username of the user
        2. returns list: list of friends

## Playlists_Persistent

### Description

This is the service that holds the database of the playlists.
It is responsible for the following:

1. Creating the database "playlists"
2. Creating the tables
    1. playlists (playlist_id, username, playlist_name)
    2. songInPlaylist (playlist_id, artist, title)
    3. playlistSharedWith (playlist_id, username)
3. Hosting the database

## Playlists

### Description

This is the service that handles the playlists data and anything related to it.
It uses the playlists_persistent service to store and retrieve the data.
It opens a connection with the database on the playlists_persistent service and passes a query.
It uses the song service to validate the existence of songs.
It uses the users service to validate the existence of users.
It uses the feed service to add new activities.
It is responsible for the following:

1. Creating a new playlist - POST /playlists/create/
   Creates a new playlist named "title" for the user "owner"
    1. Input string owner: username of the user/owner
    2. Input string title: name of the playlist
    3. Returns boolean: True on success, False otherwise
2. Adding a song to a playlist - POST /playlists/add_song/
    1. Input string title: name of the song
    2. Input string artist: name of the artist
    3. Input int playlist_id: id of the playlist
    4. Input string owner: username of the owner of the playlist
    5. Returns boolean: True on success, False otherwise
3. Retrieving all playlists - GET /playlists/ or GET /playlists/owned/
    1. Input string username: username of the owner of the playlist
    2. Returns list(int): list of owned playlists (ids)
4. Retrieving all shared playlists - GET /playlists/shared/
    1. Input string username: username of the user
    2. Returns list(int): list of shared playlists (ids)
5. Retrieving a playlist - GET /playlists/<int: playlist_id>/
    1. Input int playlist_id: id of the playlist
    2. Returns list(string,string): list of songs in the playlist (title, artist)
6. Invite a user to a playlist - POST /playlists/<int: playlist_id>/invite/
    1. Input int playlist_id: id of the playlist
    2. Input string username: username of the user to invite
    3. Input string username_owner: username of the owner of the playlist
    4. Returns boolean: True on success, False otherwise

## Songs_Persistent
### Description

This is the service that holds the database of the songs.
It is responsible for the following:

1. Creating the database "songs"
2. Creating the tables
    1. songs (artist, title)
3. Populating the database with the songs from the csv file
4. Hosting the database

## Songs

### Description

This is the service that handles the songs data and anything related to it.
It uses the songs_persistent service to store and retrieve the data.
It opens a connection with the database on the songs_persistent service and passes a query.
It is responsible for the following:

1. Retrieving all songs
    1. Retrieving all songs from the database
2. Checking if a song exists
    1. Checking in the database if the song exists
3. Adding a song
    1. Checking in the database if the song exists
    2. Adding the song to the database

## Feed_Persistent

### Description

This is the service that holds the database of the feed.
It is responsible for the following:

1. Creating the database "feed"
2. Creating the tables
    1. feed (activity_id, username, description, timestamp)
3. Hosting the database

## Feed

### Description

This is the service that handles the feed data and anything related to it.
It uses the feed_persistent service to store and retrieve the data.
It opens a connection with the database on the feed_persistent service and passes a query.
It is responsible for the following:

1. Adding an activity to the feed /activities/add/
    1. Checking in the database if the user exists -> /users/exists/
    2. Adding the activity to the database
2. Retrieving the feed /activities/ or /feed/
    1. Checking in the database if the user exists -> /users/exists/
    2. Retrieving the feed from the database
