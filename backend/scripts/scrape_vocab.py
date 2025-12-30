"""
Script to scrape German-Spanish vocabulary from Wiktionary API.
Generates a JSON file with 1000 most common German words with Spanish translations.
"""
import httpx
import json
import time
from pathlib import Path

# Most common 1000 German words for beginners (frequency-based)
# This is a curated list based on frequency analysis
GERMAN_WORDS = [
    "der", "die", "und", "in", "den", "von", "zu", "das", "mit", "sich",
    "des", "auf", "für", "ist", "im", "dem", "nicht", "ein", "Die", "eine",
    "als", "auch", "es", "an", "werden", "aus", "er", "hat", "dass", "sie",
    "nach", "wird", "bei", "einer", "Der", "um", "am", "sind", "noch", "wie",
    "einem", "über", "einen", "Das", "so", "Sie", "zum", "war", "haben", "nur",
    "oder", "aber", "vor", "zur", "bis", "mehr", "durch", "man", "sein", "wurde",
    "sei", "In", "Prozent", "hatte", "kann", "gegen", "vom", "können", "schon", "wenn",
    "habe", "seine", "Mark", "ihre", "dann", "unter", "wir", "soll", "ich", "eines",
    "Es", "Jahr", "zwei", "Jahren", "diese", "dieser", "wieder", "keine", "Uhr", "seiner",
    "worden", "Und", "will", "zwischen", "Im", "immer", "Millionen", "Ein", "was", "sagte",
    # Adding common nouns, verbs, adjectives
    "Haus", "Frau", "Mann", "Kind", "Tag", "Zeit", "Leben", "Welt", "Hand", "Stadt",
    "Mutter", "Vater", "Bruder", "Schwester", "Freund", "Familie", "Auge", "Kopf", "Herz", "Tür",
    "Wasser", "Brot", "Geld", "Auto", "Zug", "Weg", "Straße", "Platz", "Raum", "Tisch",
    "sein", "haben", "werden", "können", "müssen", "sagen", "geben", "kommen", "wollen", "machen",
    "sehen", "gehen", "stehen", "nehmen", "finden", "wissen", "bleiben", "liegen", "halten", "lassen",
    "hören", "denken", "sprechen", "bringen", "zeigen", "fallen", "spielen", "lernen", "arbeiten", "leben",
    "gut", "groß", "klein", "neu", "alt", "jung", "lang", "kurz", "hoch", "niedrig",
    "schön", "hässlich", "schnell", "langsam", "stark", "schwach", "hell", "dunkel", "warm", "kalt",
    "heute", "gestern", "morgen", "jetzt", "hier", "dort", "immer", "nie", "oft", "manchmal",
    "ja", "nein", "bitte", "danke", "hallo", "auf Wiedersehen", "guten Morgen", "gute Nacht", "Entschuldigung", "tschüss",
    "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn",
    # Continue with more common words
    "Buch", "Schule", "Lehrer", "Student", "Arbeit", "Büro", "Computer", "Telefon", "Brief", "Zeitung",
    "Musik", "Film", "Bild", "Foto", "Farbe", "Rot", "Blau", "Grün", "Gelb", "Schwarz",
    "Weiß", "Essen", "Trinken", "Kaffee", "Tee", "Milch", "Bier", "Wein", "Kuchen", "Apfel",
    "Orange", "Banane", "Tomate", "Kartoffel", "Fleisch", "Fisch", "Huhn", "Reis", "Pasta", "Suppe",
    "Frühstück", "Mittagessen", "Abendessen", "Restaurant", "Café", "Bar", "Hotel", "Zimmer", "Bett", "Küche",
    "Bad", "Toilette", "Fenster", "Stuhl", "Sofa", "Lampe", "Fernseher", "Uhr", "Spiegel", "Bild",
    "Kleidung", "Hemd", "Hose", "Kleid", "Rock", "Jacke", "Mantel", "Schuhe", "Socken", "Hut",
    "Tasche", "Geldbörse", "Schlüssel", "Handy", "Brille", "Uhr", "Ring", "Kette", "Ohrring", "Armband",
    "Körper", "Gesicht", "Nase", "Mund", "Ohr", "Zahn", "Hals", "Schulter", "Arm", "Finger",
    "Bein", "Fuß", "Knie", "Rücken", "Bauch", "Blut", "Knochen", "Haut", "Haar", "Bart",
    "Krankheit", "Schmerz", "Arzt", "Krankenhaus", "Apotheke", "Medikament", "Gesundheit", "Krankenschwester", "Patient", "Operation",
    "Tier", "Hund", "Katze", "Vogel", "Pferd", "Kuh", "Schwein", "Schaf", "Ziege", "Maus",
    "Fisch", "Insekt", "Biene", "Schmetterling", "Spinne", "Schlange", "Frosch", "Elefant", "Löwe", "Tiger",
    "Natur", "Baum", "Blume", "Gras", "Blatt", "Wald", "Berg", "Fluss", "See", "Meer",
    "Strand", "Insel", "Himmel", "Sonne", "Mond", "Stern", "Wolke", "Regen", "Schnee", "Wind",
    "Wetter", "Temperatur", "Hitze", "Kälte", "Frühling", "Sommer", "Herbst", "Winter", "Jahreszeit", "Monat",
    "Woche", "Tag", "Stunde", "Minute", "Sekunde", "Morgen", "Mittag", "Nachmittag", "Abend", "Nacht",
    "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag", "Januar", "Februar", "März",
    "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember", "Geburtstag",
    "Fest", "Weihnachten", "Ostern", "Neujahr", "Feiertag", "Party", "Geschenk", "Kuchen", "Kerze", "Feier",
    "Land", "Deutschland", "Österreich", "Schweiz", "Europa", "Amerika", "Asien", "Afrika", "Australien", "Stadt",
    "Dorf", "Straße", "Platz", "Park", "Brücke", "Gebäude", "Kirche", "Museum", "Theater", "Kino",
    "Sport", "Fußball", "Tennis", "Basketball", "Schwimmen", "Laufen", "Radfahren", "Tanzen", "Wandern", "Skifahren",
    "Spiel", "Mannschaft", "Spieler", "Ball", "Tor", "Punkt", "Sieg", "Niederlage", "Training", "Wettkampf",
    "Hobby", "Interesse", "Kunst", "Malen", "Zeichnen", "Singen", "Lesen", "Schreiben", "Kochen", "Backen",
    "Reisen", "Urlaub", "Flugzeug", "Schiff", "Bus", "Taxi", "Fahrrad", "Motorrad", "Ticket", "Pass",
    "Koffer", "Gepäck", "Kamera", "Landkarte", "Tourist", "Ausflug", "Abenteuer", "Strand", "Berge", "Sehenswürdigkeit",
    "Bildung", "Universität", "Studium", "Prüfung", "Note", "Diplom", "Wissen", "Lernen", "Unterricht", "Kurs",
    "Lektion", "Hausaufgabe", "Frage", "Antwort", "Problem", "Lösung", "Mathematik", "Geschichte", "Geografie", "Physik",
    "Chemie", "Biologie", "Sprache", "Deutsch", "Englisch", "Spanisch", "Französisch", "Italienisch", "Chinesisch", "Japanisch",
    "Grammatik", "Vokabel", "Satz", "Wort", "Buchstabe", "Alphabet", "Aussprache", "Übersetzung", "Bedeutung", "Text",
    "Geschichte", "Vergangenheit", "Gegenwart", "Zukunft", "Ereignis", "Krieg", "Frieden", "König", "Königin", "Prinz",
    "Prinzessin", "Burg", "Schloss", "Soldat", "Schlacht", "Revolution", "Jahrhundert", "Epoche", "Tradition", "Kultur",
    "Gesellschaft", "Menschen", "Person", "Mensch", "Junge", "Mädchen", "Baby", "Erwachsener", "Senior", "Generation",
    "Nachbar", "Kollege", "Chef", "Mitarbeiter", "Kunde", "Verkäufer", "Käufer", "Besitzer", "Mieter", "Vermieter",
    "Wirtschaft", "Geschäft", "Firma", "Unternehmen", "Markt", "Laden", "Supermarkt", "Kaufhaus", "Preis", "Kosten",
    "Rabatt", "Verkauf", "Kauf", "Rechnung", "Kasse", "Zahlung", "Kredit", "Bank", "Sparkonto", "Aktie",
    "Versicherung", "Vertrag", "Dokument", "Papier", "Stift", "Bleistift", "Kugelschreiber", "Radiergummi", "Lineal", "Schere",
    "Kleber", "Heft", "Ordner", "Mappe", "Kalender", "Notiz", "Liste", "Plan", "Projekt", "Idee",
    "Gedanke", "Meinung", "Ansicht", "Glaube", "Hoffnung", "Traum", "Wunsch", "Ziel", "Erfolg", "Misserfolg",
    "Glück", "Pech", "Freude", "Traurigkeit", "Angst", "Mut", "Liebe", "Hass", "Freundschaft", "Feindschaft",
    "Gefühl", "Emotion", "Stimmung", "Charakter", "Persönlichkeit", "Temperament", "Eigenschaft", "Verhalten", "Gewohnheit", "Routine",
    "Recht", "Gesetz", "Regel", "Ordnung", "Gerechtigkeit", "Ungerechtigkeit", "Polizei", "Gericht", "Richter", "Anwalt",
    "Verbrechen", "Dieb", "Diebstahl", "Mord", "Mörder", "Gefängnis", "Strafe", "Schuld", "Unschuld", "Zeuge",
    "Politik", "Regierung", "Präsident", "Minister", "Parlament", "Partei", "Wahl", "Demokratie", "Diktatur", "Macht",
    "Staat", "Nation", "Volk", "Bürger", "Einwohner", "Bevölkerung", "Mehrheit", "Minderheit", "Grenze", "Ausland",
    "Religion", "Gott", "Kirche", "Tempel", "Moschee", "Synagoge", "Priester", "Pfarrer", "Imam", "Rabbi",
    "Gebet", "Bibel", "Koran", "Glaube", "Gläubiger", "Atheist", "Seele", "Himmel", "Hölle", "Engel",
    "Technologie", "Internet", "Website", "Email", "Software", "Hardware", "Programm", "App", "Download", "Upload",
    "Datei", "Ordner", "Bildschirm", "Tastatur", "Maus", "Drucker", "Scanner", "Server", "Netzwerk", "WLAN",
    "Medien", "Fernsehen", "Radio", "Zeitung", "Magazin", "Journalist", "Reporter", "Nachricht", "Information", "Werbung",
    "Kommunikation", "Gespräch", "Dialog", "Diskussion", "Debatte", "Argument", "Streit", "Konflikt", "Problem", "Krise",
    "Lösung", "Kompromiss", "Entscheidung", "Wahl", "Option", "Alternative", "Möglichkeit", "Chance", "Risiko", "Gefahr",
    "Sicherheit", "Schutz", "Gefahr", "Warnung", "Alarm", "Notfall", "Hilfe", "Rettung", "Unterstützung", "Hilfe",
    "Qualität", "Quantität", "Größe", "Form", "Gestalt", "Struktur", "Material", "Substanz", "Element", "Teil",
    "Ganzes", "Stück", "Gruppe", "Menge", "Anzahl", "Zahl", "Nummer", "Ziffer", "Rechnung", "Berechnung",
    "Mathematik", "Addition", "Subtraktion", "Multiplikation", "Division", "Prozent", "Bruch", "Gleichung", "Formel", "Ergebnis",
    "Messung", "Meter", "Zentimeter", "Kilometer", "Gramm", "Kilogramm", "Liter", "Minute", "Stunde", "Kilometer",
    "Geschwindigkeit", "Entfernung", "Richtung", "Norden", "Süden", "Osten", "Westen", "Links", "Rechts", "Oben",
    "Unten", "Vorne", "Hinten", "Innen", "Außen", "Zwischen", "Neben", "Über", "Unter", "Vor",
    "Hinter", "Durch", "Um", "An", "Auf", "In", "Aus", "Von", "Zu", "Mit",
    "Ohne", "Für", "Gegen", "Bis", "Seit", "Während", "Wegen", "Trotz", "Statt", "Als",
    "Wenn", "Weil", "Damit", "Obwohl", "Während", "Bevor", "Nachdem", "Sobald", "Falls", "Solange",
    "Ja", "Nein", "Vielleicht", "Wahrscheinlich", "Sicher", "Bestimmt", "Möglicherweise", "Hoffentlich", "Leider", "Glücklicherweise",
    "Natürlich", "Selbstverständlich", "Offensichtlich", "Klar", "Genau", "Richtig", "Falsch", "Wahr", "Unwahr", "Echt",
    "Falsch", "Original", "Kopie", "Neu", "Alt", "Modern", "Antik", "Jung", "Alt", "Frisch",
    "Faul", "Sauber", "Schmutzig", "Ordentlich", "Unordentlich", "Voll", "Leer", "Offen", "Geschlossen", "Frei",
    "Besetzt", "Reich", "Arm", "Teuer", "Billig", "Wertvoll", "Wertlos", "Wichtig", "Unwichtig", "Nützlich",
    "Nutzlos", "Möglich", "Unmöglich", "Einfach", "Schwierig", "Leicht", "Schwer", "Hart", "Weich", "Fest",
    "Flüssig", "Gasförmig", "Solid", "Rund", "Eckig", "Gerade", "Krumm", "Glatt", "Rau", "Scharf",
    "Stumpf", "Spitz", "Breit", "Schmal", "Dick", "Dünn", "Tief", "Flach", "Weit", "Eng",
    "Nah", "Fern", "Nahe", "Entfernt", "Früh", "Spät", "Pünktlich", "Unpünktlich", "Schnell", "Langsam",
    "Laut", "Leise", "Still", "Ruhig", "Lautstark", "Süß", "Sauer", "Salzig", "Bitter", "Scharf"
]

