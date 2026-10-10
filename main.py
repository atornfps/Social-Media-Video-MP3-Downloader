import yt_dlp
import os
import threading
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

cancel_download=False

def start_download_thread():

    global cancel_download,download_phase
    cancel_download=False
    download_phase=1

    url=url_entry.get().strip()
    format_choice=format_option.get().lower()

    if not url:
        status_label.configure(text="Lütfen geçerli bir bağlantı girin!", text_color="red")
        return

    status_label.configure(text="İndirme başlatılıyor, lütfen bekleyin... ", text_color="yellow")
    progress_bar.set(0)
    progress_label.configure(text="%0")

    download_button.configure(state="disabled")
    cancel_button.pack(side="left", padx=10)
    cancel_button.configure(state="normal")
    progress_bar.pack(pady=(12,4))
    progress_label.pack()

    download_thread=threading.Thread(target=download_video, args=(url,format_choice))
    download_thread.start()

def cancel_download_action():
    global cancel_download
    cancel_download=True
    status_label.configure(text="İndirme iptal ediliyor...", text_color="orange")
    cancel_button.configure(state="disabled")

download_phase=1

def progress_hook(d):
    global cancel_download, download_phase
    if cancel_download:
        raise Exception("İndirme kullanıcı tarafından iptal edildi.")

    if d['status']=='downloading':
        total=d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded=d.get('downloaded_bytes',0)

        if total>0:
            part_percent=downloaded/total
        elif d.get('fragment_count'):
            part_percent=d.get('fragment_index', 0) / d.get('fragment_count', 1)
        else:
            part_percent=0

        if download_phase==1:
            overall_percent=part_percent*0.80
            status_text="Video akışı indiriliyor..."
        else:
            overall_percent=0.80+(part_percent*0.15)
            status_text="Ses akışı indiriliyor..."

        app.after(0, lambda p=overall_percent: progress_bar.set(p))
        app.after(0, lambda p=overall_percent: progress_label.configure(text=f"%{int(p*100)}"))
        app.after(0, lambda: status_label.configure(text="İndiriliyor...",text_color="yellow"))

    elif d['status']=='finished':
        if download_phase==1:
            download_phase=2
        else:
            app.after(0, lambda: progress_bar.set(0.95))
            app.after(0, lambda: progress_label.configure(text="%95"))
            app.after(0, lambda: status_label.configure(text="FFmpeg ile işleniyor ve birleştiriliyor...", text_color="cyan"))

def fetch_title(url):
    try:
        opts={
            'quiet':True,
            'no_warnings':True,
            'no_color':True,
            'noplaylist':True,
            'skip_download':True,
            'extract_flat':'in_playlist',
            'socket_timeout':10,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(url, download=False)
            title=info.get('title', 'Bilimeyen Video')
        app.after(0, lambda : video_title_label.configure(text=f"{title}"))
    except Exception:
        app.after(0, lambda:video_title_label.configure(text="Video Başlığı Alınamadı."))

def on_url_change(event=None):
    url=url_entry.get().strip()
    if url.startswith("http"):
        video_title_label.configure(text="Başlık Alınıyor...")
        threading.Thread(target=fetch_title, args=(url,), daemon=True).start()

def download_video(url,format_choice):

    downloads_path=os.path.join(os.path.expanduser('~'),'Downloads')
    
    settings={
        'outtmpl':os.path.join(downloads_path, '%(title)s.%(ext)s'), #indirilen videonun adını yt üzerindeki başlığı ve uzantısı olacak şekilde yapar
        'noplaylist':True,       #linki bir çalma listesinde veya mixte ise diğer videoları yoksayıp linke odaklanır.
        'extract_flat':'discard_in_playlist',
        'no_color':True,
        'quiet':True,
        'no_warnings':True,
        'progress_hooks':[progress_hook],
        'socket_timeout':15,

    }

    if format_choice=='mp3':
        settings['format']='bestaudio/best'
        settings['postprocessors']=[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }]
    else:
        settings['format']='bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        settings['merge_output_format']='mp4'

    try:
        with yt_dlp.YoutubeDL(settings) as ydl:
            ydl.download([url])
        app.after(0, lambda: status_label.configure(text="İndirme Başarıyla Tamamlandı! ",text_color="#00FF66"))
        app.after(0, lambda: progress_bar.set(1.0))
        app.after(0, lambda: progress_label.configure(text="%100"))
    except Exception as e:
        error_msg=str(e)
        if "iptal edildi" in str(e):
            app.after(0, lambda: status_label.configure(text="İndirme iptal edildi.", text_color="orange"))
            app.after(0, lambda: progress_bar.set(0))
            app.after(0, lambda: progress_label.configure(text="%0"))
        else:
            app.after(0, lambda msg=error_msg: status_label.configure(text=f"Bir Hata Oluştu: {msg[:30]}", text_color="red"))
    finally:
        app.after(0, lambda: download_button.configure(state="normal"))
        app.after(0, lambda: cancel_button.pack_forget())

#Arayüz
app=ctk.CTk()
app.title("Media Downloader")
app.geometry("580x450")
app.resizable(False,False)

#Başlık
title_label=ctk.CTkLabel(app, text="Social Media Video & MP3 Downloader", font=("Arial",20,"bold"))
title_label.pack(pady=(30,20))

#Link girişi
url_entry=ctk.CTkEntry(app, width=480, height=40, placeholder_text="Video linkini buraya yapıştırın (YouTube, X(Twitter), Instagram ...)")
url_entry.pack(pady=10)

url_entry.bind("<Return>", on_url_change)
url_entry.bind("<<Paste>>", lambda e:app.after(100, on_url_change))

#video başlığı
video_title_label=ctk.CTkLabel(app, text="", font=("Arial", 12, "bold"), text_color="#1E90FF",wraplength=500)
video_title_label.pack(pady=(0,5))

#Format seçimi
format_option=ctk.CTkOptionMenu(app, values=["MP4", "MP3"], width=120, height=35)
format_option.pack(pady=15)

#indirme butonu
button_frame=ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=10)

download_button=ctk.CTkButton(button_frame, text="İndirmeyi başlat", command=start_download_thread, width=220, height=40, font=("Arial", 14, "bold"))
download_button.pack(side="left", padx=10)

#iptal butonu
cancel_button=ctk.CTkButton(button_frame, text="İptal Et", command=cancel_download_action, width=120,height=38, font=("Arial",13, "bold"))

#ilerleme çubuğu
progress_bar=ctk.CTkProgressBar(app, width=440, height=12)
progress_bar.set(0)     

progress_label=ctk.CTkLabel(app, text="%0", font=("Arial",11,"bold"))

#Durum bilgisi
status_label=ctk.CTkLabel(app, text="",font=("Arial", 13))
status_label.pack(pady=5)

#kişisel imzam //ATORNFPS
footer_label=ctk.CTkLabel(app, text="Made by atornfps", font=("Arial", 13, "italic"), text_color="gray50")
footer_label.pack(side="bottom", pady=10)

app.mainloop()
        
