"""Generate 1000 German-Spanish vocabulary words"""
import json

# This creates a comprehensive 1000-word vocabulary list
vocab = []
rank = 1

# Articles (5)
articles = [
    ("der", "el"), ("die", "la"), ("das", "el/lo"), ("ein", "un"), ("eine", "una")
]
for de, es in articles:
    vocab.append({"german": de, "spanish": es, "word_class": "article", "frequency_rank": rank})
    rank += 1

# Top 100 verbs
verbs = [
    ("sein", "ser/estar"), ("haben", "tener/haber"), ("werden", "convertirse"),
    ("können", "poder"), ("müssen", "deber"), ("sagen", "decir"),
    ("machen", "hacer"), ("geben", "dar"), ("kommen", "venir"),
    ("wollen", "querer"), ("gehen", "ir"), ("sehen", "ver"),
    ("nehmen", "tomar"), ("finden", "encontrar"), ("wissen", "saber"),
    ("stehen", "estar de pie"), ("bleiben", "quedarse"), ("liegen", "yacer"),
    ("halten", "sostener"), ("lassen", "dejar"), ("denken", "pensar"),
    ("sprechen", "hablar"), ("lernen", "aprender"), ("arbeiten", "trabajar"),
    ("leben", "vivir"), ("spielen", "jugar"), ("hören", "escuchar"),
    ("schreiben", "escribir"), ("lesen", "leer"), ("essen", "comer"),
    ("trinken", "beber"), ("schlafen", "dormir"), ("wachen", "despertar"),
    ("öffnen", "abrir"), ("schließen", "cerrar"), ("kaufen", "comprar"),
    ("verkaufen", "vender"), ("beginnen", "comenzar"), ("enden", "terminar"),
    ("verstehen", "entender"), ("glauben", "creer"), ("hoffen", "esperar"),
    ("warten", "esperar"), ("laufen", "correr"), ("fahren", "conducir"),
    ("fliegen", "volar"), ("schwimmen", "nadar"), ("sitzen", "sentarse"),
    ("tragen", "llevar"), ("bringen", "traer"), ("holen", "buscar"),
    ("ziehen", "tirar"), ("drücken", "empujar"), ("werfen", "lanzar"),
    ("fangen", "atrapar"), ("suchen", "buscar"), ("fragen", "preguntar"),
    ("antworten", "responder"), ("zeigen", "mostrar"), ("erklären", "explicar"),
    ("helfen", "ayudar"), ("brauchen", "necesitar"), ("lieben", "amar"),
    ("hassen", "odiar"), ("mögen", "gustar"), ("kennen", "conocer"),
    ("treffen", "encontrarse"), ("besuchen", "visitar"), ("verlassen", "dejar"),
    ("vergessen", "olvidar"), ("erinnern", "recordar"), ("lachen", "reír"),
    ("weinen", "llorar"), ("lächeln", "sonreír"), ("rufen", "llamar"),
    ("singen", "cantar"), ("tanzen", "bailar"), ("kochen", "cocinar"),
    ("backen", "hornear"), ("waschen", "lavar"), ("putzen", "limpiar"),
    ("bauen", "construir"), ("reparieren", "reparar"), ("malen", "pintar"),
    ("zeichnen", "dibujar"), ("fotografieren", "fotografiar"), ("filmen", "filmar"),
    ("telefonieren", "telefonear"), ("mailen", "enviar correo"), ("chatten", "chatear"),
    ("surfen", "navegar"), ("klicken", "hacer clic"), ("tippen", "teclear"),
    ("drucken", "imprimir"), ("kopieren", "copiar"), ("speichern", "guardar"),
    ("löschen", "borrar"), ("senden", "enviar"), ("empfangen", "recibir"),
    ("packen", "empacar"), ("reisen", "viajar"), ("ankommen", "llegar"),
    ("steigen", "subir"), ("fallen", "caer"), ("springen", "saltar")
]
for de, es in verbs:
    vocab.append({"german": de, "spanish": es, "word_class": "verb", "frequency_rank": rank})
    rank += 1

