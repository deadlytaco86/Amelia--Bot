import yt_dlp

def search(query, max_results=10, test=False):
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',  # Prevents downloading the video, just retrieves the metadata
        'force_generic_extractor': True,  # Uses a generic extractor to perform the search
    }
    
    search_url = f"ytsearch{max_results}:{query}"
    results = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_url, download=False)
    
    if 'entries' in result:
        videos = result['entries']
        for video in videos:
            title = video.get('title')
            duration = video.get('duration')
            uploader = video.get('uploader')
            upload_date = video.get('upload_date') if video.get('upload_date') is not None else video.get('release_date')
            url = video.get('url')
            if test:
                print(f"Title: {title}")
                print(f"Duration: {duration} seconds")
                print(f"Channel: {uploader}")
                print(f"Upload Date: {upload_date}")
                print(f"URL: {url}")
                print("-----")
            results.append((title, duration, uploader, upload_date, url))
        return results
    else:
        print("No results found")
        return []
    
def plunder(video_url, folder=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'C:/Desktop/Ad free music for when AdBlock fails/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    if folder:
        available = ['regular', 'ost', 'soundtrack', 'classical', 'christmas']
        folder_name = ['Every song', 'Game OST', 'Movie and Show themes', 'Classical', 'Christmas'][available.index(folder)]
        ydl_opts['outtmpl'] = f'C:/Desktop/Ad free music for when AdBlock fails/{folder_name}/%(title)s.%(ext)s'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'{video_url}'])

if __name__ == '__main__':
    results = search("oh island in the sun", max_results=10, test=True)
    for result in results:
        print(f"Title: {result[0]}")
        print(f"Duration: {result[1]} seconds")
        print(f"Channel: {result[2]}")
        print(f"Upload Date: {result[3]}")
        print(f"URL: {result[4]}")
        print("-----")
    if len(results) > 0:
        choice = input('enter a number 1-10: ')
        if choice == '0':
            pass
        else:
            plunder(results[int(choice)-1][4])
