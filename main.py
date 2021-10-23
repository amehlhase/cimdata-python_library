import tkinter as tk
import tkinter.font as font
import urllib.request
import json
from tkinter.constants import ANCHOR
from tkinter import messagebox

# GRID Basic Configuration:
root = tk.Tk()
root.title("ISBN-basierte Bibliothek")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# VARIABLEN & KONSTANTEN:
backgroundcolor = '#d3f5dc'  # Basic Hintergrundfarbe
highlightcolor = '#7E9384'  # Highlight-Farbe für Buttons
font_gross = font.Font(family="Calibri", size=18, weight="bold")
font_mittel = font.Font(family="Calibri", size=14)
font_klein = font.Font(family="Calibri", size=11)

BASE_API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

is_infowindow_true = False


# FUNKTIONEN:


def add_to_wishlist():
    # Funktion für den Button "Zur Wunschliste hinzufügen", Titel wird in TXT geschrieben
    with open("txt/bib.txt", "a+") as bib:
        bib.write(f"{book_title}, " + f"{authors}, " +
                  f"ISBN: {book_isbn}, " + "Auf der Wunschliste\n")
    messagebox.showinfo(
        "Info", "Zur Wunschliste hinzugefügt!\nDas Fenster wird jetzt geschlossen.")
    result_window.destroy()  # Schließen des Extra-Fensters nach Hinzufügen
    load_listbox()  # erneutes Laden der Liste, damit aktuell hinzugefügtes Buch auch erscheint


def add_to_currently_reading():
    # Funktion für den Button "Gerade lesend", Titel wird in TXT geschrieben
    with open("txt/bib.txt", "a+") as bib:
        bib.write(f"{book_title}, " + f"{authors}, " +
                  f"ISBN: {book_isbn}, " + "Gerade lesend\n")
    messagebox.showinfo(
        "Info", "Der Titel wurde der Liste als Buch, das du aktuell liest, hinzugefügt!\nDas Fenster wird jetzt geschlossen.")
    result_window.destroy()  # Schließen des Extra-Fensters nach Hinzufügen
    load_listbox()  # erneutes Laden der Liste, damit aktuell hinzugefügtes Buch auch erscheint


def add_to_read():
    # Funktion für den Button "Bereits gelesen", Titel wird in TXT geschrieben
    with open("txt/bib.txt", "a+") as bib:
        bib.write(f"{book_title}, " + f"{authors}, " +
                  f"ISBN: {book_isbn}, " + "Bereits gelesen\n")
    messagebox.showinfo(
        "Info", "Der Titel wurde der Liste als Buch, das du bereits gelesen hast, hinzugefügt!\nDas Fenster wird jetzt geschlossen.")
    result_window.destroy()  # Schließen des Extra-Fensters nach Hinzufügen
    load_listbox()  # erneutes Laden der Liste, damit aktuell hinzugefügtes Buch auch erscheint


def delete_book():
    # Funktion zum Löschen eines ausgewählten Titels (der aktuell angeklickte, also blau markierte ist durch ANCHOR ausgewählt)
    delete_messagebox = messagebox.askyesno(
        "Frage", f"Soll der ausgewählte Eintrag wirklich gelöscht werden?")
    if delete_messagebox:  # nur wenn Ja geklickt wird, wird Eintrag gelöscht
        bib_listbox.delete(ANCHOR)

    # Auslesen und Überschreiben der TXT-Datei
    with open("txt/bib.txt", "r+") as bib:
        bib.truncate(0)  # TXT sicherheitshalber leeren
        for i in range(bib_listbox.size() - 1):
            bib.write(bib_listbox.get(i) + ", ")
        bib.write(bib_listbox.get(bib_listbox.size()-1))

    load_listbox()  # erneutes Laden der Liste, damit aktuell hinzugefügtes Buch auch erscheint


def load_listbox():
    # Funktion zum Laden der TXT in Listbox
    # Listbox leeren, um doppelte Einträge zu vermeiden
    bib_listbox.delete(0, tk.END)
    with open("txt/bib.txt", "r") as bib:
        liste = bib.readlines()  # Auslesen jeder einzelnen Zeile
        for item in liste:
            # Hinzufügen jeder Zeile zur Listbox
            bib_listbox.insert(tk.END, item)


