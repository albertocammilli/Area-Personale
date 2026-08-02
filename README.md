# AreaPersonale

A personal desktop dashboard built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). It brings together a few everyday tools — a YouTube downloader, a writing assistant, and (soon) a file manager, notes, and a task manager — behind a single dark-themed sidebar UI.

This is a personal/learning project and my first public repo, so expect some rough edges.

## Features

### ✅ YouTube Downloader
- Download videos via [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- Add multiple links at once
- Choose between best quality MP4 or 720p
- Live download log streamed straight into the UI
- Saves files to your `Downloads` folder

### ✅ Essay Helper (Word Counter + AI tools)
- Live character and word count
- Most-common-words breakdown, with English and Italian stopwords filtered out
- AI-powered **grammar fix** — corrects typos and grammar without touching style or tone
- AI-powered **reformat** — cleans up paragraph structure and phrasing
- AI-powered **word count adjuster** — expand or trim a text to hit a target word count while preserving meaning
- All AI features are powered by the Google **Gemini API**

### 🚧 In progress
- **File Manager** — search bar, category filters, and tags are in place, but the underlying logic isn't wired up yet
- **mp4 → mp3** — planned, not yet implemented
- **Notes** — planned, not yet implemented
- **Task Manager** — planned, not yet implemented

## Tech Stack

- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the UI
- [Pillow](https://pypi.org/project/pillow/) for image handling
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloads
- [google-genai](https://pypi.org/project/google-genai/) for AI text tools (Gemini)

## Getting Started

### Prerequisites
- Python 3.10+
- A Google Gemini API key ([get one here](https://ai.google.dev/))
- Google Chrome installed (used by `yt-dlp` to read cookies for downloads)

### Installation

```bash
git clone https://github.com/your-username/area-personale.git
cd area-personale
pip install customtkinter pillow yt-dlp google-genai
```

### Configuration

The app reads your Gemini API key from an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"   # macOS/Linux
setx GEMINI_API_KEY "your-api-key-here"     # Windows
```

### Running the app

```bash
python Area_personale.py
```

Heavier libraries (`yt-dlp`, the Gemini client) load in a background thread on startup, so the window appears quickly even before those features are ready to use.

## Project Structure

```
.
├── Area_personale.py   # Main app: UI, navigation, and all feature classes
├── gemini_api.py        # Thin wrapper around the Gemini API for AI text features
└── assets/              # Fonts and icons used by the UI
```

## Notes

- The UI text is currently in a mix of Italian and English — this is a personal tool first, so localization hasn't been cleaned up.
- Error handling for the AI features shows a Tkinter message box on API failures.

## License

Not yet decided — feel free to open an issue if you'd like to use this and need a license added.