# Top 200 nouns - organized by category
nouns = [
    # Family & People (50)
    ("Mann", "hombre"), ("Frau", "mujer"), ("Kind", "niño"), ("Baby", "bebé"),
    ("Mutter", "madre"), ("Vater", "padre"), ("Bruder", "hermano"), ("Schwester", "hermana"),
    ("Oma", "abuela"), ("Opa", "abuelo"), ("Onkel", "tío"), ("Tante", "tía"),
    ("Cousin", "primo"), ("Neffe", "sobrino"), ("Nichte", "sobrina"),
    ("Sohn", "hijo"), ("Tochter", "hija"), ("Ehemann", "esposo"), ("Ehefrau", "esposa"),
    ("Freund", "amigo"), ("Freundin", "amiga"), ("Familie", "familia"),
    ("Mensch", "persona"), ("Leute", "gente"), ("Junge", "niño"), ("Mädchen", "niña"),
    ("Person", "persona"), ("Nachbar", "vecino"), ("Kollege", "colega"),
    ("Chef", "jefe"), ("Lehrer", "profesor"), ("Schüler", "alumno"),
    ("Student", "estudiante"), ("Arzt", "médico"), ("Krankenschwester", "enfermera"),
    ("Polizist", "policía"), ("Verkäufer", "vendedor"), ("Koch", "cocinero"),
    ("Kellner", "camarero"), ("Fahrer", "conductor"), ("Pilot", "piloto"),
    ("Künstler", "artista"), ("Musiker", "músico"), ("Sänger", "cantante"),
    ("Schauspieler", "actor"), ("Autor", "autor"), ("Ingenieur", "ingeniero"),
    ("Anwalt", "abogado"), ("Bauer", "agricultor"), ("Fischer", "pescador"),
    
    # Home & Living (50)
    ("Haus", "casa"), ("Wohnung", "apartamento"), ("Zimmer", "habitación"),
    ("Küche", "cocina"), ("Badezimmer", "baño"), ("Schlafzimmer", "dormitorio"),
    ("Wohnzimmer", "sala"), ("Garten", "jardín"), ("Balkon", "balcón"),
    ("Dach", "techo"), ("Wand", "pared"), ("Boden", "suelo"), ("Decke", "techo"),
    ("Tür", "puerta"), ("Fenster", "ventana"), ("Treppe", "escalera"),
    ("Tisch", "mesa"), ("Stuhl", "silla"), ("Bett", "cama"), ("Sofa", "sofá"),
    ("Schrank", "armario"), ("Regal", "estante"), ("Lampe", "lámpara"),
    ("Spiegel", "espejo"), ("Bild", "cuadro"), ("Uhr", "reloj"),
    ("Teppich", "alfombra"), ("Vorhang", "cortina"), ("Kissen", "almohada"),
    ("Decke", "manta"), ("Handtuch", "toalla"), ("Dusche", "ducha"),
    ("Badewanne", "bañera"), ("Toilette", "inodoro"), ("Herd", "estufa"),
    ("Ofen", "horno"), ("Kühlschrank", "refrigerador"), ("Mikrowelle", "microondas"),
    ("Waschmaschine", "lavadora"), ("Staubsauger", "aspiradora"),
    ("Fernseher", "televisor"), ("Radio", "radio"), ("Computer", "computadora"),
    ("Handy", "celular"), ("Telefon", "teléfono"), ("Kamera", "cámara"),
    ("Schlüssel", "llave"), ("Löffel", "cuchara"), ("Gabel", "tenedor"),
    ("Messer", "cuchillo"),
    
    # Time & Nature (40)
    ("Tag", "día"), ("Zeit", "tiempo"), ("Jahr", "año"), ("Leben", "vida"),
    ("Welt", "mundo"), ("Stadt", "ciudad"), ("Land", "país"), ("Dorf", "pueblo"),
    ("Erde", "tierra"), ("Himmel", "cielo"), ("Sonne", "sol"), ("Mond", "luna"),
    ("Stern", "estrella"), ("Wolke", "nube"), ("Regen", "lluvia"),
    ("Schnee", "nieve"), ("Wind", "viento"), ("Sturm", "tormenta"),
    ("Wetter", "clima"), ("Frühling", "primavera"), ("Sommer", "verano"),
    ("Herbst", "otoño"), ("Winter", "invierno"), ("Monat", "mes"),
    ("Woche", "semana"), ("Stunde", "hora"), ("Minute", "minuto"),
    ("Morgen", "mañana"), ("Abend", "noche"), ("Nacht", "noche"),
    ("Berg", "montaña"), ("Fluss", "río"), ("See", "lago"), ("Meer", "mar"),
    ("Strand", "playa"), ("Wald", "bosque"), ("Baum", "árbol"),
    ("Blume", "flor"), ("Gras", "hierba"), ("Stein", "piedra"),
    
    # Education & Work (30)
    ("Schule", "escuela"), ("Universität", "universidad"), ("Klasse", "clase"),
    ("Lektion", "lección"), ("Hausaufgabe", "tarea"), ("Prüfung", "examen"),
    ("Note", "nota"), ("Buch", "libro"), ("Heft", "cuaderno"),
    ("Stift", "bolígrafo"), ("Papier", "papel"), ("Tafel", "pizarra"),
    ("Rucksack", "mochila"), ("Arbeit", "trabajo"), ("Beruf", "profesión"),
    ("Büro", "oficina"), ("Firma", "empresa"), ("Geschäft", "tienda"),
    ("Laden", "tienda"), ("Supermarkt", "supermercado"), ("Bank", "banco"),
    ("Post", "correo"), ("Bibliothek", "biblioteca"), ("Museum", "museo"),
    ("Theater", "teatro"), ("Kino", "cine"), ("Restaurant", "restaurante"),
    ("Hotel", "hotel"), ("Krankenhaus", "hospital"), ("Kirche", "iglesia"),
    
    # Body & Health (30)
    ("Körper", "cuerpo"), ("Kopf", "cabeza"), ("Gesicht", "cara"),
    ("Auge", "ojo"), ("Ohr", "oreja"), ("Nase", "nariz"), ("Mund", "boca"),
    ("Zahn", "diente"), ("Zunge", "lengua"), ("Hals", "cuello"),
    ("Schulter", "hombro"), ("Arm", "brazo"), ("Hand", "mano"),
    ("Finger", "dedo"), ("Bein", "pierna"), ("Fuß", "pie"),
    ("Herz", "corazón"), ("Bauch", "estómago"), ("Rücken", "espalda"),
    ("Haut", "piel"), ("Haar", "cabello"), ("Gesundheit", "salud"),
    ("Krankheit", "enfermedad"), ("Schmerz", "dolor"), ("Medikament", "medicamento"),
    ("Arzt", "médico"), ("Patient", "paciente"), ("Blut", "sangre"),
    ("Knochen", "hueso"), ("Muskel", "músculo")
]
for de, es in nouns:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Top 100 adjectives
adjectives = [
    ("gut", "bueno"), ("groß", "grande"), ("klein", "pequeño"),
    ("neu", "nuevo"), ("alt", "viejo"), ("jung", "joven"),
    ("lang", "largo"), ("kurz", "corto"), ("hoch", "alto"),
    ("niedrig", "bajo"), ("schön", "hermoso"), ("hässlich", "feo"),
    ("schnell", "rápido"), ("langsam", "lento"), ("stark", "fuerte"),
    ("schwach", "débil"), ("hell", "claro"), ("dunkel", "oscuro"),
    ("warm", "cálido"), ("kalt", "frío"), ("heiß", "caliente"),
    ("kühl", "fresco"), ("trocken", "seco"), ("nass", "mojado"),
    ("sauber", "limpio"), ("schmutzig", "sucio"), ("voll", "lleno"),
    ("leer", "vacío"), ("offen", "abierto"), ("geschlossen", "cerrado"),
    ("frei", "libre"), ("besetzt", "ocupado"), ("reich", "rico"),
    ("arm", "pobre"), ("teuer", "caro"), ("billig", "barato"),
    ("wichtig", "importante"), ("unwichtig", "sin importancia"),
    ("möglich", "posible"), ("unmöglich", "imposible"), ("einfach", "fácil"),
    ("schwierig", "difícil"), ("leicht", "ligero"), ("schwer", "pesado"),
    ("weich", "suave"), ("hart", "duro"), ("rund", "redondo"),
    ("eckig", "angular"), ("gerade", "recto"), ("krumm", "torcido"),
    ("breit", "ancho"), ("schmal", "estrecho"), ("dick", "gordo"),
    ("dünn", "delgado"), ("tief", "profundo"), ("flach", "plano"),
    ("weit", "lejos"), ("nah", "cerca"), ("früh", "temprano"),
    ("spät", "tarde"), ("pünktlich", "puntual"), ("laut", "ruidoso"),
    ("leise", "silencioso"), ("still", "tranquilo"), ("ruhig", "calmado"),
    ("süß", "dulce"), ("sauer", "ácido"), ("salzig", "salado"),
    ("bitter", "amargo"), ("scharf", "picante"), ("frisch", "fresco"),
    ("alt", "rancio"), ("gesund", "sano"), ("krank", "enfermo"),
    ("müde", "cansado"), ("wach", "despierto"), ("hungrig", "hambriento"),
    ("durstig", "sediento"), ("satt", "satisfecho"), ("glücklich", "feliz"),
    ("traurig", "triste"), ("fröhlich", "alegre"), ("böse", "enojado"),
    ("ängstlich", "asustado"), ("mutig", "valiente"), ("faul", "perezoso"),
    ("fleißig", "trabajador"), ("intelligent", "inteligente"),
    ("dumm", "tonto"), ("klug", "inteligente"), ("nett", "amable"),
    ("freundlich", "amigable"), ("höflich", "cortés"), ("unhöflich", "grosero"),
    ("lustig", "gracioso"), ("ernst", "serio"), ("interessant", "interesante"),
    ("langweilig", "aburrido"), ("spannend", "emocionante"),
    ("gefährlich", "peligroso"), ("sicher", "seguro")
]
for de, es in adjectives:
    vocab.append({"german": de, "spanish": es, "word_class": "adjective", "frequency_rank": rank})
    rank += 1