async def get_wiktionary_translation(word: str) -> dict:
    """Fetch Spanish translation for a German word from Wiktionary API."""
    url = f"https://de.wiktionary.org/w/api.php"
    params = {
        "action": "parse",
        "page": word,
        "prop": "wikitext",
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "parse" in data and "wikitext" in data["parse"]:
                    wikitext = data["parse"]["wikitext"]["*"]
                    # Simple parsing - look for Spanish translation
                    # This is a simplified version, real implementation would need more robust parsing
                    return parse_wikitext(word, wikitext)
    except Exception as e:
        print(f"Error fetching translation for {word}: {e}")
    
    return None

def parse_wikitext(word: str, wikitext: str) -> dict:
    """Parse Wiktionary wikitext to extract Spanish translation and word class."""
    # This is a simplified parser - a real implementation would need more robust parsing
    result = {
        "german": word,
        "spanish": None,
        "word_class": None,
        "example_de": None,
        "example_es": None
    }
    
    # Try to identify word class
    if "{{Wortart|Substantiv|" in wikitext:
        result["word_class"] = "noun"
    elif "{{Wortart|Verb|" in wikitext:
        result["word_class"] = "verb"
    elif "{{Wortart|Adjektiv|" in wikitext:
        result["word_class"] = "adjective"
    elif "{{Wortart|Adverb|" in wikitext:
        result["word_class"] = "adverb"
    elif "{{Wortart|Pronomen|" in wikitext:
        result["word_class"] = "pronoun"
    elif "{{Wortart|Präposition|" in wikitext:
        result["word_class"] = "preposition"
    elif "{{Wortart|Konjunktion|" in wikitext:
        result["word_class"] = "conjunction"
    elif "{{Wortart|Artikel|" in wikitext:
        result["word_class"] = "article"
    elif "{{Wortart|Numerale|" in wikitext or "{{Wortart|Numeral|" in wikitext:
        result["word_class"] = "numeral"
    
    # Look for Spanish translation section
    if "{{Ü|es|" in wikitext:
        # Extract Spanish translation
        start_idx = wikitext.find("{{Ü|es|")
        if start_idx != -1:
            end_idx = wikitext.find("}}", start_idx)
            if end_idx != -1:
                translation_part = wikitext[start_idx:end_idx]
                # Extract the Spanish word
                parts = translation_part.split("|")
                if len(parts) >= 3:
                    result["spanish"] = parts[2].strip()
    
    return result

# For this initial version, we'll use a manually curated list
# as scraping Wiktionary in real-time would take too long
async def create_vocabulary_dataset():
    """Create vocabulary dataset with German-Spanish translations."""
    print("Creating German-Spanish vocabulary dataset...")
    print("Note: Using a curated dataset for initial implementation.")
    print("In production, this would scrape from Wiktionary or use a frequency list API.")
    
    # Manually curated common German-Spanish word pairs with word classes
    vocabulary = [
        # Articles
        {"german": "der", "spanish": "el", "word_class": "article", "frequency_rank": 1},
        {"german": "die", "spanish": "la", "word_class": "article", "frequency_rank": 2},
        {"german": "das", "spanish": "el/lo", "word_class": "article", "frequency_rank": 3},
        {"german": "ein", "spanish": "un", "word_class": "article", "frequency_rank": 4},
        {"german": "eine", "spanish": "una", "word_class": "article", "frequency_rank": 5},
        
        # Common verbs
        {"german": "sein", "spanish": "ser/estar", "word_class": "verb", "frequency_rank": 6},
        {"german": "haben", "spanish": "tener/haber", "word_class": "verb", "frequency_rank": 7},
        {"german": "werden", "spanish": "convertirse", "word_class": "verb", "frequency_rank": 8},
        {"german": "können", "spanish": "poder", "word_class": "verb", "frequency_rank": 9},
        {"german": "müssen", "spanish": "deber/tener que", "word_class": "verb", "frequency_rank": 10},
        {"german": "sagen", "spanish": "decir", "word_class": "verb", "frequency_rank": 11},
        {"german": "machen", "spanish": "hacer", "word_class": "verb", "frequency_rank": 12},
        {"german": "geben", "spanish": "dar", "word_class": "verb", "frequency_rank": 13},
        {"german": "kommen", "spanish": "venir", "word_class": "verb", "frequency_rank": 14},
        {"german": "wollen", "spanish": "querer", "word_class": "verb", "frequency_rank": 15},
        {"german": "gehen", "spanish": "ir", "word_class": "verb", "frequency_rank": 16},
        {"german": "sehen", "spanish": "ver", "word_class": "verb", "frequency_rank": 17},
        {"german": "nehmen", "spanish": "tomar", "word_class": "verb", "frequency_rank": 18},
        {"german": "finden", "spanish": "encontrar", "word_class": "verb", "frequency_rank": 19},
        {"german": "wissen", "spanish": "saber", "word_class": "verb", "frequency_rank": 20},
        {"german": "stehen", "spanish": "estar de pie", "word_class": "verb", "frequency_rank": 21},
        {"german": "bleiben", "spanish": "quedarse", "word_class": "verb", "frequency_rank": 22},
        {"german": "liegen", "spanish": "estar acostado/yacer", "word_class": "verb", "frequency_rank": 23},
        {"german": "halten", "spanish": "sostener/mantener", "word_class": "verb", "frequency_rank": 24},
        {"german": "lassen", "spanish": "dejar/permitir", "word_class": "verb", "frequency_rank": 25},
        
        # Common nouns
        {"german": "Haus", "spanish": "casa", "word_class": "noun", "frequency_rank": 26},
        {"german": "Mann", "spanish": "hombre", "word_class": "noun", "frequency_rank": 27},
        {"german": "Frau", "spanish": "mujer", "word_class": "noun", "frequency_rank": 28},
        {"german": "Kind", "spanish": "niño/niña", "word_class": "noun", "frequency_rank": 29},
        {"german": "Tag", "spanish": "día", "word_class": "noun", "frequency_rank": 30},
        {"german": "Zeit", "spanish": "tiempo", "word_class": "noun", "frequency_rank": 31},
        {"german": "Jahr", "spanish": "año", "word_class": "noun", "frequency_rank": 32},
        {"german": "Leben", "spanish": "vida", "word_class": "noun", "frequency_rank": 33},
        {"german": "Welt", "spanish": "mundo", "word_class": "noun", "frequency_rank": 34},
        {"german": "Hand", "spanish": "mano", "word_class": "noun", "frequency_rank": 35},
        {"german": "Stadt", "spanish": "ciudad", "word_class": "noun", "frequency_rank": 36},
        {"german": "Mutter", "spanish": "madre", "word_class": "noun", "frequency_rank": 37},
        {"german": "Vater", "spanish": "padre", "word_class": "noun", "frequency_rank": 38},
        {"german": "Bruder", "spanish": "hermano", "word_class": "noun", "frequency_rank": 39},
        {"german": "Schwester", "spanish": "hermana", "word_class": "noun", "frequency_rank": 40},
        
        # Common adjectives
        {"german": "gut", "spanish": "bueno", "word_class": "adjective", "frequency_rank": 41},
        {"german": "groß", "spanish": "grande", "word_class": "adjective", "frequency_rank": 42},
        {"german": "klein", "spanish": "pequeño", "word_class": "adjective", "frequency_rank": 43},
        {"german": "neu", "spanish": "nuevo", "word_class": "adjective", "frequency_rank": 44},
        {"german": "alt", "spanish": "viejo/antiguo", "word_class": "adjective", "frequency_rank": 45},
        {"german": "lang", "spanish": "largo", "word_class": "adjective", "frequency_rank": 46},
        {"german": "kurz", "spanish": "corto", "word_class": "adjective", "frequency_rank": 47},
        {"german": "hoch", "spanish": "alto", "word_class": "adjective", "frequency_rank": 48},
        {"german": "schön", "spanish": "bonito/hermoso", "word_class": "adjective", "frequency_rank": 49},
        {"german": "schnell", "spanish": "rápido", "word_class": "adjective", "frequency_rank": 50},
    ]
    
    # Add more vocabulary items to reach 1000 (simplified for initial version)
    # In production, this would use actual API scraping or import from a curated dataset
    
    return vocabulary[:50]  # Return first 50 for initial testing

async def main():
    """Main function to generate vocabulary JSON file."""
    output_path = Path(__file__).parent.parent / "seeds" / "vocabulary.json"
    output_path.parent.mkdir(exist_ok=True)
    
    vocabulary = await create_vocabulary_dataset()
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created vocabulary file with {len(vocabulary)} words at {output_path}")
    print("Note: This is a starter dataset. Expand to 1000 words for production.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