def load_book_listbox(event):
    # Funktion für neues Fenster, in dem Buchinformationen über das aktuell ausgewählte Element in der Listbox angezeigt werden
    global is_infowindow_true, info_window
    if not is_infowindow_true:
        info_window = tk.Toplevel(root)
        info_window.title("Buchinformationen")
        info_window.configure(background=backgroundcolor,
                              highlightbackground=backgroundcolor)

        current_entry = bib_listbox.get(ANCHOR).split(", ")
        current_entry_isbn = current_entry[2].lstrip("ISBN: ")
        current_entry_status = current_entry[-1].rstrip("\n")

        # Auslesen der JSON-Datei
        with urllib.request.urlopen(BASE_API_LINK + current_entry_isbn) as f:
            text = f.read()
        json_obj = json.loads(text.decode("utf-8"))

        book_info = json_obj["items"][0]
        authors = ", ".join(json_obj["items"][0]["volumeInfo"]["authors"])
        book_title = book_info["volumeInfo"]["title"]
        book_isbn = book_info["volumeInfo"]["industryIdentifiers"][1]["identifier"]
        book_pages = book_info["volumeInfo"]["pageCount"]
        book_language = (book_info["volumeInfo"]["language"]).upper()
        book_year = book_info["volumeInfo"]["publishedDate"]

        # GRID Config für separates Fenster
        info_window.grid_rowconfigure(0, weight=1)
        info_window.grid_rowconfigure(1, weight=1)
        info_window.grid_rowconfigure(2, weight=1)
        info_window.grid_rowconfigure(3, weight=1)
        info_window.grid_rowconfigure(4, weight=1)
        info_window.grid_rowconfigure(5, weight=1)
        info_window.grid_rowconfigure(6, weight=1)

        info_window.grid_columnconfigure(0, weight=1)
        info_window.grid_columnconfigure(1, weight=1)

        # Labels mit allen ausgelesenen Informationen:
        tk.Label(info_window,
                 text="Autor*in:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window,
                 text=f"{authors}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=0, column=1, sticky="w")

        tk.Label(info_window,
                 text="Titel:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window,
                 text=f"„{book_title}“", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_window,
                 text="Seitenanzahl:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window, text=f"{book_pages}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
            row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_window,
                 text="Veröffentlichung:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=3, column=0, sticky="w")
        tk.Label(info_window, text=f"{book_year}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
            row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_window,
                 text="Sprache:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window, text=f"{book_language}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
            row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_window,
                 text="ISBN:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window, text=f"{book_isbn}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
            row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(info_window,
                 text="Status:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        tk.Label(info_window, text=f"{current_entry_status}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
            row=6, column=1, padx=5, pady=5, sticky="w")
        is_infowindow_true = True
    else:
        # Schließen des alten Fensters, falls bereits eines geöffnet ist
        info_window.destroy()
        is_infowindow_true = False
        load_book_listbox(event)


def get_book_data():
    # Funktion um Buch-Daten für die eingegebene ISBN abzufragen
    # Formatierung des User-Inputs, um überflüssige Bindestriche und Leerzeichen zu entfernen
    user_input = entry.get().replace("-", "").strip()

    # Auslesen der JSON-Datei mit fest definiertem API-Link (siehe oben bei Variablen) und individuellem User-Input
    with urllib.request.urlopen(BASE_API_LINK + user_input) as f:
        text = f.read()

    open_result_window()  # Öffnen eines neuen Fensters für Suchergebnis

    if len(user_input) == 10 or len(user_input) == 13:
        global json_obj, book_info, authors, book_title, book_isbn, book_pages, book_language, book_year
        json_obj = json.loads(text.decode("utf-8"))

        if json_obj["totalItems"] == 0:
            # falls "echte" ISBN eingegeben wurde, aber kein Ergebnis gefunden werden konnte (Titel z.B. nicht bei Google Books verfügbar oder es handelt sich um ein nicht supportetes Format wie nischige E-Books o.ä.)
            tk.Label(result_window, text="Zu der eingegebenen ISBN wurde leider kein Eintrag gefunden.\nBitte probiere es nochmal und gib eine gültige 13- oder 10-stellige ISBN ein",
                     font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=0, padx=15, pady=15)
        else:
            # falls ISBN gefunden, werden Variablen angelegt, die die benötigten Informationen aus der JSON-Datei bündeln
            book_info = json_obj["items"][0]
            authors = ", ".join(json_obj["items"][0]["volumeInfo"]["authors"])

            book_title = book_info["volumeInfo"]["title"]
            book_isbn = book_info["volumeInfo"]["industryIdentifiers"][1]["identifier"]
            # auskommentiert, da buggy und eher für die Weiterarbeit am Projekt geeignet: thumbnails und summary des Titels
            # book_thumbnail = book_info["volumeInfo"]["imageLinks"]["thumbnail"]
            # book_summary = book_info["searchInfo"]["textSnippet"]
            book_pages = book_info["volumeInfo"]["pageCount"]
            book_language = (book_info["volumeInfo"]["language"]).upper()
            book_year = book_info["volumeInfo"]["publishedDate"]

            # Erstellung und Packing der Label mit den gewünschten Informationen im neuen Fenster
            tk.Label(result_window,
                     text="Autor*in:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window,
                     text=f"{authors}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Titel:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=2, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window,
                     text=f"„{book_title}“", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=2, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Seitenanzahl:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=3, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_pages}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=3, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Veröffentlichung:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=4, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_year}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=4, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Sprache:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=5, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_language}", font=font_klein, background=backgroundcolor,
                     highlightbackground=backgroundcolor).grid(row=5, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="ISBN:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=6, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_isbn}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=6, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Autor*in:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window,
                     text=f"{authors}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Titel:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=2, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window,
                     text=f"„{book_title}“", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=2, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Seitenanzahl:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=3, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_pages}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=3, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Veröffentlichung:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=4, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_year}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=4, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="Sprache:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=5, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_language}", font=font_klein, background=backgroundcolor,
                     highlightbackground=backgroundcolor).grid(row=5, column=1, padx=5, pady=5, sticky="w")

            tk.Label(result_window,
                     text="ISBN:", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=6, column=0, padx=5, pady=5, sticky="w")
            tk.Label(result_window, text=f"{book_isbn}", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(
                row=6, column=1, padx=5, pady=5, sticky="w")

            tk.Button(result_window, text="Auf die Wunschliste",
                      font=font_klein, command=add_to_wishlist, background=highlightcolor,
                      highlightbackground=highlightcolor).grid(row=7, column=0, pady=10, padx=10)
            tk.Button(result_window, text="Gerade lesend",
                      font=font_klein, command=add_to_currently_reading, background=highlightcolor,
                      highlightbackground=highlightcolor).grid(row=7, column=1, pady=10, padx=10)
            tk.Button(result_window, text="Bereits gelesen",
                      font=font_klein, command=add_to_read, background=highlightcolor,
                      highlightbackground=highlightcolor).grid(row=7, column=2, pady=10, padx=10)
    else:
        # Bei ungültiger ISBN-Eingabe, d.h. weder 10- noch 13-stellig
        tk.Label(
            result_window, text="Keine Suchergebnisse! Bitte gib eine gültige 13- oder 10-stellige ISBN ein.", font=font_klein, background=backgroundcolor, highlightbackground=backgroundcolor).grid(row=1, column=0, padx=15, pady=15)


def open_result_window():
    # separate Funktion, um ein eigenes Fenster mit dem Buch-Suchergebnis zu öffnen
    global result_window
    result_window = tk.Toplevel(root)
    result_window.title("Suchergebnis")
    result_window.configure(background=backgroundcolor,
                            highlightbackground=backgroundcolor)

    result_window.grid_rowconfigure(0, weight=1)
    result_window.grid_rowconfigure(1, weight=1)
    result_window.grid_rowconfigure(2, weight=1)
    result_window.grid_rowconfigure(3, weight=1)
    result_window.grid_rowconfigure(4, weight=1)
    result_window.grid_rowconfigure(5, weight=1)
    result_window.grid_rowconfigure(6, weight=1)
    result_window.grid_rowconfigure(7, weight=1)

    result_window.grid_columnconfigure(0, weight=1)
    result_window.grid_columnconfigure(1, weight=1)
    result_window.grid_columnconfigure(2, weight=1)


# Callback-Funktion, um aus der Entrybar heraus mit Enter die get_book_data Funktion aufzurufen; Funktionalität mit bind() weiter unten gesichert
def callback(event):
    get_book_data()


# WIDGETS:
# Widget: Label zur Erklärung für Entrybar
entry_label = tk.Label(root, text="ISBN:", font=font_mittel,
                       background=backgroundcolor, highlightbackground=backgroundcolor)

# Widget: Entry-Bar mit Callback-Funktion, um Enter-Taste drücken zu können statt Such-Button klicken zu müssen
entry = tk.Entry(root, width=30, font=font_mittel)
entry.bind('<Return>', callback)

# Widget: Suchbutton mit eigener Hintergrundfarbe
search_button = tk.Button(
    root, text="Suchen", font=font_mittel, command=get_book_data, background=highlightcolor,
    highlightbackground=highlightcolor)

# Widget: Headline für Listbox
hl_bib = tk.Label(root, text="Meine gespeicherten Bücher:",
                  font=font_gross, background=backgroundcolor, highlightbackground=backgroundcolor)

# Widget: Listbox, in der die Bücherliste dargestellt wird; mit bind() Aufruf der Buchinformationen via Klick auf das Element in der Listbox möglich
bib_listbox = tk.Listbox(root, font=font_klein, width=70, height=20)
bib_listbox.bind("<<ListboxSelect>>", load_book_listbox)

# Widget: Lösch-Button
delete_button = tk.Button(root, text="Eintrag löschen",
                          font=font_mittel, command=delete_book, background=highlightcolor,
                          highlightbackground=highlightcolor)


# Aufruf: Laden der Bücherliste
load_listbox()

# PACKING:
# Festlegen der Hintergrundfarbe (Mac und Windows):
root.configure(background=backgroundcolor, highlightbackground=backgroundcolor)

# Packing von ISBN-Label, Entrybar und Such-Button:
entry_label.grid(row=0, column=0, padx=10, sticky="e")
entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
search_button.grid(row=0, column=2, padx=10, sticky="w")

# Packing von Headline für Listbox sowie Listbox
hl_bib.grid(row=1, column=0, columnspan=3, padx=10, pady=15, sticky="s")
bib_listbox.grid(row=2, column=0, columnspan=3,
                 padx=10, pady=10, sticky="ns")

# Packing Lösch-Button
delete_button.grid(row=3, column=0, columnspan=3,
                   padx=10, pady=10, sticky="ns")


# Aufrufen MAINLOOP:
root.mainloop()
