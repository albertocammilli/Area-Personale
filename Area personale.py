from sys import exception

import customtkinter as ctk
from customtkinter import CTkFrame, CTkTextbox, CTkLabel
from tkinter import filedialog
from PIL import Image
import threading
from pathlib import Path
import sys
import string
import os
import json
from datetime import datetime
from send2trash import send2trash

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
                                   corner_radius=5,
                                   command=self.thread_make,
                                   width=180,
                                   height=38,
                                   font=ctk.CTkFont(family='Tahoma', size=15, weight="normal", slant="roman"),
                                   fg_color="green")
        self.insert = ctk.CTkLabel(self.frame,
                                   text="Paste your link here. You can add more than one",
                                   font=ctk.CTkFont(family='Tahoma', size=15, weight="normal", slant="roman"))
        self.options = ctk.CTkComboBox(self.frame,
                                       values=["MP4 Video (Best Quality)", "MP4 Video (Low Quality, 720p)"],
                                       width=350)
        self.text_box = ctk.CTkTextbox(self.frame,
                                       height=200,
                                       width=550,
                                       fg_color="#1b1b1b")
        self.input = ctk.CTkTextbox(self.frame,
                                    height=30,
                                    width=500,
                                    border_color="#808080",
                                    border_width=1)
        self.add = ctk.CTkButton(self.frame,
                                 text="add",
                                 corner_radius=7,
                                 fg_color="orange",
                                 width=60,
                                 hover_color="#8B4000",
                                 command=self.add,)
        self.add.place(relx=0.8, rely=0.25, anchor="center")
        self.options.place(relx=0.45, rely=0.25, anchor="center")
        self.start.place(relx=0.5, rely=0.925, anchor="center")
        self.input.place(relx=0.5, rely=0.15, anchor="center")
        self.insert.place(relx=0.5, rely=0.05, anchor="center")
        self.text_box.place(relx=0.5, rely=0.33, anchor="n")

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
                    "concurrent_fragment_downloads": 4}
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