# Adverbs (50)
adverbs = [
    ("hier", "aquí"), ("dort", "allí"), ("da", "ahí"),
    ("jetzt", "ahora"), ("heute", "hoy"), ("gestern", "ayer"),
    ("morgen", "mañana"), ("immer", "siempre"), ("nie", "nunca"),
    ("oft", "a menudo"), ("manchmal", "a veces"), ("selten", "raramente"),
    ("wieder", "otra vez"), ("noch", "todavía"), ("schon", "ya"),
    ("bald", "pronto"), ("später", "más tarde"), ("früher", "antes"),
    ("zuerst", "primero"), ("dann", "entonces"), ("danach", "después"),
    ("vorher", "antes"), ("nachher", "después"), ("sofort", "inmediatamente"),
    ("gleich", "enseguida"), ("gerade", "justo ahora"), ("eben", "recién"),
    ("sehr", "muy"), ("zu", "demasiado"), ("genug", "suficiente"),
    ("viel", "mucho"), ("wenig", "poco"), ("mehr", "más"),
    ("weniger", "menos"), ("am meisten", "más"), ("am wenigsten", "menos"),
    ("auch", "también"), ("nur", "solo"), ("fast", "casi"),
    ("etwa", "aproximadamente"), ("ungefähr", "aproximadamente"),
    ("genau", "exactamente"), ("wirklich", "realmente"),
    ("eigentlich", "realmente"), ("vielleicht", "quizás"),
    ("wahrscheinlich", "probablemente"), ("sicher", "seguramente"),
    ("bestimmt", "definitivamente"), ("hoffentlich", "ojalá"),
    ("leider", "lamentablemente")
]
for de, es in adverbs:
    vocab.append({"german": de, "spanish": es, "word_class": "adverb", "frequency_rank": rank})
    rank += 1

