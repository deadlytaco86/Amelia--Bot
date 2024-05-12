import os
from pytube import YouTube
from pytube import Search

def search(key: str, depth: int):
    s = Search(key)
    round_1 = len(s.results)

    while (depth - 1) > 0:
        s.get_next_results()
        depth -= 1
        print(depth)

    #print(f'found {len(s.results)} results')
    return s



def plunder(id, folder = None):
    yt = YouTube.from_id(id)
    try:
        stream = yt.streams.get_by_itag(140)
    except:
        stream = yt.streams.get_by_itag(139)
    if folder == None:
        path = stream.download('C:\\Desktop\\Ad free music for when AdBlock fails\\Unsorted')
        os.rename(path, path.split('.mp4')[0] + '.mp3')
    else:
        available = ['regular', 'ost', 'soundtrack', 'classical', 'christmas']
        folder_name = ['Every song', 'Game OST', 'Movie and Show themes', 'Classical', 'Christmas'][available.index(folder)]
        path = stream.download(f'C:\\Desktop\\Ad free music for when AdBlock fails\\{folder_name}')
        os.rename(path, path.split('.mp4')[0] + '.mp3')