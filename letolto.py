import yt_dlp

def letoltes_mp3(url):
    opciok = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s', # A fájl neve a videó címe lesz
    }
    
    with yt_dlp.YoutubeDL(opciok) as ydl:
        ydl.download([url])

link = input("Add meg a YouTube linket: ")
letoltes_mp3(link)
print("Kész! A fájlt megtalálod a szkript mellett.")