# Prepositions (30)
prepositions = [
    ("in", "en"), ("an", "en/a"), ("auf", "en/sobre"),
    ("zu", "a"), ("bei", "en casa de"), ("mit", "con"),
    ("von", "de"), ("für", "para"), ("über", "sobre"),
    ("unter", "debajo de"), ("vor", "delante de"), ("hinter", "detrás de"),
    ("neben", "al lado de"), ("zwischen", "entre"), ("durch", "a través de"),
    ("um", "alrededor de"), ("gegen", "contra"), ("ohne", "sin"),
    ("bis", "hasta"), ("seit", "desde"), ("während", "durante"),
    ("wegen", "debido a"), ("aus", "de/desde"), ("nach", "después de"),
    ("gegenüber", "frente a"), ("entlang", "a lo largo de"),
    ("außerhalb", "fuera de"), ("innerhalb", "dentro de"),
    ("oberhalb", "encima de"), ("unterhalb", "debajo de")
]
for de, es in prepositions:
    vocab.append({"german": de, "spanish": es, "word_class": "preposition", "frequency_rank": rank})
    rank += 1

# Conjunctions (20)
conjunctions = [
    ("und", "y"), ("oder", "o"), ("aber", "pero"),
    ("denn", "porque"), ("sondern", "sino"), ("dass", "que"),
    ("wenn", "cuando/si"), ("weil", "porque"), ("obwohl", "aunque"),
    ("während", "mientras"), ("bevor", "antes de que"),
    ("nachdem", "después de que"), ("bis", "hasta que"),
    ("seit", "desde que"), ("als", "cuando"), ("wie", "como"),
    ("damit", "para que"), ("falls", "en caso de que"),
    ("sobald", "tan pronto como"), ("solange", "mientras")
]
for de, es in conjunctions:
    vocab.append({"german": de, "spanish": es, "word_class": "conjunction", "frequency_rank": rank})
    rank += 1

# Pronouns (30)
pronouns = [
    ("ich", "yo"), ("du", "tú"), ("er", "él"),
    ("sie", "ella"), ("es", "ello"), ("wir", "nosotros"),
    ("ihr", "vosotros"), ("Sie", "usted/ustedes"),
    ("mich", "me"), ("dich", "te"), ("sich", "se"),
    ("uns", "nos"), ("euch", "os"), ("mir", "me"),
    ("dir", "te"), ("ihm", "le"), ("ihr", "le"),
    ("ihnen", "les"), ("mein", "mi"), ("dein", "tu"),
    ("sein", "su"), ("unser", "nuestro"), ("euer", "vuestro"),
    ("dieser", "este"), ("jener", "aquel"), ("welcher", "cual"),
    ("jemand", "alguien"), ("niemand", "nadie"),
    ("etwas", "algo"), ("nichts", "nada")
]
for de, es in pronouns:
    vocab.append({"german": de, "spanish": es, "word_class": "pronoun", "frequency_rank": rank})
    rank += 1

