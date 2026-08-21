# AreaPersonale

A personal desktop dashboard built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). It brings together five everyday tools — a video downloader, a writing assistant, a file manager, an mp4 → mp3 converter and a notes app — behind a single dark-themed sidebar UI.

This is a personal/learning project and my first public repo, so expect some rough edges.

## Features

### Video Downloader
- Download videos via [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- Queue several links with the **add** button before starting
- Choose between best quality MP4 and 720p
- Live download log streamed straight into the UI (`stdout`/`stderr` are redirected to the textbox)
- Saves files to your `Downloads` folder

### Essay Helper (word counter + AI tools)
- Character and word count on demand
- Most-common-words breakdown, with English and Italian stopwords filtered out
- AI **grammar fix** — corrects typos and grammar without touching style or tone
- AI **reformat** — cleans up paragraph structure and phrasing
- AI **change words num** — type a target in the small entry and the text is expanded or trimmed to roughly that word count while preserving meaning
- All AI features run on the Google **Gemini API**

### File Manager
- Three fixed categories — **school**, **personal**, **other** — backed by the `School/`, `Personal/` and `Other/` folders next to the script (created automatically on first run)
- Search by filename and filter by extension at the same time
- **+** moves the files you pick into the selected category
- **open** launches a file with its default application, **open directory** opens the category folder
- **double-click** a *delete* button to send that file to the Recycle Bin (single clicks do nothing, on purpose)
- Faster than the Windows file manager for scanning and opening personal documents

### mp4 → mp3
- Pick any number of `.mp4` files and extract their audio via [`moviepy`](https://pypi.org/project/moviepy/)
- Choose the output folder with **Browse...** (defaults to `Downloads`)
- **Clear All** empties the queue; conversion runs on a background thread so the UI stays responsive

### Notes
- Notes are stored in `notes.json` next to the script and grouped by day
- Each note has a title, a short content and a longer description
- Live search across title, content, description and date as you type
- **AI fill** completes only the fields you left empty, inferring them from the ones you filled in
- Open a note to edit or delete it

## Requirements

### CustomTkinter — important

The UI **does not run on stock CustomTkinter 5.2.2**. It relies on APIs that only exist in a patched build:

- `customtkinter.register_project_fonts(root, fonts_dir)` — loads the bundled `.ttf` files at runtime
- `CTkLabel(..., font_wrap=..., full_circle=..., unified_bind=...)`
- `CTkButton(..., pressed_color=...)`

On an unmodified install, `register_project_fonts` raises `AttributeError` and the extra keyword arguments raise `ValueError` from CustomTkinter's own argument check, so the window never opens. If you want to run this, you need the same patched CustomTkinter — a plain `pip install customtkinter` is not enough.

### Everything else

- **Python 3.12+** — the AI prompts use nested quotes inside f-strings ([PEP 701](https://peps.python.org/pep-0701/)), which is a syntax error on 3.11 and below
- A Google Gemini API key ([get one here](https://ai.google.dev/))
- **ffmpeg** on your `PATH` — `yt-dlp` needs it to merge the separate best-quality video and audio streams; without it downloads fall back to the single-file MP4. The mp4 → mp3 converter does not need it, since `moviepy` ships its own binary through `imageio-ffmpeg`.

## Tech Stack

- Python 3.12+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (patched — see above) for the UI
- [Pillow](https://pypi.org/project/pillow/) for the sidebar icons
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloads
- [google-genai](https://pypi.org/project/google-genai/) for the AI text tools (Gemini)
- [moviepy](https://pypi.org/project/moviepy/) for audio extraction
- [Send2Trash](https://pypi.org/project/Send2Trash/) so deleted files land in the Recycle Bin

## Installation

```bash
git clone https://github.com/albertocammilli/Area-Personale.git
```

```bash
cd Area-Personale
```

```bash
pip install customtkinter pillow yt-dlp google-genai moviepy send2trash
```

Then replace the installed CustomTkinter with the patched build (see [Requirements](#customtkinter--important)).

### Configuration

The Gemini client reads your API key from the environment:

```bash
setx GEMINI_API_KEY "your-api-key-here"
```

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Use `setx` on Windows and `export` on macOS/Linux. `gemini_api.py` calls `gemini-3.1-flash-lite` with the URL-context tool enabled, so notes and prompts containing links can be looked up before an answer is generated.

### Running the app

The filename contains a space, so quote it:

```bash
python "Area personale.py"
```

Heavier libraries (`yt-dlp`, `moviepy`, the Gemini client) load in a background thread on startup, so the window appears quickly even before those features are ready to use. The sidebar icons load in a second background thread.

## Project Structure

```
.
├── Area personale.py    # Main app: window, sidebar, and one class per tool
├── gemini_api.py        # Thin wrapper around the Gemini API for AI text features
├── notes.json           # Notes database (created/updated by the Notes tool)
├── assets/
│   ├── fonts/           # Century Gothic + Tahoma, registered at startup
│   └── images/          # Sidebar icons
├── School/              # File Manager categories, created on first run
├── Personal/
└── Other/
```

## UI layout

The whole interface is built with `.grid()` and expands with the window. The root window uses two weighted columns (sidebar and main area) and one weighted row, each tool frame stretches into the main area with `sticky="nsew"`, and switching tools is done with `grid()` / `grid_remove()`. The main frame has `grid_propagate(False)` so a tool's content can never push the sidebar out of shape.

## Known limitations

- Adding files in the File Manager **moves** them with `Path.rename`, which fails across different drives on Windows
- Pick a category before using the File Manager buttons — **+** silently does nothing and **open directory** raises until one is selected
- The Video Downloader takes over `sys.stdout` and `sys.stderr` for the whole app, so any `print` from another tool ends up in its download log
- The window has no minimum size, so shrinking it far enough compresses the layout and clips labels
- Several AI handlers swallow exceptions with a bare `except`, so a failed request can leave a button stuck on its "…" label
- API errors surface as a Tkinter message box