#could maybe add a priority files system
class FileManager:
    def __init__(self, parent):
        # path of the script
        self.script_dir = Path(__file__).parent

        # files
        self.files = []

        self.filtered_files = []

        # current directory
        self.current = None

        # extentions present
        self.extensions = set()

        self.current_search = ""
        self.current_extension = "all"

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

        # tags
        self.tags_combobox = ctk.CTkComboBox(
            self.frame,
            values=["all"] + list(self.extensions),
            font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
            width=160,
            command=self.change_extension
        )
        self.tags_combobox.place(relx=1, rely=0.15, anchor="ne")
        self.tags_combobox.set("all")

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
            command=lambda: self.search(self.searchbar.get(), self.tags_combobox.get())

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

        # open directory button
        self.directory_button = ctk.CTkButton(self.frame,
                                              text="open directory",
                                              fg_color="#424242",
                                              hover_color="#616161",
                                              width=40,
                                              height=30,
                                              font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                              command=lambda: os.startfile(self.current))
        self.directory_button.place(relx=0.02, rely=0.87)

        # refresh
        self.refresh_button = ctk.CTkButton(self.frame,
                                            text="⟳",
                                            fg_color="#424242",
                                            hover_color="#616161",
                                            width=30,
                                            height=30,
                                            font=ctk.CTkFont(family="Tahoma", size=20, slant="roman"),
                                            command=lambda: self.refresh(self.current_search, self.current_extension))

        self.refresh_button.place(relx=0.21, rely=0.87)

        #warning of double tap
        self.double_tap_label=ctk.CTkLabel(self.frame,
                                           text="Double tap to delete a file",
                                           font=ctk.CTkFont(family="Tahoma", size=10, slant="roman"),
                                           fg_color="transparent",)
        self.double_tap_label.place(relx=0.4, rely=0.87)

        # scrollable frame
        self.files_scrollable_frame = ctk.CTkScrollableFrame(self.frame,
                                                             width=560,
                                                             height=200)
        self.files_scrollable_frame.place(relx=0.51, rely=0.55, anchor="center")

        self.files_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.files_scrollable_frame.grid_rowconfigure(1, weight=0)

    def open_file(self, num, selected_list):
        os.startfile(selected_list[num])
        print(num)

    def change_current(self, value: str):
        if value == "school":
            self.current = self.path_cartella_scuola
        elif value == "personal":
            self.current = self.path_cartella_personale
        else:
            self.current = self.path_cartella_altro
        self.refresh(self.current_search, self.current_extension)

    def select_file(self):
        if self.current is not None:
            files = filedialog.askopenfilenames(title="select a file")
            for file in files:
                file = Path(file)
                destinazione = self.current / file.name
                file.rename(destinazione)
                self.files.append(file)
            self.refresh(self.current_search, self.current_extension)
        else:
            pass

    def search(self, text, extension):
        self.refresh(text, extension)

    def change_extension(self, value):
        self.current_extension = value
        self.refresh(self.current_search, value)

    def show_list(self, selected_list):
        for widget in self.files_scrollable_frame.winfo_children():
            widget.destroy()

        for i, file in enumerate(selected_list):
            label = ctk.CTkLabel(self.files_scrollable_frame, text=file.name, anchor="nw", height=20,
                                 font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"))
            label.grid(row=i, column=0, sticky="nw", pady=2, padx=5)

            delete_button = ctk.CTkButton(self.files_scrollable_frame,
                                          text="delete",
                                          fg_color="#750a02",
                                          hover_color="#b30c00",
                                          width=20,
                                          height=20,
                                          font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"))
            delete_button.grid(row=i, column=1, sticky="", pady=2, padx=5)
            delete_button.bind("<Double-Button-1>", lambda event, idx=i: self.delete_file(idx, selected_list))

            open_button = ctk.CTkButton(self.files_scrollable_frame,
                                        text="open",
                                        fg_color="#b38600",
                                        hover_color="orange",
                                        width=40,
                                        height=20,
                                        font=ctk.CTkFont(family="Tahoma", size=15, slant="roman"),
                                        command=lambda idx=i: self.open_file(idx, selected_list))
            open_button.grid(row=i, column=2, sticky="nw", pady=2, padx=5)

    def delete_file(self, idx, selected_list):
        send2trash(str(selected_list[idx]))
        self.files.remove(selected_list[idx])
        try:
            self.filtered_files.remove(selected_list[idx])
        except:
            pass
        self.refresh(self.current_search, self.current_extension)

    def refresh(self, search, extension):
        self.files.clear()
        self.filtered_files.clear()
        for i, file in enumerate(self.current.iterdir()):
            if file.is_file():
                self.files.append(file)
                self.extensions.add(file.suffix)
        self.tags_combobox.configure(values=["all"] + list(self.extensions))
        # filtering the files
        if search == "" and extension == "all":
            self.show_list(self.files)
        else:
            for file in self.files:
                if extension != "all" and extension != str(file.suffix):
                    continue
                if search.lower() not in file.name.lower() and search != "":
                    continue
                self.filtered_files.append(file)
            self.show_list(self.filtered_files)

    def show(self):
        self.frame.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)

    def hide(self):
        self.frame.place_forget()##

class Mp3ToMp4:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(
            parent,
            fg_color="#1e1e1e",
            corner_radius=6
        )

        self.files=[]

        self.selected_folder=Path(Path.home() / "Downloads")



        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_columnconfigure(0, weight=3)  # select files più largo
        self.frame.grid_columnconfigure(1, weight=1)  # start più stretto

        # header clear all
        self.clear_all_button = ctk.CTkButton(
            self.frame,
            text="Clear All",
            font=ctk.CTkFont(family="Tahoma", size=12, weight="normal", slant="roman"),
            height=24,
            width=80,
            corner_radius=6,
            fg_color="transparent",
            text_color=("gray40", "gray70"),
            hover_color=("gray80", "gray25"),
            border_width=1,
            border_color=("gray70", "gray35"),
            command=self.clear_all
        )
        self.clear_all_button.grid(
            row=0, column=1, sticky="e", padx=(10, 20), pady=(14, 0)
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame,
            corner_radius=10,
            fg_color=("gray86", "gray17"),
        )
        self.scroll_frame.grid(
            row=1, column=0, columnspan=2,
            sticky="nsew", padx=20, pady=(8, 12)
        )

        # --- Bottone "select files" ---
        self.select_files_button = ctk.CTkButton(
            self.frame,
            text="Select Files",
            font=ctk.CTkFont(family="Tahoma", size=16, weight="normal", slant="roman"),
            height=48,
            corner_radius=8,
            command=self.select_files
        )
        self.select_files_button.grid(
            row=2, column=0, sticky="ew", padx=(20, 10), pady=(0, 20)
        )

        self.start_button = ctk.CTkButton(
            self.frame,
            text="Start",
            font=ctk.CTkFont(family="Tahoma", size=18, weight="bold", slant="italic"),
            height=48,
            corner_radius=8,
            fg_color="#2FA72F",
            hover_color="#248024",
            command=self.convert_thread
        )
        self.start_button.grid(
            row=2, column=1, sticky="ew", padx=(10, 20), pady=(0, 20)
        )

        self.browse_button = ctk.CTkButton(
            self.frame,
            text="Browse...",
            font=ctk.CTkFont(family="Tahoma", size=12, weight="normal", slant="italic"),
            height=24,
            width=60,
            corner_radius=6,
            fg_color="transparent",
            text_color=("gray40", "gray70"),
            hover_color=("gray80", "gray25"),
            border_width=1,
            border_color=("gray70", "gray35"),
            command=self.change_directory
        )
        self.browse_button.grid(
            row=0, column=0, sticky="w", padx=(20, 20), pady=(14, 0))

        self.dir_label=ctk.CTkLabel(self.frame,
                                    text=str(self.selected_folder),
                                    font=ctk.CTkFont(family="Tahoma", size=10, weight="normal", slant="italic"),
                                    text_color=("gray80", "gray70"),)
        self.dir_label.grid(row=0, column=0, sticky="w", padx=(100, 20), pady=(14, 0))


    def change_directory(self):
        new_dir=filedialog.askdirectory()
        self.selected_folder=new_dir
        self.update_ui()


    def select_files(self):
        files = filedialog.askopenfilenames(title="select a file", filetypes=[("mp4", "*.mp4")])
        for file in files:
            if Path(file) not in self.files:
                file = Path(file)
                self.files.append(file)
                self.show_files(self.files)
            else:
                pass

    def show_files(self, selected_list):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for i, file in enumerate(selected_list):
            label=ctk.CTkLabel(self.scroll_frame, text=f"{i+1})   {str(file.name)}", font=("Tahoma", 13))
            label.grid(row=i, column=0, sticky="nw",pady=2)

    def clear_all(self):
        self.files.clear()
        self.show_files(self.files)

    def start(self):
        for file in self.files:
            try:
                AudioFileClip(file).write_audiofile(Path(self.selected_folder) / (Path(file).stem + ".mp3"))
            finally:
                AudioFileClip(str(file)).close()
        self.frame.after(0, self.update_ui)



    def convert_thread(self):
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.start, daemon=True).start()
    # show/hide ui

    def update_ui(self):
        self.start_button.configure(state="normal", text="done✅")
        self.frame.after(4000, lambda: self.start_button.configure(text="Start"))
        self.dir_label.configure(text=self.selected_folder)



    def show(self):
        self.frame.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)

    def hide(self):
        self.frame.place_forget()