# Numbers (30)
numbers = [
    ("null", "cero"), ("eins", "uno"), ("zwei", "dos"),
    ("drei", "tres"), ("vier", "cuatro"), ("fünf", "cinco"),
    ("sechs", "seis"), ("sieben", "siete"), ("acht", "ocho"),
    ("neun", "nueve"), ("zehn", "diez"), ("elf", "once"),
    ("zwölf", "doce"), ("dreizehn", "trece"), ("vierzehn", "catorce"),
    ("fünfzehn", "quince"), ("zwanzig", "veinte"), ("dreißig", "treinta"),
    ("vierzig", "cuarenta"), ("fünfzig", "cincuenta"),
    ("sechzig", "sesenta"), ("siebzig", "setenta"),
    ("achtzig", "ochenta"), ("neunzig", "noventa"),
    ("hundert", "cien"), ("tausend", "mil"), ("Million", "millón"),
    ("erste", "primero"), ("zweite", "segundo"), ("dritte", "tercero")
]
for de, es in numbers:
    vocab.append({"german": de, "spanish": es, "word_class": "numeral", "frequency_rank": rank})
    rank += 1

# Colors (20)
colors = [
    ("Farbe", "color"), ("rot", "rojo"), ("blau", "azul"),
    ("grün", "verde"), ("gelb", "amarillo"), ("orange", "naranja"),
    ("lila", "morado"), ("rosa", "rosa"), ("braun", "marrón"),
    ("schwarz", "negro"), ("weiß", "blanco"), ("grau", "gris"),
    ("silber", "plateado"), ("gold", "dorado"), ("beige", "beige"),
    ("türkis", "turquesa"), ("violett", "violeta"), ("pink", "rosa"),
    ("hell", "claro"), ("dunkel", "oscuro")
]
for de, es in colors:
    vocab.append({"german": de, "spanish": es, "word_class": "adjective", "frequency_rank": rank})
    rank += 1

