# ToSpotify

> Easily add songs to a spotify playlist, right from your terminal!

## Usage

Run the following commands to initialize the virtual environment:

```
make venv
source venv/bin/activate
```

Now, you need to set up your SPOTIPY API keys correctly. I personally store the following in `spotify_credentials`:

```
export SPOTIPY_CLIENT_ID='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
export SPOTIPY_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
export SPOTIPY_REDIRECT_URI='tospotify://tospotify'
```

Then, to use these, simply type `source spotify_credentials`.

Now, adding songs to a playlist is as simple as:

```
python to_spotify.py USERNAME PLAYLISTNAME SONG1 SONG2 SONG3 ...
```

## License

[The MIT License](https://jay.mit-license.org/2018)
