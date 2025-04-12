import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

def get_available_formats():
    video_url = url_entry.get()
    if not video_url:
        update_status("Error: No video URL provided!", "red")
        return
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'listformats': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = [f"{f['format_id']} - {f['format_note']}" for f in info.get('formats', []) if 'format_id' in f]
            quality_dropdown['values'] = formats if formats else ["best"]
            quality_var.set(formats[0] if formats else "best")
            update_status("Formats loaded!", "green")
    except Exception as e:
        update_status(f"Error: {e}", "red")

def download_video():
    download_media(video=True)

def download_audio():
    download_media(video=False)

def download_media(video=True):
    video_url = url_entry.get()
    file_path = path_label.cget("text")
    selected_quality = quality_var.get().split(' - ')[0]
    
    if not video_url:
        update_status("Error: No video URL provided!", "red")
        return
    
    if not file_path:
        update_status("Error: No download path selected!", "red")
        return
    
    ydl_opts = {
        'outtmpl': os.path.join(file_path, '%(title)s.%(ext)s'),
        'format': selected_quality if video else 'bestaudio/best',
        'progress_hooks': [progress_hook]
    }
    
    if not video:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_opts['ffmpeg_location'] = r'C:\ffmpeg'
    
    update_status("Downloading...", "blue")
    progress_bar['value'] = 0
    progress_label.config(text="0%")
    root.update_idletasks()
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        update_status("Download Completed!", "green")
    except Exception as e:
        update_status(f"Error: {e}", "red")

def get_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)

def update_status(message, color):
    status_label.config(text=message, fg=color)

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', 1)
        progress_percent = (downloaded_bytes / total_bytes) * 100
        progress_bar['value'] = progress_percent
        progress_label.config(text=f"{progress_percent:.2f}%")
        root.update_idletasks()

# Default download folder (Downloads directory)
default_path = str(Path.home() / "Downloads")

# Tkinter GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x500")

tk.Label(root, text="YouTube Downloader", fg='blue', font=("Arial", 20)).pack(pady=10)

tk.Label(root, text="Enter Video URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

fetch_formats_btn = tk.Button(root, text="Get Available Formats", command=get_available_formats)
fetch_formats_btn.pack(pady=5)

path_label = tk.Label(root, text=default_path)
path_label.pack()
tk.Button(root, text="Select Folder", command=get_path).pack(pady=5)

tk.Label(root, text="Select Quality:").pack()
quality_var = tk.StringVar(value="best")
quality_dropdown = ttk.Combobox(root, textvariable=quality_var)
quality_dropdown.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=5)
progress_label = tk.Label(root, text="0%")
progress_label.pack()

tk.Button(root, text="Download Video", command=download_video).pack(pady=5)
tk.Button(root, text="Download Audio", command=download_audio).pack(pady=5)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=10)

root.mainloop()