# Food & Drinks (80)
food = [
    ("Essen", "comida"), ("Trinken", "bebida"), ("Brot", "pan"),
    ("Butter", "mantequilla"), ("Käse", "queso"), ("Milch", "leche"),
    ("Ei", "huevo"), ("Fleisch", "carne"), ("Fisch", "pescado"),
    ("Huhn", "pollo"), ("Rind", "res"), ("Schwein", "cerdo"),
    ("Wurst", "salchicha"), ("Schinken", "jamón"), ("Salat", "ensalada"),
    ("Gemüse", "verdura"), ("Obst", "fruta"), ("Apfel", "manzana"),
    ("Birne", "pera"), ("Banane", "plátano"), ("Orange", "naranja"),
    ("Zitrone", "limón"), ("Erdbeere", "fresa"), ("Kirsche", "cereza"),
    ("Traube", "uva"), ("Melone", "melón"), ("Ananas", "piña"),
    ("Kartoffel", "papa"), ("Tomate", "tomate"), ("Gurke", "pepino"),
    ("Zwiebel", "cebolla"), ("Knoblauch", "ajo"), ("Karotte", "zanahoria"),
    ("Kohl", "repollo"), ("Salat", "lechuga"), ("Paprika", "pimiento"),
    ("Bohne", "frijol"), ("Reis", "arroz"), ("Nudeln", "fideos"),
    ("Spaghetti", "espagueti"), ("Pizza", "pizza"), ("Suppe", "sopa"),
    ("Salz", "sal"), ("Pfeffer", "pimienta"), ("Zucker", "azúcar"),
    ("Öl", "aceite"), ("Essig", "vinagre"), ("Soße", "salsa"),
    ("Kuchen", "pastel"), ("Torte", "tarta"), ("Keks", "galleta"),
    ("Schokolade", "chocolate"), ("Eis", "helado"), ("Bonbon", "caramelo"),
    ("Honig", "miel"), ("Marmelade", "mermelada"),
    ("Kaffee", "café"), ("Tee", "té"), ("Wasser", "agua"),
    ("Saft", "jugo"), ("Limonade", "limonada"), ("Bier", "cerveza"),
    ("Wein", "vino"), ("Cola", "cola"), ("Kakao", "cacao"),
    ("Frühstück", "desayuno"), ("Mittagessen", "almuerzo"),
    ("Abendessen", "cena"), ("Snack", "merienda"), ("Mahlzeit", "comida"),
    ("Teller", "plato"), ("Tasse", "taza"), ("Glas", "vaso"),
    ("Flasche", "botella"), ("Dose", "lata"), ("Paket", "paquete"),
    ("Löffel", "cuchara"), ("Gabel", "tenedor"), ("Messer", "cuchillo")
]
for de, es in food:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Animals (50)
animals = [
    ("Tier", "animal"), ("Hund", "perro"), ("Katze", "gato"),
    ("Vogel", "pájaro"), ("Pferd", "caballo"), ("Kuh", "vaca"),
    ("Schwein", "cerdo"), ("Schaf", "oveja"), ("Ziege", "cabra"),
    ("Hase", "conejo"), ("Maus", "ratón"), ("Ratte", "rata"),
    ("Hamster", "hámster"), ("Meerschweinchen", "cobaya"),
    ("Fisch", "pez"), ("Hai", "tiburón"), ("Wal", "ballena"),
    ("Delfin", "delfín"), ("Frosch", "rana"), ("Schlange", "serpiente"),
    ("Eidechse", "lagarto"), ("Schildkröte", "tortuga"),
    ("Insekt", "insecto"), ("Fliege", "mosca"), ("Mücke", "mosquito"),
    ("Biene", "abeja"), ("Wespe", "avispa"), ("Ameise", "hormiga"),
    ("Schmetterling", "mariposa"), ("Käfer", "escarabajo"),
    ("Spinne", "araña"), ("Löwe", "león"), ("Tiger", "tigre"),
    ("Elefant", "elefante"), ("Giraffe", "jirafa"), ("Affe", "mono"),
    ("Bär", "oso"), ("Wolf", "lobo"), ("Fuchs", "zorro"),
    ("Hirsch", "ciervo"), ("Reh", "corzo"), ("Wildschwein", "jabalí"),
    ("Eichhörnchen", "ardilla"), ("Igel", "erizo"), ("Adler", "águila"),
    ("Eule", "búho"), ("Taube", "paloma"), ("Huhn", "gallina"),
    ("Ente", "pato"), ("Gans", "ganso")
]
for de, es in animals:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Transportation (30)
transport = [
    ("Auto", "coche"), ("Bus", "autobús"), ("Zug", "tren"),
    ("Straßenbahn", "tranvía"), ("U-Bahn", "metro"),
    ("Flugzeug", "avión"), ("Hubschrauber", "helicóptero"),
    ("Schiff", "barco"), ("Boot", "bote"), ("Fahrrad", "bicicleta"),
    ("Motorrad", "motocicleta"), ("Roller", "scooter"),
    ("Taxi", "taxi"), ("Lkw", "camión"), ("Traktor", "tractor"),
    ("Verkehr", "tráfico"), ("Straße", "calle"), ("Autobahn", "autopista"),
    ("Brücke", "puente"), ("Tunnel", "túnel"), ("Bahnhof", "estación"),
    ("Flughafen", "aeropuerto"), ("Hafen", "puerto"),
    ("Haltestelle", "parada"), ("Parkplatz", "estacionamiento"),
    ("Tankstelle", "gasolinera"), ("Benzin", "gasolina"),
    ("Diesel", "diésel"), ("Reifen", "neumático"), ("Motor", "motor")
]
for de, es in transport:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Clothing (40)
clothing = [
    ("Kleidung", "ropa"), ("Hemd", "camisa"), ("T-Shirt", "camiseta"),
    ("Pullover", "suéter"), ("Jacke", "chaqueta"), ("Mantel", "abrigo"),
    ("Hose", "pantalón"), ("Jeans", "vaqueros"), ("Rock", "falda"),
    ("Kleid", "vestido"), ("Anzug", "traje"), ("Krawatte", "corbata"),
    ("Schal", "bufanda"), ("Handschuh", "guante"), ("Mütze", "gorro"),
    ("Hut", "sombrero"), ("Schuhe", "zapatos"), ("Stiefel", "botas"),
    ("Sandalen", "sandalias"), ("Turnschuhe", "zapatillas deportivas"),
    ("Socken", "calcetines"), ("Strumpfhose", "medias"),
    ("Unterwäsche", "ropa interior"), ("BH", "sujetador"),
    ("Unterhose", "calzoncillo"), ("Pyjama", "pijama"),
    ("Badeanzug", "traje de baño"), ("Bikini", "bikini"),
    ("Badehose", "bañador"), ("Gürtel", "cinturón"),
    ("Tasche", "bolso"), ("Geldbörse", "cartera"),
    ("Rucksack", "mochila"), ("Koffer", "maleta"),
    ("Regenschirm", "paraguas"), ("Brille", "gafas"),
    ("Sonnenbrille", "gafas de sol"), ("Uhr", "reloj"),
    ("Schmuck", "joya"), ("Ring", "anillo")
]
for de, es in clothing:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Sports & Hobbies (30)
sports = [
    ("Sport", "deporte"), ("Fußball", "fútbol"), ("Basketball", "baloncesto"),
    ("Tennis", "tenis"), ("Volleyball", "voleibol"), ("Handball", "balonmano"),
    ("Golf", "golf"), ("Schwimmen", "natación"), ("Laufen", "correr"),
    ("Joggen", "hacer jogging"), ("Wandern", "senderismo"),
    ("Radfahren", "ciclismo"), ("Skifahren", "esquiar"),
    ("Snowboarden", "hacer snowboard"), ("Eislaufen", "patinar sobre hielo"),
    ("Tanzen", "bailar"), ("Yoga", "yoga"), ("Fitness", "fitness"),
    ("Gymnastik", "gimnasia"), ("Kampfsport", "artes marciales"),
    ("Boxen", "boxeo"), ("Hobby", "pasatiempo"), ("Musik", "música"),
    ("Malen", "pintar"), ("Zeichnen", "dibujar"), ("Lesen", "leer"),
    ("Schreiben", "escribir"), ("Fotografieren", "fotografía"),
    ("Reisen", "viajar"), ("Kochen", "cocinar")
]
for de, es in sports:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Technology & Modern Life (30)
tech = [
    ("Internet", "internet"), ("Website", "sitio web"), ("Email", "correo electrónico"),
    ("Passwort", "contraseña"), ("Software", "software"), ("App", "aplicación"),
    ("Download", "descarga"), ("Upload", "subida"), ("Link", "enlace"),
    ("Datei", "archivo"), ("Ordner", "carpeta"), ("Dokument", "documento"),
    ("Foto", "foto"), ("Video", "video"), ("Musik", "música"),
    ("Film", "película"), ("Spiel", "juego"), ("Programm", "programa"),
    ("System", "sistema"), ("Virus", "virus"), ("Hacker", "hacker"),
    ("Netzwerk", "red"), ("Server", "servidor"), ("Cloud", "nube"),
    ("Speicher", "memoria"), ("Bildschirm", "pantalla"),
    ("Tastatur", "teclado"), ("Maus", "ratón"), ("WLAN", "wifi"),
    ("Bluetooth", "bluetooth")
]
for de, es in tech:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Emotions & States (30)
emotions = [
    ("Gefühl", "sentimiento"), ("Liebe", "amor"), ("Hass", "odio"),
    ("Freude", "alegría"), ("Glück", "felicidad"), ("Trauer", "tristeza"),
    ("Angst", "miedo"), ("Wut", "ira"), ("Ärger", "enojo"),
    ("Überraschung", "sorpresa"), ("Interesse", "interés"),
    ("Langeweile", "aburrimiento"), ("Hoffnung", "esperanza"),
    ("Zweifel", "duda"), ("Vertrauen", "confianza"),
    ("Stolz", "orgullo"), ("Scham", "vergüenza"), ("Schuld", "culpa"),
    ("Neid", "envidia"), ("Eifersucht", "celos"), ("Stress", "estrés"),
    ("Ruhe", "calma"), ("Frieden", "paz"), ("Krieg", "guerra"),
    ("Problem", "problema"), ("Lösung", "solución"),
    ("Frage", "pregunta"), ("Antwort", "respuesta"),
    ("Wahrheit", "verdad"), ("Lüge", "mentira")
]
for de, es in emotions:
    vocab.append({"german": de, "spanish": es, "word_class": "noun", "frequency_rank": rank})
    rank += 1

