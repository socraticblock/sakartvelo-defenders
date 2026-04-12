#!/usr/bin/env python3
"""
Sakartvelo Defenders - Cultural Footer Content Generator
Generates 120+ Georgian cultural facts, proverbs, and historical quotes
for the game's loading screen and main menu cultural footer system.

Each entry is formatted as: CATEGORY | "Fact text in English"
"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cultural_footer.txt")

# ---------------------------------------------------------------------------
# 1. GEORGIAN WINE CULTURE (13 entries)
# ---------------------------------------------------------------------------
WINE_CULTURE = [
    "Georgia is home to the world's oldest wine, with archaeological evidence dating back 8,000 years.",
    "In 2017, UNESCO added the traditional Georgian method of winemaking in qvevri to its Intangible Cultural Heritage list.",
    "Qvevri are large clay vessels buried underground, used for fermenting and storing wine — a tradition unbroken for millennia.",
    "Georgia has over 525 indigenous grape varieties, more than any other country on Earth.",
    "The ancient Georgian winemaking tradition was confirmed by chemical analysis of pottery shards from the South Caucasus region.",
    "Georgian wine was so prized in antiquity that the Greek poet Homer mentioned it in his works.",
    "Rkatsiteli, one of Georgia's oldest grape varieties, can produce wines with remarkable aging potential.",
    "Saperavi, Georgia's signature red grape, is one of the few teinturier grapes with both red skin and red flesh.",
    "The Rtveli — Georgia's traditional grape harvest — is celebrated as a major communal event every autumn.",
    "Georgian amber wine, fermented with grape skins and stems in qvevri, is experiencing a global renaissance among sommeliers.",
    "Legend says that Georgia's patron saint, St. Nino, carried a cross made of grapevine bound with her own hair.",
    "The Georgian toast 'Gaumarjos!' means 'Victory!' and reflects wine's deep connection to Georgian identity and resilience.",
    "Wine is considered a sacred element in Georgian Orthodox tradition and is used in every church sacrament.",
]

# ---------------------------------------------------------------------------
# 2. GEORGIAN ALPHABET (13 entries)
# ---------------------------------------------------------------------------
ALPHABET = [
    "The Georgian alphabet, called Mkhedruli, consists of 33 letters and is one of only 14 unique alphabets in the world.",
    "In 2016, UNESCO inscribed the three historical scripts of the Georgian alphabet on its Representative List of Intangible Cultural Heritage.",
    "Georgia is one of the few nations in the world to have invented its own writing system independently.",
    "The Georgian alphabet has evolved through three distinct scripts: Asomtavruli (capitals), Nuskhuri (minuscule), and Mkhedruli (modern).",
    "King Parnavaz I of Iberia is traditionally credited with creating the first Georgian script in the 3rd century BC.",
    "The modern Mkhedruli script became dominant in the 11th century and is still used today for all Georgian writing.",
    "Georgian has no uppercase or lowercase distinction in its modern script — all letters have the same form.",
    "The Georgian alphabet is written left-to-right and is phonetic, with a nearly one-to-one correspondence between letters and sounds.",
    "Georgian calligraphy is considered a high art form, with annual competitions and exhibitions held in Tbilisi and abroad.",
    "The unique shapes of Georgian letters have inspired modern typographers and designers around the world.",
    "Scholars debate whether the Georgian script was influenced by Aramaic or developed independently — the question remains unresolved.",
    "Each Georgian letter has a traditional numerical value, used historically in religious manuscripts and chronologies.",
    "The oldest surviving Georgian manuscript, the Martyrdom of St. Shushanik, dates to the 5th century AD.",
]

# ---------------------------------------------------------------------------
# 3. GEORGIAN CUISINE (13 entries)
# ---------------------------------------------------------------------------
CUISINE = [
    "Khachapuri — Georgia's iconic cheese-filled bread — comes in regional varieties including Adjarian, Imeretian, and Megrelian styles.",
    "Adjarian khachapuri is shaped like a boat, filled with cheese and butter, and topped with a runny egg — a UNESCO-recognized dish.",
    "Khinkali are Georgian soup dumplings, traditionally filled with spiced meat and broth, eaten with a specific twisting technique.",
    "The supra, or Georgian feast, is a cornerstone of Georgian social life, governed by elaborate ritual and the tamada (toastmaster).",
    "The tamada is the toastmaster at a Georgian supra, expected to deliver eloquent, philosophical toasts that can last minutes each.",
    "Badrijani nigvzit — fried eggplant rolls with walnut-garlic paste — is one of Georgia's most beloved appetizers.",
    "Churchkhela, the 'Georgian Snickers,' is made by dipping walnut strings in concentrated grape juice and drying them like candles.",
    "Georgian cuisine features over 100 types of herb-and-walnut-based dishes, reflecting the country's extraordinary biodiversity.",
    "Chakhokhbili is a traditional Georgian chicken stew with tomatoes, herbs, and aromatic spices, dating back centuries.",
    "Lobio, a hearty bean stew, is considered one of the oldest dishes in Georgian culinary tradition.",
    "Georgian tonis puri — bread baked in a clay tandoor called a tone — has been made the same way for over a thousand years.",
    "Tkemali, a tart plum sauce, is Georgia's national condiment and accompanies almost every meat dish.",
    "Gozinaki, a candy of caramelized walnuts and honey, is traditionally served on New Year's Eve for good fortune.",
]

# ---------------------------------------------------------------------------
# 4. GEORGIAN POLYPHONIC SINGING (12 entries)
# ---------------------------------------------------------------------------
POLYPHONIC_SINGING = [
    "Georgian polyphonic singing was inscribed on UNESCO's Intangible Cultural Heritage list in 2001 — one of the very first entries.",
    "Georgia's three-part singing tradition is among the oldest in the world, with roots reaching back over a thousand years.",
    "Unlike Western harmony, Georgian polyphony is characterized by dissonant intervals, drone bass, and complex yodel-like krimanchuli techniques.",
    "Each region of Georgia has its own distinct polyphonic style — Gurian, Kakhetian, Svan, and Megrelian traditions differ significantly.",
    "Gurian polyphony from western Georgia features a unique improvisational 'krimanchuli' — a high-pitched, yodel-like voice part.",
    "The Chakrulo song, a Georgian polyphonic masterpiece, was included on the Voyager Golden Record sent into space in 1977.",
    "Georgian folk songs were among the first non-Western music studied by European ethnomusicologists in the late 19th century.",
    "The Rustavi Choir, founded in 1968, brought Georgian polyphonic singing to international audiences and won a Grammy Award.",
    "In Kakheti, men sing at the supra table in three-part harmony, with a deep drone bass anchoring the melody above.",
    "Georgian polyphony is traditionally taught orally from generation to generation, without written musical notation.",
    "Scholars believe Georgia's geographic isolation in the Caucasus helped preserve its ancient polyphonic traditions intact.",
    "The 2003 film 'Since Otar Left' featured Georgian polyphonic singing and brought wider awareness to the tradition.",
]

# ---------------------------------------------------------------------------
# 5. GEORGIAN HISTORY FACTS (13 entries)
# ---------------------------------------------------------------------------
HISTORY = [
    "The ancient kingdom of Colchis, in western Georgia, is widely believed to be the land of the Golden Fleece from Greek mythology.",
    "The Greek myth of Jason and the Argonauts likely drew on Georgian traditions of using sheepskins to collect gold from rivers.",
    "Queen Tamar (r. 1184-1213) is considered Georgia's greatest ruler, presiding over a golden age of culture, military power, and diplomacy.",
    "King David the Builder (r. 1089-1125) reunified Georgia and won the decisive Battle of Didgori in 1121 against the Seljuk Turks.",
    "The Battle of Didgori, fought on August 12, 1121, is celebrated annually as Georgia's greatest military victory — 'Didgoroba.'",
    "Georgia adopted Christianity as its state religion in AD 337, making it one of the world's oldest Christian nations.",
    "According to tradition, Saint Nino of Cappadocia brought Christianity to Georgia after seeing a vision of the Virgin Mary.",
    "The Rose Revolution of November 2003 was a peaceful protest that ousted the government and became a model for non-violent democratic change.",
    "Georgia was a major stop on the Silk Road, connecting Europe and Asia through mountain passes in the Caucasus.",
    "The medieval Georgian empire under Queen Tamar stretched from the Black Sea to the Caspian, encompassing much of the South Caucasus.",
    "The Bagrationi dynasty ruled Georgia for over a thousand years, from the 9th century until the Russian annexation in 1801.",
    "The Georgian national epic, 'The Knight in the Panther's Skin' by Shota Rustaveli, was written in the 12th century during Tamar's golden age.",
    "Georgia declared independence from the Soviet Union on April 9, 1991, restoring sovereignty it had lost to Russian annexation in 1801.",
]

# ---------------------------------------------------------------------------
# 6. GEORGIAN PROVERBS AND SAYINGS (13 entries)
# ---------------------------------------------------------------------------
PROVERBS = [
    "A guest is a gift from God — 'სტუმარი ღვთის საჩუქარია' (Stumar gvtis sachukaria).",
    "The wolf changes its fur but not its nature — 'მგამი ბეწვს იცვლის, ხასიათს — არა.'",
    "A good name is better than a rich belt — 'კარგ სახელი აღბარია.'",
    "If you chase two rabbits, you will lose them both — 'ორ მგავს ერთი ცხვარი არ ედევს.'",
    "When the night comes, even a donkey can be mistaken for a horse — 'ღამე მოვა, ნათესავ ცხვარს ცესკვან ვერ განურჩები.'",
    "Every bird admires its own nest — 'ყოველი ფრინველი თავის ბუდეს აქედვენს.'",
    "Where there is no wine, there is no love — 'სადაც არ არის ღვინო, სადაც არ არის სიყვარული.'",
    "The sun does not ask permission to shine — 'მზეს ნება არ ჰკითხავს.'",
    "A tree that is bent while young cannot be straightened when old — 'მოხუც ხეს ვერ გასწორებ.'",
    "Even an ant can carry twice its weight — 'შეიძლება ჭიანჭველმაც თავის წონის ორმაგი ატანოს.'",
    "He who does not climb the mountain will not see the plain — 'მთაზე რომ არ ასვლიხ, ვერ დანახავ ვაკე.'",
    "Patience is bitter, but its fruit is sweet — 'მოთმინება ტკბოლია, მაგრამ მისი ნაყოფი ტკბილი.'",
    "A nation that forgets its past has no future — 'ის ერი არა აქვს მომავალი, რომელიც იწყებს დავიწყოს წარსული.'",
]

# ---------------------------------------------------------------------------
# 7. GEORGIAN NATURE (12 entries)
# ---------------------------------------------------------------------------
NATURE = [
    "The Caucasus Mountains, separating Georgia from Russia to the north, include Mount Shkhara at 5,193 meters — the highest peak in Georgia.",
    "Georgia is one of the most ecologically diverse countries on Earth, with climates ranging from subtropical to alpine to semi-arid.",
    "The Black Sea coast of Georgia features subtropical conditions where tea, citrus fruits, and even bamboo grow naturally.",
    "Georgia's Vashlovani National Park contains semi-arid landscapes resembling the African savanna — rare for Europe.",
    "The Borjomi-Kharagauli National Park is one of the largest protected areas in the Caucasus, home to brown bears, wolves, and lynx.",
    "Georgia's Svaneti region contains glaciers that feed major rivers flowing into both the Black Sea and the Caspian Sea.",
    "The Prometheus Cave in western Georgia features stunning stalactites and stalagmites and is one of the largest caves in the Caucasus.",
    "Lake Ritsa in Abkhazia, surrounded by ancient forests and snow-capped peaks, is considered one of the most beautiful mountain lakes in the world.",
    "Georgia is home to the Caucasian wisent, a rare species of bison that was brought back from the brink of extinction.",
    "The Alazani Valley in Kakheti is one of Georgia's most fertile wine-growing regions, fed by snowmelt from the Caucasus.",
    "Georgia has over 25,000 rivers and approximately 850 lakes, giving it extraordinary water resources for its size.",
    "The Tusheti region in northeastern Georgia is a remote highland paradise, accessible only via a dramatic mountain pass open a few months a year.",
]

# ---------------------------------------------------------------------------
# 8. GEORGIAN ARCHITECTURE (12 entries)
# ---------------------------------------------------------------------------
ARCHITECTURE = [
    "The Svan towers of Upper Svaneti are medieval stone defensive towers, some dating to the 9th century, UNESCO World Heritage listed since 1996.",
    "Uplistsikhe, an ancient rock-hewn town near Gori, was carved into a cliff face and served as a major Silk Road settlement from the 1st millennium BC.",
    "Vardzia, a 13th-century cave city in southern Georgia, once housed 20,000 people and was carved into the side of a mountain under Queen Tamar.",
    "Georgian Orthodox churches feature a distinctive cross-dome architectural style found nowhere else in Christian architecture.",
    "The Jvari Monastery, perched above the confluence of two rivers, is a 6th-century masterpiece and a UNESCO World Heritage Site.",
    "The Gelati Monastery, founded by King David the Builder in 1106, was a major center of learning and houses medieval mosaics of exceptional quality.",
    "Bagrati Cathedral in Kutaisi, built in the 11th century, was one of the largest churches in the medieval Georgian kingdom.",
    "The Svetitskhoveli Cathedral in Mtskheta is the burial site of the robe of Christ, according to Georgian Orthodox tradition.",
    "Mtskheta, Georgia's ancient capital, is a UNESCO World Heritage Site and one of the oldest continuously inhabited cities in the world.",
    "The Narikala Fortress overlooking Tbilisi dates to the 4th century and has been expanded by Arab, Mongol, and Georgian rulers.",
    "Ananuri Fortress on the Georgian Military Highway is a striking 16th-17th century complex with towers and frescoed churches.",
    "The David Gareja monastery complex, partially carved into a semi-desert cliff face, was founded in the 6th century and straddles the Georgia-Azerbaijan border.",
]

# ---------------------------------------------------------------------------
# 9. GEORGIAN LANGUAGE FACTS (12 entries)
# ---------------------------------------------------------------------------
LANGUAGE = [
    "Georgian is the largest member of the Kartvelian language family, which has no known relationship to any other language family in the world.",
    "The Kartvelian language family includes Georgian, Megrelian, Laz, and Svan — all native to the South Caucasus.",
    "Georgian is famous for its consonant clusters, with words like 'gvprtskvni' (you peel us) containing eight consecutive consonants.",
    "Georgian uses an elaborate system of verb conjugation, with verbs marked for person, number, tense, aspect, mood, and version.",
    "The Georgian language has no grammatical gender — not for nouns, pronouns, or adjectives — making it simpler than many European languages.",
    "Georgian is one of the oldest living literary languages, with a rich tradition of hagiographic, historical, and poetic texts dating to the 5th century.",
    "The verb 'to be' is omitted in the present tense in Georgian — 'es me' literally means 'I this' for 'I am this.'",
    "Georgian features postpositions rather than prepositions, placing relation words after the noun they modify.",
    "Ergative-absolutive case alignment in Georgian means the subject of a transitive verb takes a different case than the subject of an intransitive verb.",
    "The Georgian language has contributed virtually no loanwords to English, reflecting centuries of cultural isolation in the Caucasus.",
    "Old Georgian texts from the 5th-10th centuries provide crucial evidence for understanding early Christian literature in the Caucasus.",
    "Georgian has a rich tradition of oral folklore, including epic poems, fairy tales, and ritual songs passed down for generations.",
]

# ---------------------------------------------------------------------------
# 10. GEORGIAN SPORTS AND TRADITIONS (12 entries)
# ---------------------------------------------------------------------------
SPORTS_TRADITIONS = [
    "Lelo burti is an ancient Georgian folk rugby-like sport played with a heavy leather ball, considered a precursor to modern rugby.",
    "Georgia's national rugby team is called 'the Lelos,' named after the traditional folk sport, and has competed in every Rugby World Cup since 2003.",
    "Georgian wrestling has ancient roots and Georgian wrestlers have won numerous Olympic and World Championship medals.",
    "The Georgian national dance, performed by the Sukhishvili National Ballet, is renowned worldwide for its acrobatic jumps and sword dances.",
    "The Khorumi war dance originated in the western region of Adjara and depicts preparations for battle against invading armies.",
    "Georgian chidaoba, a traditional form of wrestling, was inscribed on UNESCO's Intangible Cultural Heritage list in 2018.",
    "Nodar Dumbadze Professional State Youth Theatre in Tbilisi is one of the most important centers for Georgian performing arts.",
    "Tbilisoba, an annual October festival, celebrates the capital city with wine tastings, folk music, and traditional crafts.",
    "The Alaverdoba festival, held annually at Alaverdi Cathedral, combines religious observance with a major harvest celebration and fair.",
    "Georgia's Olympic weightlifting tradition produced legends like Lasha Talakhadze, considered the greatest super heavyweight of all time.",
    "The traditional Georgian martial art 'Mardi' includes stick fighting, dagger techniques, and horsemanship, taught in mountain communities.",
    "Georgian polyphonic lullabies and work songs are integral parts of daily village life, sung while harvesting, building, or caring for children.",
]


def generate_cultural_footer():
    """Compile all entries and write to the cultural footer text file."""

    entries = []

    entries.extend([(f"Wine Culture | \"{e}\"") for e in WINE_CULTURE])
    entries.extend([(f"Alphabet | \"{e}\"") for e in ALPHABET])
    entries.extend([(f"Cuisine | \"{e}\"") for e in CUISINE])
    entries.extend([(f"Polyphonic Singing | \"{e}\"") for e in POLYPHONIC_SINGING])
    entries.extend([(f"History | \"{e}\"") for e in HISTORY])
    entries.extend([(f"Proverbs | \"{e}\"") for e in PROVERBS])
    entries.extend([(f"Nature | \"{e}\"") for e in NATURE])
    entries.extend([(f"Architecture | \"{e}\"") for e in ARCHITECTURE])
    entries.extend([(f"Language | \"{e}\"") for e in LANGUAGE])
    entries.extend([(f"Sports and Traditions | \"{e}\"") for e in SPORTS_TRADITIONS])

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Header comment
        f.write("# Sakartvelo Defenders — Cultural Footer Content\n")
        f.write(f"# Total entries: {len(entries)}\n")
        f.write("# Format: CATEGORY | \"Fact text in English\"\n")
        f.write("# Used on loading screens and main menu rotating footer.\n")
        f.write("#\n")
        f.write("# Categories:\n")
        f.write("#   Wine Culture, Alphabet, Cuisine, Polyphonic Singing,\n")
        f.write("#   History, Proverbs, Nature, Architecture, Language,\n")
        f.write("#   Sports and Traditions\n")
        f.write("#\n\n")

        for entry in entries:
            f.write(entry + "\n")

    return entries


if __name__ == "__main__":
    entries = generate_cultural_footer()
    print(f"Generated {len(entries)} cultural footer entries.")
    print(f"Saved to: {OUTPUT_FILE}")

    # Print category distribution
    from collections import Counter
    counts = Counter(e.split(" | ")[0] for e in entries)
    print("\nCategory distribution:")
    for cat, count in sorted(counts.items()):
        print(f"  {cat}: {count}")
