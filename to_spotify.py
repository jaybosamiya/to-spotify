import sys

import spotipy
import spotipy.util as util


def find_track(track_name):
    print "Searching for: '%s'" % track_name

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
        return None

    for track in tracks:
        name = track['name']
        artist = track['artists']
        if (track_name.lower() in (
                x.lower() for x in (
                    name,
                    artist + ' - ' + name,
                    name + ' - ' + artist))):
            print "Found '%s' perfectly :)" % track_name
            return track['id']

    for i, track in enumerate(tracks):
        print("%d) %s - %s" % (i, track['artists'], track['name']))

    while True:
        choice = raw_input('Pick a track: ')
        if choice == 'n':
            print "Okay, no such track"
            return None

        try:
            choice = int(choice)
            break
        except ValueError:
            print "Choose an integer choice!"

        if choice < 0 or choice >= len(tracks):
            print "Choose a valid track!"

    return tracks[choice]['id']


def find_or_create_playlist(playlist_name):
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
        result = sp.user_playlist_create(username, playlist_name)
        print "Created playlist"
        return result['id']
    else:
        return playlist_ids[0]


if len(sys.argv) >= 4:
    username = sys.argv[1]
    playlist_name = sys.argv[2]
    track_names = sys.argv[3:]
else:
    print "Usage: %s username playlist_name tracks..." % (sys.argv[0],)
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    playlist_id = find_or_create_playlist(playlist_name)
    track_ids = [find_track(t) for t in track_names]

    track_ids = [x for x in track_ids if x is not None]
    if len(track_ids) == 0:
        print "No tracks added"
    else:
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print "Done adding %d tracks! :)" % len(track_ids)

else:
    print "Can't get token for", username