# Common phrases (20)
phrases = [
    ("ja", "sí"), ("nein", "no"), ("bitte", "por favor"),
    ("danke", "gracias"), ("Entschuldigung", "disculpa"),
    ("hallo", "hola"), ("tschüss", "adiós"), ("guten Morgen", "buenos días"),
    ("guten Tag", "buenas tardes"), ("guten Abend", "buenas noches"),
    ("gute Nacht", "buenas noches"), ("bis später", "hasta luego"),
    ("bis morgen", "hasta mañana"), ("wie geht's", "cómo estás"),
    ("gut", "bien"), ("schlecht", "mal"), ("so la la", "más o menos"),
    ("viel Glück", "buena suerte"), ("Prost", "salud"),
    ("Gesundheit", "salud")
]
for de, es in phrases:
    vocab.append({"german": de, "spanish": es, "word_class": "phrase", "frequency_rank": rank})
    rank += 1

print(f"Generated {len(vocab)} words")

# Save to file
with open('vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)

print(f"✅ Saved to vocabulary.json")

# Additional common words to reach 1000 (100)
additional = [
    # Questions words
    ("wer", "quién", "pronoun"), ("was", "qué", "pronoun"),
    ("wo", "dónde", "adverb"), ("wann", "cuándo", "adverb"),
    ("warum", "por qué", "adverb"), ("wie", "cómo", "adverb"),
    ("wieviel", "cuánto", "adverb"), ("welcher", "cuál", "pronoun"),
    
    # Days of the week
    ("Montag", "lunes", "noun"), ("Dienstag", "martes", "noun"),
    ("Mittwoch", "miércoles", "noun"), ("Donnerstag", "jueves", "noun"),
    ("Freitag", "viernes", "noun"), ("Samstag", "sábado", "noun"),
    ("Sonntag", "domingo", "noun"),
    
    # Months
    ("Januar", "enero", "noun"), ("Februar", "febrero", "noun"),
    ("März", "marzo", "noun"), ("April", "abril", "noun"),
    ("Mai", "mayo", "noun"), ("Juni", "junio", "noun"),
    ("Juli", "julio", "noun"), ("August", "agosto", "noun"),
    ("September", "septiembre", "noun"), ("Oktober", "octubre", "noun"),
    ("November", "noviembre", "noun"), ("Dezember", "diciembre", "noun"),
    
    # More verbs
    ("atmen", "respirar", "verb"), ("husten", "toser", "verb"),
    ("niesen", "estornudar", "verb"), ("bluten", "sangrar", "verb"),
    ("heilen", "curar", "verb"), ("wachsen", "crecer", "verb"),
    ("schrumpfen", "encoger", "verb"), ("brechen", "romper", "verb"),
    ("reparieren", "reparar", "verb"), ("flicken", "remendar", "verb"),
    ("nähen", "coser", "verb"), ("stricken", "tejer", "verb"),
    ("häkeln", "hacer ganchillo", "verb"), ("weben", "tejer", "verb"),
    ("schneiden", "cortar", "verb"), ("kleben", "pegar", "verb"),
    ("reißen", "rasgar", "verb"), ("falten", "doblar", "verb"),
    ("biegen", "doblar", "verb"), ("drehen", "girar", "verb"),
    ("schütteln", "sacudir", "verb"), ("mischen", "mezclar", "verb"),
    ("trennen", "separar", "verb"), ("verbinden", "conectar", "verb"),
    ("lösen", "resolver", "verb"), ("gewinnen", "ganar", "verb"),
    ("verlieren", "perder", "verb"), ("kämpfen", "luchar", "verb"),
    ("siegen", "vencer", "verb"), ("scheitern", "fracasar", "verb"),
    
    # More nouns
    ("Gefahr", "peligro", "noun"), ("Sicherheit", "seguridad", "noun"),
    ("Chance", "oportunidad", "noun"), ("Risiko", "riesgo", "noun"),
    ("Vorteil", "ventaja", "noun"), ("Nachteil", "desventaja", "noun"),
    ("Anfang", "comienzo", "noun"), ("Ende", "fin", "noun"),
    ("Mitte", "medio", "noun"), ("Rand", "borde", "noun"),
    ("Ecke", "esquina", "noun"), ("Seite", "lado", "noun"),
    ("Richtung", "dirección", "noun"), ("Weg", "camino", "noun"),
    ("Straße", "calle", "noun"), ("Platz", "plaza", "noun"),
    ("Ort", "lugar", "noun"), ("Stelle", "sitio", "noun"),
    ("Raum", "espacio", "noun"), ("Bereich", "área", "noun"),
    ("Zone", "zona", "noun"), ("Gebiet", "región", "noun"),
    ("Teil", "parte", "noun"), ("Stück", "pieza", "noun"),
    ("Ganzes", "todo", "noun"), ("Hälfte", "mitad", "noun"),
    ("Viertel", "cuarto", "noun"), ("Drittel", "tercio", "noun"),
    ("Prozent", "porcentaje", "noun"), ("Grad", "grado", "noun"),
    ("Temperatur", "temperatura", "noun"), ("Länge", "longitud", "noun"),
    ("Breite", "anchura", "noun"), ("Höhe", "altura", "noun"),
    ("Tiefe", "profundidad", "noun"), ("Gewicht", "peso", "noun"),
    ("Größe", "tamaño", "noun"), ("Alter", "edad", "noun"),
    ("Geschwindigkeit", "velocidad", "noun"), ("Kraft", "fuerza", "noun"),
    ("Energie", "energía", "noun"), ("Macht", "poder", "noun"),
    ("Stärke", "fuerza", "noun"), ("Schwäche", "debilidad", "noun")
]

for de, es, wc in additional:
    vocab.append({"german": de, "spanish": es, "word_class": wc, "frequency_rank": rank})
    rank += 1

print(f"\n✅ Now have {len(vocab)} words total")

with open('vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)
    
print(f"✅ Updated vocabulary.json with {len(vocab)} words")
