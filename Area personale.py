import customtkinter as ctk
from customtkinter import CTkFrame, CTkTextbox
from tkinter import filedialog
from PIL import Image
import threading
from pathlib import Path
import sys
import string
import os

ytd = None
get_response_ai = None
gemini_api = None


class YtDownloader:
    def __init__(self, parent):
        self.frame = CTkFrame(parent,
                              fg_color="#1e1e1e",
                              corner_radius=6)

        self.start = ctk.CTkButton(self.frame,
                                   text="start",
                                   font=("Roboto", 12),
                                   corner_radius=10,
                                   command=self.thread_make)
        self.insert = ctk.CTkLabel(self.frame,
                                   text="Paste your link here. You can add more than one",
                                   font=ctk.CTkFont(family='Tahoma', size=15, weight="normal", slant="roman"))
        self.options = ctk.CTkComboBox(self.frame,
                                       values=["MP4 Video (Best Quality)", "MP4 Video (Low Quality, 720p)"],
                                       width=200)
        self.text_box = ctk.CTkTextbox(self.frame,
                                       height=150,
                                       width=400,
                                       fg_color="#1b1b1b")
        self.input = ctk.CTkTextbox(self.frame,
                                    height=20,
                                    border_color="#808080",
                                    border_width=1)
        self.add = ctk.CTkButton(self.frame,
                                 text="add",
                                 corner_radius=7,
                                 fg_color="orange",
                                 width=40,
                                 hover_color="#8B4000",
                                 command=self.add)
        self.add.place(relx=0.72, rely=0.25, anchor="center")
        self.options.place(relx=0.5, rely=0.35, anchor="center")
        self.start.place(relx=0.5, rely=0.45, anchor="center")
        self.input.place(relx=0.5, rely=0.25, anchor="center")
        self.insert.place(relx=0.5, rely=0.15, anchor="center")
        self.text_box.place(relx=0.5, rely=0.75, anchor="center")

        # code variables
        self.quality = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
        self.link = []
        self.link_count = 1
        sys.stdout = self
        sys.stderr = self

    def add(self):
        self.link.append(self.input.get(1.0, "end"))
        print(f"{self.link_count}) {self.link[-1]}")
        if self.link_count > 1:
            self.start.configure(text="Download videos!")
        self.input.delete(1.0, "end")
        self.link_count += 1

    # write from terminal to ui
    def write(self, string):
        self.text_box.insert("end", string)
        self.text_box.see("end")

    def flush(self):
        pass

    # ion remember how dis work
    # creating the thread
    def thread_make(self):
        self.start.configure(fg_color="gray", hover_color="gray", command=None)
        self.download_thread = threading.Thread(target=self.download_video, daemon=True)
        self.download_thread.start()

    # this one is called by the thread
    def download_video(self):
        self.link.append(self.input.get("1.0", "end"))
        if self.options.get() == "MP4 Video (Best Quality)":
            self.quality = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
        elif self.options.get() == "MP4 Video (Low Quality, 720p)":
            self.quality = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
        settings = {"format": self.quality,
                    "outtmpl": os.path.expanduser("~/Downloads/%(title)s.%(ext)s"),
                    "concurrent_fragment_downloads": 4,
                    "cookiesfrombrowser": ("chrome",)}
        if self.input.get(1.0, "end") == "\n":
            pass
        else:
            self.link.append(self.input.get(1.0, "end"))
        with ytd.YoutubeDL(settings) as ydl:
            ydl.download(self.link)

    # show/hide ui
    def show(self):
        self.frame.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)

    def hide(self):
        self.frame.place_forget()


