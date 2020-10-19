""" search module to get artist albums from Discogs """

import discogs_client as dc
import time
from pkg_sound_system.compare_sentences import sentence_similarity as sensim
# import requests as r


class search_api:

    def __init__(self):
        oauth_token = "SFEBGVdOuNYcbmwWyamGRqBQxDGiBNSysGLfKjzM"
        self.d = dc.Client(
            'SoundSystemDiscogsApp/0.1',
            user_token=oauth_token
        )

    def search_r(self, my_query: str):
        """ connect to the discogs API and search for the user query """
        # print(f"{my_query=}")
        try:
            results = self.d.search(
                my_query,
                type='release',
                format='CD,album'
            )
            # print(f"{results.pages=}")
            # print(f"{len(results)=}")
            artist = results[0].artists[0]
            artist.name
            # print(f"{artist.name=}")
            albums_names = []
            total_album = []
            val = 0
            i = 0
            init_time = time.time()
            while self.deconte(init_time) < 15:
                if not albums_names:
                    val = 0
                else:
                    for album_name in albums_names:
                        instance = sensim(album_name, results[i].title)
                        if instance.similarity_percentage() > 0.60:
                            val += 1
                if val == 0:
                    tracklist = []
                    videos = []
                    # print(f"######## ALBUM :: {results[i].title} ########")
                    # print(f"{results[i].genres=}")
                    # print(results[i].images[0]['uri'])
                    # print("### tracks")
                    for track in results[i].tracklist:
                        # track_var = f">{track.position}-"
                        # track_var += "{track.title}-{track.duration}")
                        # Print(track_var)
                        tracklist.append({
                            'position': track.position,
                            'title': track.title,
                            'duration': track.duration
                        })
                    # print("### ytb videos")
                    for video in results[i].videos:
                        # print(f"{video.title=}:{video.url=}")
                        videos.append({'title': video.title, 'url': video.url})
                    for elem in tracklist:
                        for vid in videos:
                            compare_titles = sensim(
                                elem['title'],
                                vid['title']
                            )
                            if compare_titles.similarity_percentage() > 0.70:
                                elem['url'] = vid['url']
                                # vt = f"video {vid['title']}"
                                # vt += "track {elem['title']}"
                                # print(vt)
                                # print("########################################")
                    # print(f"######### ALBUM :: {results[i].title} #########")
                    # print(f"{tracklist=}")
                    album = {
                        'artist': artist.name,
                        'title': results[i].title,
                        'image': results[i].images[0]['uri'],
                        'genre': results[i].genres,
                        'tracklist': tracklist
                    }
                    total_album.append(album)
                    albums_names.append(results[i].title)
                    time.sleep(1.5)
                i += 1
            if not total_album:
                return ["the album variable from search.py is empty."]
            else:
                return total_album
        except Exception as e:
            print(f"serah_r from search.py {e=}")

    def deconte(self, set_time: float):
        return time.time() - set_time


if __name__ == '__main__':
    s = search_api()
    ise = s.search_r(str(input("search artist track or album : ")))
    print(ise)
