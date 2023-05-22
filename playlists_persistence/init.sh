#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE playlists;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "playlists" <<-EOSQL
    CREATE TABLE playlists(
      playlist_id serial primary key,
      title TEXT NOT NULL DEFAULT 'New Playlist',
      username_owner TEXT NOT NULL
    );


    CREATE TABLE songInPlaylist(
      playlist_id int references playlists(playlist_id) NOT NULL,
      artist TEXT NOT NULL,
      title TEXT NOT NULL,

      PRIMARY KEY (playlist_id, artist,title)
    );

    CREATE TABLE playlistSharedWith(
      playlist_id int references playlists(playlist_id) NOT NULL,
      username TEXT NOT NULL,

      PRIMARY KEY (playlist_id, username)
    );
EOSQL