class WordCounter:
    def __init__(self, parent):
        self.frame = CTkFrame(
            parent,
            fg_color="#1e1e1e",
            corner_radius=6
        )

        # logic variables
        self.characters = "-"
        self.words = "-"
        self.common_words = {}
        self.stop_words = {'stai', "i'd", 'y', 'avessimo', 'avuti', "it'd", 'facevi', 'over', 'le', 'before',
                           'those', 'col', 'starete', 'dov', 'saranno', 'tuoi', 'sarete', "weren't", 'farai',
                           'avesse', 'avuto', 'farete', 'mustn', 'some', 'stanno', 'sugl', 'ero', 'farei', 'suo',
                           'era', 'fosse', 'where', "he'd", 'dall', 'facessero', 'haven', 'all', 'fummo',
                           'faremo', 'anche', 'avrei', 'how', 'facesti', 'più', 'stava', 'herself', 'it', 'no',
                           'their', 'cui', 'contro', 'di', 'su', 'mie', 'fai', 'doing', 'your', 'vostro',
                           'quanta', 'facciano', 'stando', 'up', 'after', "i'm", 'ai', 'stessimo', 'mightn',
                           'c', 'abbiano', 'perché', 'fossimo', 'into', 'io', 'sull', 'between', 'avrà', 'se',
                           'sta', 'then', 'than', 'of', 'am', 'about', 'faceva', 'wouldn', 'its', 'alla',
                           'dagli', 'il', 'aveva', 'starebbero', 'ours', 'queste', 'tutto', 'stetti', 'this',
                           'saremmo', 'avevi', 'such', 'essendo', 'vostri', 'through', 'a', 'faccio', 'coi',
                           'avrai', 'they', 'was', 'couldn', 'from', 'are', 'facciate', 'dai', 'sue', "shan't",
                           "won't", 'quanti', 'hadn', 'few', "shouldn't", 'myself', 'lui', 'facevo', "she'll",
                           'avremo', 'avrete', 'ti', 'siano', 'stessero', 'uno', 'yours', 'eravate', 'his',
                           'eri', "aren't", 'staresti', 'i', "you'll", 'at', "they've", 'too', 'quelle', 'mia',
                           'sugli', 'lo', 'quale', 'stiate', 'm', 'shan', 'each', 'our', 'sarebbe', 'why', 'starò',
                           'per', 'stiamo', 'siate', 'ci', "i'll", 'dei', "that'll", 'can', 'hers', 'sarai',
                           "didn't", 'stavi', 'avute', 'only', 'saresti', 'degli', 'facciamo', 'sarebbero',
                           'ed', 'sarò', 'needn', 'weren', "she'd", 'o', 'fossi', 'quante', 'fareste',
                           'vostre', 'as', 'stia', 'sto', 'do', 'faccia', "it'll", 'quelli', 'nor', 'faresti',
                           'starà', 'miei', 'tuo', 'fosti', 'fossero', 'my', 'nostri', 'avrebbe', 'in',
                           'faceste', 'd', 'to', "we'd", 'these', 'other', 'avremmo', 'will', 'avuta',
                           'steste', 'stavo', 'sei', 'll', 'non', 'further', 's', 'tua', 'fui', 'eravamo',
                           'feci', 'starei', 'having', 'that', "we're", 'siamo', 'avranno', 'against',
                           'stesti', 'been', 'starebbe', 'stavamo', "we've", 'avevo', 'himself', 'here',
                           'ad', 'nelle', 'ho', 'out', "they're", 'gli', 'tu', 'dove', 'erano', 'is',
                           'delle', 'didn', "they'd", "he's", "i've", 'isn', 'yourselves', 'stemmo',
                           'won', 'avevano', 'loro', 'facessimo', 'stareste', 'quanto', 'yourself',
                           'avesti', 've', 'negli', 'once', 'chi', 'sono', 'da', 'sullo', 'li', 'hasn',
                           'fece', 'because', 'ha', 'fanno', 'she', 'nell', 'off', "mustn't", 'come',
                           'faranno', 'sulle', 'so', 'nostro', 'abbiate', 'avrebbero', 'did', "she's",
                           'abbiamo', 'ebbero', 'stavano', 'farò', 'foste', 'on', "mightn't", 'again',
                           'me', 't', 'è', 'avessi', 'for', 'stette', 'al', 'any', 'dal', 'nei', "you're",
                           'suoi', 'avrò', 'sarei', 'stessi', 'questo', "you'd", 'stettero', 'same',
                           'nella', "he'll", 'fecero', 'siete', 'sua', "wouldn't", 'ne', 'una', 'with',
                           'facendo', 'down', 'under', 'itself', 'above', 'not', 'most', 'starai', 'have',
                           'facesse', 'should', 'and', 'them', "they'll", 'we', "should've", 'dalla', 'voi',
                           'stavate', 'vostra', 'more', 'noi', 'aren', 'you', 'questi', 'whom', 'fu',
                           "hadn't", 'avete', "couldn't", 'faremmo', 'does', "doesn't", 'when', 'while',
                           'staremo', 're', 'or', 'ain', 'hanno', 'avemmo', 'avendo', 'saremo', 'stiano',
                           'were', "hasn't", 'shouldn', 'facessi', 'alle', 'farebbe', 'sia', 'staranno',
                           'theirs', 'dalle', 'facevano', 'themselves', 'farebbero', 'below', 'sulla',
                           'by', 'avevamo', 'her', 'negl', 'che', 'doesn', 'della', 'ebbe', 'very', 'who',
                           'ma', "needn't", 'dell', 'facevate', 'don', 'just', 'e', 'con', 'avevate',
                           'during', 'an', 'own', 'the', 'quella', 'ourselves', 'nostre', 'ebbi',
                           'facevamo', "haven't", 'avessero', 'l', 'what', 'allo', 'nel', 'if', 'but',
                           'sarà', 'sul', 'vi', 'stesse', 'furono', 'both', "we'll", 'now', 'del',
                           'avreste', 'facemmo', 'wasn', 'he', 'nello', 'dagl', 'aveste', 'sareste',
                           'tue', 'avresti', 'be', 'mio', 'quello', 'hai', 'there', "don't", 'has',
                           'which', 'dallo', 'la', 'agli', 'agl', "you've", 'farà', 'sui', 'staremmo',
                           "isn't", 'mi', 'dello', 'tra', 'questa', 'being', "it's", 'nostra', "wasn't",
                           'si', 'abbia', 'him', 'degl', 'lei', 'tutti', 'until', 'un', 'had'}

        # Text container
        self.text_container = CTkTextbox(
            self.frame,
            fg_color="#1b1b1b",
            width=380,
            height=330
        )
        self.text_container.place(
            relx=0.33,
            rely=0.45,
            anchor="center"
        )

        # Count label
        self.count_textbox = ctk.CTkTextbox(
            self.frame,
            font=ctk.CTkFont(
                family='Tahoma',
                size=17,
                weight="bold",
                slant="roman"
            ), fg_color="#1b1b1b",
            width=197,
            height=100
        )
        self.count_textbox.place(
            relx=0.67,
            rely=0.025,
            anchor="nw",
        )
        self.count_textbox.insert("1.0", f"STATS:\n\nCharacters: {self.characters}\nWords: {self.words}")

        # Count button
        self.count_button = ctk.CTkButton(
            self.frame,
            text="count!",
            fg_color="#E3A600",
            hover_color="#FFCC00",
            pressed_color="#E38800",
            font=ctk.CTkFont(
                family='Tahoma',
                size=15,
                weight="bold",
                slant="roman"
            ),
            width=380,
            command=lambda: self.count(self.text_container.get("1.0", "end-1c"))
        )
        self.count_button.place(
            relx=0.33,
            rely=0.935,
            anchor="center"
        )

        self.common_words_textbox = ctk.CTkTextbox(
            self.frame,
            fg_color="#1b1b1b",
            width=197,
            height=160,
            font=ctk.CTkFont(
                family='Tahoma',
                size=14,
            )
        )
        self.common_words_textbox.place(
            relx=0.67,
            rely=0.298,
            anchor="nw"
        )

        self.grammar_fix_button = ctk.CTkButton(
            self.frame,
            text="grammar fix",
            fg_color="#1E90FF",
            hover_color="#63B8FF",
            font=ctk.CTkFont(
                family='Tahoma',
                size=15,
                weight="normal",
                slant="roman",
            ),
            width=197,
            height=28,
            command=lambda: self.grammar_fix_thread()
        )
        self.grammar_fix_button.place(
            relx=0.67,
            rely=0.815,
            anchor="nw"
        )

        # Reformat button
        self.reformat_button = ctk.CTkButton(
            self.frame,
            text="reformat",
            fg_color="#2ECC71",
            hover_color="#58D68D",
            font=ctk.CTkFont(
                family='Tahoma',
                size=15,
                weight="normal",
                slant="roman"
            ),
            width=197,
            height=28,
            command=lambda: self.reformat_thread()
        )
        self.reformat_button.place(
            relx=0.67,
            rely=0.9,
            anchor="nw"
        )

        # word count match button
        self.change_word_count_button = ctk.CTkButton(
            self.frame,
            text="change words num",
            fg_color="#F5512C",
            hover_color="#F7622C",
            font=ctk.CTkFont(
                family='Tahoma',
                size=15,
                weight="normal",
                slant="roman",
            ),
            width=140,
            height=28,
            command=lambda: self.change_words_number_thread())

        self.change_word_count_button.place(
            relx=0.67,
            rely=0.73,
            anchor="nw"
        )

        self.change_words_entry = ctk.CTkEntry(
            self.frame,
            width=52,
            height=30,
            placeholder_text="num...",
            font=ctk.CTkFont(
                family='Tahoma',
                size=15,
                weight="normal",
                slant="roman",
            ),
        )
        self.change_words_entry.place(
            relx=0.912,
            rely=0.73,
            anchor="nw"
        )

    def count(self, text):
        self.common_words = {}
        self.common_words_textbox.delete(1.0, "end")
        self.count_textbox.configure(state="normal")
        self.characters = len(text)
        self.words = len(text.split())
        self.count_textbox.delete("0.0", "end")
        self.count_textbox.insert("1.0", f"STATS:\n\nCharacters: {self.characters}\nWords: {self.words}")
        self.count_textbox.configure(state="disabled")

        no_punctuation_text = "".join(carattere for carattere in text if carattere not in string.punctuation)

        for word in no_punctuation_text.split():
            if word not in self.stop_words:
                self.common_words[word] = self.common_words.get(word, 0) + 1
        self.common_words = sorted(self.common_words.items(), key=lambda x: x[1], reverse=False)
        for key, value in self.common_words:
            self.common_words_textbox.insert("1.0", f"{key}: {value}\n")

    # grammar fix here
    def grammar_fix_thread(self):
        if self.text_container.get("1.0", "end-1c") != "":
            self.grammar_fix_button.configure(text="grammar fix...", state="disabled")
            threading.Thread(target=self.grammar_fix, daemon=True).start()

    def grammar_fix(self):
        try:
            output = gemini_api.get_response_ai(f"text: {self.text_container.get("1.0", "end-1c")}",
                                                "Il tuo unico compito è correggere errori di battitura e grammaticali nel testo delimitato da <testo></testo>. OUTPUT: restituisci ESCLUSIVAMENTE il testo corretto. Nessun'altra parola. - Niente introduzioni  - Niente commenti, note o spiegazioni. - Niente markdown, virgolette o tag attorno al testo in output. - Se il testo è già corretto, restituiscilo identico, senza aggiungere nulla. REGOLE DI CORREZIONE: - Correggi solo errori oggettivi: ortografia, concordanze, punteggiatura. - Non modificare stile, tono, lessico o struttura delle frasi. - Non aggiungere, rimuovere o unire paragrafi, a capo o spaziatura rispetto all'originale. ",
                                                parent_widget=self.frame
                                                )
            self.update_textbox(output)
        except:
            pass

    # reformat here
    def reformat_thread(self):
        if self.text_container.get("1.0", "end-1c") != "":
            self.reformat_button.configure(text="reformat...", state="disabled")
            threading.Thread(target=self.reformat, daemon=True).start()

    def reformat(self):
        try:
            output = gemini_api.get_response_ai(f"text: {self.text_container.get("1.0", "end-1c")}",
                                                "restituisci SOLO il seguente testo diviso in paragrafi chiari (se la lunghezza lo richiede) e riformulando le parti che lo richiedono in una forma più efficace(solo se necessario, se la scrittura non è affatto solida, altrimenti lascia così com'è) evita ### e **. mantieni ovviamente la lingua originale")
            self.update_textbox(output)
        except:
            pass

    # words number change here
    def change_words_number_thread(self):
        if self.text_container.get("1.0", "end-1c") != "":
            self.change_word_count_button.configure(text="change word num...", state="disabled")
            threading.Thread(target=self.change_words_number, daemon=True).start()

    def change_words_number(self):
        self.count(self.text_container.get("1.0", "end-1c"))
        try:
            if self.change_words_entry.get() != "":
                if int(self.change_words_entry.get()) < int(self.words):
                    output = gemini_api.get_response_ai(f"text: {self.text_container.get("1.0", "end-1c")}",
                                                        f"Your task is to adjust the word count of the text to approximately {self.change_words_entry.get()} words. (current length: {self.words} PRIORITY OF CHANGES (apply in this order): 1. First, remove redundant or unnecessary words/phrases without changing meaning or tone. 2. If that's not enough to reach the target, summarize or rephrase wordy sentences. 3. If the target is far from the current word count, rephrase and shrink more aggressively where needed, while preserving the core meaning. RULES: - Keep the writing style, tone and voice as close to the original as possible. - Do not add paragraphs or line breaks that weren't present in the original text. - Do not add new content, examples, or ideas not present in the original. - If no target word count is specified, return the original text unchanged. OUTPUT: return ONLY the resulting text. No comments, no explanations, no preamble, no notes about word count.")
                    self.update_textbox(output)
                elif int(self.change_words_entry.get()) > int(self.words):
                    output = gemini_api.get_response_ai(
                        f"text: {self.text_container.get("1.0", "end-1c")}",
                        f"Your task is to increase the word count of the text below to approximately {self.change_words_entry.get()} words. " f"The current text is approximately {len(self.text_container.get('1.0', 'end-1c').split())} words.\n\n" "PRIORITY OF CHANGES (apply in this order):\n" "1. First, elaborate on existing points with more detail, explanation, or context.\n" "2. If that's not enough, expand concise or compressed sentences into fuller, more descriptive ones.\n" "3. If the target is far above the current count, add more depth throughout while staying strictly within the scope of the original content.\n\n" "RULES:\n" "- Do not introduce new topics, facts, ideas, or examples that aren't implied by the original text.\n" "- Keep the writing style, tone and voice as close to the original as possible.\n" "- Do not add paragraphs or line breaks that weren't present in the original text.\n" "- If no target word count is specified, return the original text unchanged.\n\n" "OUTPUT: return ONLY the resulting text. No comments, no explanations, no preamble, no notes about word count.")
                    self.update_textbox(output)
                else:
                    pass
            else:
                self.update_textbox(self.text_container.get("1.0", "end-1c"))
                pass
        except:
            pass

    def update_textbox(self, text):
        self.text_container.delete("1.0", "end")
        self.text_container.insert("1.0", text)
        self.grammar_fix_button.configure(text="grammar fix", state="normal")
        self.reformat_button.configure(text="reformat", state="normal")
        self.change_word_count_button.configure(text="change word num", state="normal")
        self.count(self.text_container.get("1.0", "end-1c"))

    # show/hide ui
    def show(self):
        self.frame.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)

    def hide(self):
        self.frame.place_forget()