class Notes:
    def __init__(self,parent):

        self.db = Path(__file__).parent / "notes.json"


        self.frame = ctk.CTkFrame(
            parent,
            fg_color="#1e1e1e",
            corner_radius=6
        )

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=4)
        self.frame.grid_rowconfigure(2, weight=1)

        self.searchbar=ctk.CTkEntry(self.frame,
                                    placeholder_text="search by title, content, date...",
                                    font=ctk.CTkFont(family="Tahoma", size=12, weight="normal", slant="italic"))
        self.searchbar.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=5)

        self.scrollable_frame=ctk.CTkScrollableFrame(self.frame)
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=5)

        self.add_button=ctk.CTkButton(self.frame,
                                      text="+",
                                      fg_color="green",
                                      hover_color="#03a600",
                                      command=lambda: self.open_create_window(app))
        self.add_button.grid(row=2, column=0, sticky="e", padx=5)

        self.show_notes()

    def open_create_window(self, master):
        window = ctk.CTkToplevel(master=master)
        window.geometry("420x560")
        window.title("New note")
        window.configure(fg_color="#1e1e1e")

        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(4, weight=1)  # description
        window.grid_rowconfigure(6, weight=3)  # content

        label_font = ctk.CTkFont(family="Tahoma", size=12, weight="bold", slant="roman")

        # --- Warning ---
        self.warning_label = ctk.CTkLabel(
            window,
            text="⚠  Fill in at least the title or the content",
            font=ctk.CTkFont(family="Tahoma", size=12, weight="normal", slant="italic"),
            text_color="#e0a800",
            anchor="w"
        )

        # --- Title ---
        self.title_label = ctk.CTkLabel(
            window,
            text="Title",
            font=label_font,
            text_color=("gray40", "gray70"),
            anchor="w"
        )
        self.title_label.grid(row=1, column=0, sticky="ew", padx=20, pady=(18, 4))

        self.title_entry = ctk.CTkEntry(
            window,
            placeholder_text="e.g. Shopping list, Chemistry lesson 3...",
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(family="Tahoma", size=13, weight="normal", slant="roman")
        )
        self.title_entry.grid(row=2, column=0, sticky="ew", padx=20)

        # --- Description ---
        self.content_label = ctk.CTkLabel(
            window,
            text="Content",
            font=label_font,
            text_color=("gray40", "gray70"),
            anchor="w"
        )
        self.content_label.grid(row=3, column=0, sticky="ew", padx=20, pady=(16, 4))

        self.content_textbox = ctk.CTkTextbox(
            window,
            fg_color="#1b1b1b",
            corner_radius=6,
            height=70,
            font=ctk.CTkFont(family="Tahoma", size=13, weight="normal", slant="roman")
        )
        self.content_textbox.grid(row=4, column=0, sticky="nsew", padx=20)

        self.description_label = ctk.CTkLabel(
            window,
            text="Expanded description / extras",
            font=label_font,
            text_color=("gray40", "gray70"),
            anchor="w"
        )
        self.description_label.grid(row=5, column=0, sticky="ew", padx=20, pady=(16, 4))

        self.description_textbox = ctk.CTkTextbox(
            window,
            fg_color="#1b1b1b",
            corner_radius=6,
            height=200,
            font=ctk.CTkFont(family="Tahoma", size=13, weight="normal", slant="roman")
        )
        self.description_textbox.grid(row=6, column=0, sticky="nsew", padx=20, pady=(0, 10))

        self.buttons_frame = ctk.CTkFrame(window, fg_color="transparent")
        self.buttons_frame.grid(row=7, column=0, sticky="ew", padx=20, pady=(16, 18))
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.ai_fill_button = ctk.CTkButton(
            self.buttons_frame,
            text="Let AI fill in the rest",
            font=ctk.CTkFont(family="Tahoma", size=13, weight="normal", slant="italic"),
            height=32,
            corner_radius=8,
            fg_color="transparent",
            text_color=("gray40", "gray70"),
            hover_color=("gray80", "gray25"),
            border_width=1,
            border_color=("gray70", "gray35"),
            command=self.on_ai_fill
        )
        self.ai_fill_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.add_note_button = ctk.CTkButton(
            self.buttons_frame,
            text="Add",
            font=ctk.CTkFont(family="Tahoma", size=15, weight="normal", slant="roman"),
            height=32,
            corner_radius=8,
            fg_color="green",
            hover_color="#2FA72F",
            command=lambda: self.on_add_note(window)
        )
        self.add_note_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.delete_note_button = ctk.CTkButton(
            self.buttons_frame,
            text="Delete",
            font=ctk.CTkFont(family="Tahoma", size=15, weight="normal", slant="roman"),
            height=32,
            corner_radius=8,
            fg_color="red",
            hover_color="#FF4D4D",
            command=None)

    def on_ai_fill(self):
        title = self.title_entry.get()
        content = self.content_textbox.get("1.0", "end").strip()
        description = self.description_textbox.get("1.0", "end").strip()
        if title!="" and content!="" and description!="":
            self.warning_label.configure(text="all the fields are already filled! ")
            self.warning_label.grid(row=0, pady=(5,0))
        else:
            self.warning_label.forget()
            threading.Thread(target=lambda: self.ai_fill(title, content, description), daemon=True).start()
            self.ai_fill_button.configure(state="disabled")


    def ai_fill(self, title, content, description):
        new_title=title
        new_content=content
        new_description=description
        #gen title
        if title=="":
            new_title=gemini_api.get_response_ai(f"based on the content of this note: {content+" "+description}, generate a title for it",
                                                 "your job is to generate a proper short title based on the context given. if its just a singular word, write it as the title. if it's a link, search it up and see what it's about before generating a title. output ONLY the text")
        if content=="":
            new_content = gemini_api.get_response_ai(
                f"based on the content of this note: {title + "\n\n" + description}, generate its content. mind you this has to be a very brief summary of the note.",
                "your job is to generate proper short content based on the context of the note given. output ONLY the text")
        if description=="":
            new_description = gemini_api.get_response_ai(
                f"based on the content of this note: {title + "\n\n" + content}, generate its description. This is the place of the note that houses the most detailed description.",
                "your job is to generate proper short content based on the context of the note given. output ONLY the text")
        self.update_ui(new_title, new_content, new_description)

    def update_ui(self, new_title, new_content, new_description):
        self.title_entry.delete(0, "end")
        self.content_textbox.delete("1.0", "end")
        self.description_textbox.delete("1.0", "end")
        self.title_entry.insert(0, new_title)
        self.content_textbox.insert("1.0", new_content)
        self.description_textbox.insert("1.0", new_description)
        self.ai_fill_button.configure(state="normal")

    def on_add_note(self, window):
        title=self.title_entry.get()
        content=self.content_textbox.get("1.0", "end").strip()
        description=self.description_textbox.get("1.0", "end").strip()
        date=datetime.now().isoformat(timespec="seconds")
        if title!="":
            self.add_note(title, content, description, date)
            self.warning_label.grid_forget()
            window.destroy()
        elif content != "" and title == "":
            self.add_note("Untitled note", content, description, date)
            self.warning_label.grid_forget()
            window.destroy()
        else:
            self.warning_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 0))


    def add_note(self, title, content, description,  date=None):
        max_id=0
        if date is None:
            date = datetime.now().isoformat(timespec="seconds")
        notes=[]
        try:
            with open(self.db, encoding="utf-8") as f:
                notes=json.load(f)
        except:
            pass
        for note in notes:
            if note["id"]>max_id:
                max_id=note["id"]

        notes.insert(0,{
            "id": max_id + 1,
            "title": title,
            "content": content,
            "description": description,
            "date": date
        })

        with open(self.db, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        self.show_notes()

    def show_notes(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        notes=[]

        self.scrollable_frame.columnconfigure(0, weight=1)
        notes_sorted = {}
        try:
            with open(self.db, encoding="utf-8") as f:
                notes=json.load(f)
        except:
            pass
        for note in notes:
            day=note["date"][:10]
            notes_sorted.setdefault(day, []).append(note)


        for i, day in enumerate(notes_sorted):
            frame=ctk.CTkFrame(self.scrollable_frame,
                               fg_color="#212121",)
            frame.grid(row=i, column=0, sticky="ew", pady=5, padx=5, ipady=5)
            for val, note in enumerate(notes_sorted[day]):
                frame.columnconfigure(0, weight=1)
                date_label=ctk.CTkLabel(frame,
                                        text=day)
                date_label.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
                label = ctk.CTkLabel(frame,
                                     text=note["title"],
                                     font=ctk.CTkFont(family="Tahoma", size=15, weight="normal", slant="roman"),)
                label.grid(row=val+1, column=0, sticky="w", pady=2, padx=30)

                open_button=ctk.CTkButton(frame,
                                          fg_color="#ffa600",
                                          hover_color="yellow",
                                          text="open",
                                          width=40,
                                          command=lambda binded_note=notes_sorted[day][val]: self.open_note(binded_note),
                                          font=ctk.CTkFont(family="Tahoma", size=15, weight="normal", slant="roman"))
                open_button.grid(row=val+1, column=1, sticky="e", padx=10, pady=2)

    def open_note(self, note):
        self.open_create_window(app)
        self.add_note_button.configure(text="edit note", fg_color="teal", hover_color="#00A5A5",
                                       command=lambda:self.edit_note(note["id"],
                                                                     self.title_entry.get(),
                                                                     self.content_textbox.get("1.0", "end-1c"),
                                                                     self.description_textbox.get("1.0", "end-1c")))
        self.delete_note_button.configure(command = lambda: self.delete_note(note["id"]))
        self.ai_fill_button.configure(text="AI fill  ")
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        self.add_note_button.grid(row=0, column=1, sticky="ew", padx=(10, 10))
        self.delete_note_button.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        self.title_entry.insert(0, note["title"])
        self.content_textbox.insert("1.0", note["content"])
        self.description_textbox.insert("1.0", note["description"])

    def edit_note(self, note_id, title, content, description):
        notes=[]
        note_found=False
        with open(self.db, encoding="utf-8") as f:
            notes=json.load(f)
        for note in notes:
            if note["id"] == note_id:
                note["title"]=title
                note["content"]=content
                note["description"]=description
                note_found=True
                break
        if note_found:
            with open(self.db, "w", encoding="utf-8") as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
        else:
            print("cound not find note")
        self.show_notes()

    def delete_note(self, note_id):
        notes = []
        with open(self.db, encoding="utf-8") as f:
            notes=json.load(f)
        for note in notes:
            if note["id"] == note_id:
                notes.remove(note)
        with open(self.db, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        self.show_notes()

















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

        self.mp3mp4= Mp3ToMp4(self.main_frame)
        self.mp3mp4.hide()

        self.notes=Notes(self.main_frame)
        self.notes.hide()

        # binding
        self.yt_downloader_card.bind("<Button-1>", lambda event: self.launch("youtube"))
        self.yt_downloader_label.bind("<Button-1>", lambda event: self.launch("youtube"))

        self.file_manager_card.bind("<Button-1>", lambda event: self.launch("filemanager"))
        self.file_manager_label.bind("<Button-1>", lambda event: self.launch("filemanager"))

        self.word_counter_card.bind("<Button-1>", lambda event: self.launch("wordcounter"))
        self.word_counter_label.bind("<Button-1>", lambda event: self.launch("wordcounter"))

        self.mp4mp3_card.bind("<Button-1>", lambda event: self.launch("mp3mp4"))
        self.mp4mp3_label.bind("<Button-1>", lambda event: self.launch("mp3mp4"))

        self.notes_card.bind("<Button-1>", lambda event: self.launch("notes"))
        self.notes_label.bind("<Button-1>", lambda event: self.launch("notes"))


        # hover
        self.make_widget_hover(self.yt_downloader_card, self.yt_downloader_label)
        self.make_widget_hover(self.file_manager_card, self.file_manager_label)
        self.make_widget_hover(self.word_counter_card, self.word_counter_label)
        self.make_widget_hover(self.mp4mp3_card, self.mp4mp3_label)
        self.make_widget_hover(self.notes_card, self.notes_label)
        self.make_widget_hover(self.task_manager_card, self.task_manager_label)

        self.program_map = {"youtube": self.yt,
                            "wordcounter": self.word,
                            "filemanager": self.files,
                            "mp3mp4": self.mp3mp4,
                            "notes": self.notes}

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
            width=320,
            height=42,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text=f"Hello, {(Path.home()).name}",
            font_wrap=True,
            justify='left',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Century Gothic', size=60, weight="bold", slant="roman"),
        )
        self.greeting_label.place(x=35, y=10)

        self.subtitle_label = ctk.CTkLabel(
            self,
            width=300,
            height=25,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='What are we doing today?',
            font_wrap=True,
            justify='left',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Century Gothic', size=20, weight="normal", slant="roman"),
        )
        self.subtitle_label.place(x=24, y=81)

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
    global ytd, get_response_ai, gemini_api, AudioFileClip
    import yt_dlp as _ytd
    import gemini_api as _gemini_api
    from moviepy import AudioFileClip as _AudioFileClip
    AudioFileClip= _AudioFileClip
    ytd = _ytd
    gemini_api = _gemini_api
    get_response_ai = _gemini_api.get_response_ai


if __name__ == "__main__":
    threading.Thread(target=import_libraries_heavy, daemon=True).start()
    ctk.set_appearance_mode("dark")
    app = AreaPersonale()
    app.mainloop()
