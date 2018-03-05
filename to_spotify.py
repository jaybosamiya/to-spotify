import sys

import spotipy
import spotipy.util as util

if len(sys.argv) == 4:
    username = sys.argv[1]
    playlist_name = sys.argv[2]
    track_name = sys.argv[3]
else:
    print "Usage: %s username playlist_name track" % (sys.argv[0],)
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.search(q=track_name, type='track')

    tracks = []
    for track in results['tracks']['items']:
        tracks.append({
            'name': track['name'],
            'artists': ', '.join(a['name'] for a in track['artists']),
            'id': track['id']
        })

    if len(tracks) == 0:
        print "No such tracks found"
        sys.exit(1)

    for i, track in enumerate(tracks):
        print("%d) %s - %s" % (i, track['artists'], track['name']))

    print("")
    choice = raw_input('Pick a track: ')

    if choice in ('', 'n'):
        print "Nothing added"
        sys.exit(0)

    try:
        choice = int(choice)
    except ValueError:
        print "Choose an integer choice!"
        sys.exit(2)

    if choice < 0 or choice >= len(tracks):
        print "Choose a valid track!"
        sys.exit(3)

    track_id = tracks[choice]['id']

    playlists = []
    while True:
        results = sp.current_user_playlists(offset=len(playlists))
        playlists.extend(results['items'])
        if (len(playlists) >= results['total']):
            break

    playlist_ids = [p['id'] for p in playlists if p['name'] == playlist_name]

    if len(playlist_ids) > 1:
        print "Whut?! Impossible number of same named playlists"
        sys.exit(4)
    elif len(playlist_ids) < 1:
        playlist_id = sp.user_playlist_create(username, playlist_name)['id']
    else:
        playlist_id = playlist_ids[0]

    results = sp.user_playlist_add_tracks(username, playlist_id, [track_id])

    print "Done! :)"

else:
    print "Can't get token for", username