class FileManager:
    def __init__(self, parent):
        # path of the script
        self.script_dir = Path(__file__).parent

        #files
        self.files=[]

        # current directory
        self.current = None

        #extentions present
        self.extensions=set()

        #filtered files, temporary list
        self.filtered_files=[]

        self.path_cartella_personale = self.script_dir / "Personal"
        self.path_cartella_scuola = self.script_dir / "School"
        self.path_cartella_altro = self.script_dir / "Other"

        self.cartelle = (self.path_cartella_personale,
                         self.path_cartella_scuola,
                         self.path_cartella_altro)

        for cartella in self.cartelle:
            if cartella.exists():
                pass
            else:
                cartella.mkdir(parents=True, exist_ok=True)

        self.frame = CTkFrame(
            parent,
            fg_color="#1e1e1e",
            corner_radius=6
        )

        # searchbar
        self.searchbar = ctk.CTkEntry(self.frame,
                                      width=520,
                                      placeholder_text="search...",
                                      font=ctk.CTkFont(family='Tahoma', size=15, slant="italic"))
        self.searchbar.place(relx=0.45, rely=0.05, anchor="center")

        # search button
        self.search_button = ctk.CTkButton(
            self.frame,
            width=50,
            text="Search",
            font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),

        )
        self.search_button.place(relx=0.945, rely=0.05, anchor="center")

        # filters
        self.filter_options = ctk.CTkSegmentedButton(
            self.frame,
            values=["school", "personal", "other"],
            font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
            command=self.change_current
        )
        for btn in self.filter_options._buttons_dict.values():
            btn.configure(width=140)
        self.filter_options.place(relx=0.015, rely=0.15, anchor="nw")

        # tags
        self.tags_combobox = ctk.CTkComboBox(
            self.frame,
            values=["all"]+list(self.extensions),
            font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
            width=160,
            command=self.filter_files
        )
        self.tags_combobox.place(relx=1, rely=0.15, anchor="ne")
        self.tags_combobox.set("all")

        # add file/move
        self.add_button = ctk.CTkButton(self.frame,
                                        text="+",
                                        fg_color="lime",
                                        hover_color="green",
                                        width=40,
                                        height=40,
                                        font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                        command=self.select_file)

        self.add_button.place(relx=0.93, rely=0.87)

        #open directory button
        self.directory_button = ctk.CTkButton(self.frame,
                                        text="open directory",
                                        fg_color="#424242",
                                        hover_color="#616161",
                                        width=40,
                                        height=30,
                                        font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                        command=lambda: os.startfile(self.current))
        self.directory_button.place(relx=0.02, rely=0.87)

        #refresh
        self.refresh_button = ctk.CTkButton(self.frame,
                                              text="⟳",
                                              fg_color="#424242",
                                              hover_color="#616161",
                                              width=30,
                                              height=30,
                                              font=ctk.CTkFont(family="Tahoma", size=20, slant="roman"),
                                              command=lambda: self.show_files())

        self.refresh_button.place(relx=0.21, rely=0.87)

        # scrollable frame
        self.files_scrollable_frame = ctk.CTkScrollableFrame(self.frame,
                                                             width=560,
                                                             height=200)
        self.files_scrollable_frame.place(relx=0.51, rely=0.55, anchor="center")

        self.files_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.files_scrollable_frame.grid_rowconfigure(1, weight=0)

    def show_files(self):
        self.files.clear()
        for widget in self.files_scrollable_frame.winfo_children():
            widget.destroy()

        for i, file in enumerate(self.current.iterdir()):
            if file.is_file():
                label = ctk.CTkLabel(self.files_scrollable_frame, text=file.name, anchor="nw", height=20,
                                     font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"))
                label.grid(row=i, column=0, sticky="nw", pady=2, padx=5)
                button = ctk.CTkButton(self.files_scrollable_frame,
                                       text="open",
                                       fg_color="#b38600",
                                       hover_color="orange",
                                       width=40,
                                       height=20,
                                       font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                       command=lambda idx=i: self.open_file(idx, False)
                                       )
                button.grid(row=i, column=1, sticky="nw", pady=2, padx=5)
                self.files.append(file)
                self.extensions.add(file.suffix)
                print("f{self.files}\n\n")
        self.tags_combobox.configure(values=["all"]+list(self.extensions))



    def open_file(self, num, filtered):
        if not filtered:
            print(num)
            os.startfile(self.files[num])
        else:
            os.startfile(self.filtered_files[num])


    def change_current(self, value: str):
        if value == "school":
            self.current = self.path_cartella_scuola
        elif value == "personal":
            self.current = self.path_cartella_personale
        else:
            self.current = self.path_cartella_altro
        self.show_files()

    def select_file(self):
        if self.current is not None:
            file = Path(filedialog.askopenfilename(title="select a file"))
            destinazione = self.current / file.name
            file.rename(destinazione)
            self.files.append(file)
            self.show_files()
        else:
            pass


    def filter_files(self, value):
        if value=="all":
            self.show_files()
        else:
            self.filtered_files.clear()
            for file in self.files:
                if file.suffix == value:
                    self.filtered_files.append(file)
                    print(len(self.filtered_files))
            for widget in self.files_scrollable_frame.winfo_children():
                widget.destroy()

            for i, file in enumerate(self.filtered_files):

                    label = ctk.CTkLabel(self.files_scrollable_frame, text=file.name, anchor="nw", height=20,
                                         font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"))
                    label.grid(row=i, column=0, sticky="nw", pady=2, padx=5)
                    button = ctk.CTkButton(self.files_scrollable_frame,
                                           text="open",
                                           fg_color="#b38600",
                                           hover_color="orange",
                                           width=40,
                                           height=20,
                                           font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                           command=lambda idx=i: self.open_file(idx, True))
                    button.grid(row=i, column=1, sticky="nw", pady=2, padx=5)





    def show(self):
        self.frame.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)

    def hide(self):
        self.frame.place_forget()


class AreaPersonale(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.register_project_fonts(self, Path(__file__).resolve().parent / "assets" / "fonts")
        self.title("AreaPersonale")
        self.geometry("900x600")
        self.configure(fg_color="#0e0e0e")
        self.resizable(False, False)
        self._build_ui()
        threading.Thread(target=self._load_images_async, daemon=True).start()
        self.current = ""

        # starting program classes and showing
        self.yt = YtDownloader(self.main_frame)  # start program classes
        self.yt.hide()

        self.word = WordCounter(self.main_frame)
        self.word.hide()

        self.files = FileManager(self.main_frame)
        self.files.hide()

        # binding
        self.yt_downloader_card.bind("<Button-1>", lambda event: self.launch("youtube"))
        self.yt_downloader_label.bind("<Button-1>", lambda event: self.launch("youtube"))

        self.file_manager_card.bind("<Button-1>", lambda event: self.launch("filemanager"))
        self.file_manager_label.bind("<Button-1>", lambda event: self.launch("filemanager"))

        self.word_counter_card.bind("<Button-1>", lambda event: self.launch("wordcounter"))
        self.word_counter_label.bind("<Button-1>", lambda event: self.launch("wordcounter"))

        # hover
        self.make_widget_hover(self.yt_downloader_card, self.yt_downloader_label)
        self.make_widget_hover(self.file_manager_card, self.file_manager_label)
        self.make_widget_hover(self.word_counter_card, self.word_counter_label)
        self.make_widget_hover(self.mp4mp3_card, self.mp4mp3_label)
        self.make_widget_hover(self.notes_card, self.notes_label)
        self.make_widget_hover(self.task_manager_card, self.task_manager_label)

        self.program_map = {"youtube": self.yt, "wordcounter": self.word, "filemanager": self.files}

    # logic
    def launch(self, program):
        if self.current:
            self.current.hide()
        self.current = self.program_map[program]
        self.program_map[program].show()

    # hover
    def make_widget_hover(self, card, label):
        card.bind("<Enter>", lambda e: (card.configure(fg_color="#2e2e2e"), label.configure(fg_color="#2e2e2e")))
        card.bind("<Leave>", lambda e: (card.configure(fg_color="#1e1e1e"), label.configure(fg_color="#1e1e1e")))
        label.bind("<Enter>", lambda e: (card.configure(fg_color="#2e2e2e"), label.configure(fg_color="#2e2e2e")))
        label.bind("<Leave>", lambda e: (card.configure(fg_color="#1e1e1e"), label.configure(fg_color="#1e1e1e")))

    def _load_images_async(self):
        try:
            # Carica i file dal disco nel thread secondario
            img_yt = ctk.CTkImage(light_image=Image.open(
                Path(__file__).resolve().parent / "assets" / "images" / "hard-drive-download.png"),
                dark_image=Image.open(Path(
                    __file__).resolve().parent / "assets" / "images" / "hard-drive-download.png"),
                size=(18, 18))
            img_file = ctk.CTkImage(
                light_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "folder-check.png"),
                dark_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "folder-check.png"),
                size=(18, 18))
            img_word = ctk.CTkImage(
                light_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "file-type.png"),
                dark_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "file-type.png"),
                size=(18, 18))
            img_mp4mp3 = ctk.CTkImage(
                light_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "clapperboard.png"),
                dark_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "clapperboard.png"),
                size=(18, 18))
            img_notes = ctk.CTkImage(
                light_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "link.png"),
                dark_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "link.png"),
                size=(18, 18))
            img_task = ctk.CTkImage(
                light_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "cpu.png"),
                dark_image=Image.open(Path(__file__).resolve().parent / "assets" / "images" / "cpu.png"), size=(18, 18))

            # Assegna le immagini alle etichette in modo sicuro sul thread principale
            self.after(0, lambda: self.yt_downloader_label.configure(image=img_yt))
            self.after(0, lambda: self.file_manager_label.configure(image=img_file))
            self.after(0, lambda: self.word_counter_label.configure(image=img_word))
            self.after(0, lambda: self.mp4mp3_label.configure(image=img_mp4mp3))
            self.after(0, lambda: self.notes_label.configure(image=img_notes))
            self.after(0, lambda: self.task_manager_label.configure(image=img_task))
        except Exception as e:
            print(f"Image loading failed: {e}")

    def _build_ui(self):
        self.greeting_label = ctk.CTkLabel(
            self,
            width=296,
            height=42,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Ciao Albe',
            font_wrap=True,
            justify='left',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Century Gothic', size=60, weight="bold", slant="roman"),
        )
        self.greeting_label.place(x=34, y=10)

        self.subtitle_label = ctk.CTkLabel(
            self,
            width=217,
            height=25,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Cosa facciamo oggi?',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Century Gothic', size=20, weight="normal", slant="roman"),
        )
        self.subtitle_label.place(x=34, y=81)

        self.frame_1 = ctk.CTkFrame(
            self,
            width=215,
            height=403,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='#0e0e0e',
        )
        self.frame_1.place(x=34, y=134)

        self.yt_downloader_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.yt_downloader_card.place(x=7, y=0)

        self.file_manager_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.file_manager_card.place(x=7, y=68)

        self.word_counter_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.word_counter_card.place(x=7, y=136)

        self.mp4mp3_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.mp4mp3_card.place(x=7, y=204)

        self.notes_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.notes_card.place(x=7, y=273)

        self.task_manager_card = ctk.CTkFrame(
            self.frame_1,
            height=60,
            corner_radius=12,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.task_manager_card.place(x=7, y=342)

        self.yt_downloader_label = ctk.CTkLabel(
            self.frame_1,
            width=164,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  Video Downloader',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman")

        )
        self.yt_downloader_label.place(x=25, y=16)

        self.file_manager_label = ctk.CTkLabel(
            self.frame_1,
            width=164,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  File Manager',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman"),

        )
        self.file_manager_label.place(x=25, y=84)

        self.word_counter_label = ctk.CTkLabel(
            self.frame_1,
            width=164,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  Essay Helper',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman"),
        )
        self.word_counter_label.place(x=23, y=152)

        self.mp4mp3_label = ctk.CTkLabel(
            self.frame_1,
            width=152,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  mp4 --> mp3',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman"),
        )
        self.mp4mp3_label.place(x=23, y=220)

        self.notes_label = ctk.CTkLabel(
            self.frame_1,
            width=164,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  Notes',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman"),
        )
        self.notes_label.place(x=25, y=289)

        self.task_manager_label = ctk.CTkLabel(
            self.frame_1,
            width=167,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            bg_color='#1e1e1e',
            text='  Task manager',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Tahoma', size=15, weight="bold", slant="roman"),
        )
        self.task_manager_label.place(x=24, y=358)

        self.main_frame = ctk.CTkFrame(
            self,
            width=614,
            height=401,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='#1e1e1e',
        )
        self.main_frame.place(x=266, y=134)


# importing thread
def import_libraries_heavy():
    global ytd, get_response_ai, gemini_api
    import yt_dlp as _ytd
    import gemini_api as _gemini_api
    ytd = _ytd
    gemini_api = _gemini_api
    get_response_ai = _gemini_api.get_response_ai


if __name__ == "__main__":
    threading.Thread(target=import_libraries_heavy, daemon=True).start()
    ctk.set_appearance_mode("dark")
    app = AreaPersonale()
    app.mainloop()
