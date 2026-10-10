# Media Downloader

A modern, fast, and multi-threaded desktop application built with python for downloading videos and extracting audio from YouTube and various social media platforms.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![UI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)

---

## Key Features

* **Instant Metadata Extraction:** Automatically fetches and displays the video title in real-time as soon as a valid link is pasted or entered.
* **Multi-Format Support:** Download videos in high-definition **MP4** or convert audio directly to **192 kbps MP3**.
* **Non-Blocking Multi-Threaded Architecture:** Network operations (`yt-dlp`) run on seperate threads using Python's `threading` module to keep GUI fluid and responsive at all times.
* **Cancellation Support:** Allows users to terminate ongoing download processes gracefully.
* **Cross-Platform Compability:** Works seamlessly across Windows, macOS and Linux.

---

## Tech Stack & Dependencies
* **Language:** Python 3.x
* **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern extension of Tkinter)
* **Download Engine:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Advanced YouTube & video platform downloader)
* **Media Processing:** [FFmpeg](https://ffmpeg.org/) (Required for post-processing and merging video/audio streams)

---

## Architecture & Engineering Highlights

1. **Thread-Safe GUI Updates(`app.after`):**
To prevent GUI freeze and thread-race conditions during asynchronous network tasks, all UI element modifications are safely dispatched to the main event loop via `app.after()`.

2. **Adaptive Stream Handling:**
YouTube serves high-definition streams seperately (video and audio tracks). The application handles dynamic format selection (`bestvideo+bestaudio`) and merges them post-downloading using FFmpeg pipeline processors.

3. **Event Binding for UX Optimization:**
The URL input field utilizes `<Return>` and `<<Paste>>` event listeners to asynchronously trigger metadata parsing without requiring manual user button clicks.

---

## Installation & Setup

### Prerequisites

Ensure you have Python installed and **FFmpeg** added to your system's PATH environment variable.

1. **Clone the Repository:**
```bash
   git clone https://github.com/atornfps/Social-Media-Video-MP3-Downloader.git
   cd Social-Media-Video-MP3-Downloader
   ```

2. **Install Required Libraries:**
```bash
   pip install customtkinter yt-dlp
   ```

3. **Run The Application:**
```bash
python main.py
```

---

## Versioning & Roadmap

- **v1.0.0 (Current):**
    - Stable UI implementation using CustonTkinter
    - Non-blocking milti-threaded download engine & cancellation handler.
    - Real-time video title fetching via event bindings (`<Return>` and `<<Paste>>`).
    - Dynamic 2-phase progress bar integration for YouTube adaptive streams (Video + Audio).
- **v1.0.1 (Patch Release - Standalone Executable):**
    - Standalone `.exe` binary generation & desktop shortcut deployment via PyInstaller.
    - Custom application icon (`.ico`) integration
- **v1.1.0 (Planned Future Update):**
    - Multi-language support (Turkish & English UI toggle).
    - Custom download destination directory selection via folder picker dialog.
    - Indeterminate progress for files with unkown total size.
    - Granular progress tracking for fragmented HLS/m3u8 live streams.
- **v1.2.0 (Advenced Features & Media Formats):**
    - Extended audio/video format options (MP3, WAV, MP4, WEBM, etc.).
    - Batch and playlist download support.
    - Video resolution & quality seleciton menu (1080p, 720p, 480p, etc.).
- **v2.0.0 (Major Vision):**
    - Porting the application into a full-fledged Chrome/Firefox Browser Extension.

---

## Author

Developed by **Melik Uğur Karakaya** ([@atornfps](https://github.com/atornfps))

