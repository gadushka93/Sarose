from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

user_data = {}  # Speicherung der Bestellinfos je Nutzer

BILDER_PFAD = "Bilder"  # Lokaler Bilder-Ordner

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Jetzt bestellen", callback_data="order_1")],
    ]
    await update.message.reply_text("Willkommen bei Sarose Studios-Bot! 💐 Was möchtest du tun?",
                                    reply_markup=InlineKeyboardMarkup(keyboard))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    if data.startswith("cat_"):
        category = data.replace("cat_", "")
        image_urls = {
            "rosen": "https://example.com/rosen.jpg",
            "braut": "https://example.com/braut.jpg",
            "geburtstag": "https://example.com/geburtstag.jpg",
            "abschluss": "https://example.com/abschluss.jpg",
            "proposal": "https://example.com/proposal.jpg",
        }
        url = image_urls.get(category, "")
        if url:
            await query.message.reply_photo(photo=url, caption=f"{category.capitalize()} 🌸")
        else:
            await query.message.reply_text(f"Bild für Kategorie {category} nicht gefunden.")

    elif data == "order_1":
        user_data[chat_id] = {}
        keyboard = [
            [InlineKeyboardButton("Proposal", callback_data="anlass_proposal")],
            [InlineKeyboardButton("Geburtstag", callback_data="anlass_geburtstag")],
            [InlineKeyboardButton("Abschluss", callback_data="anlass_abschluss")],
            [InlineKeyboardButton("Krankenhausbesuch", callback_data="anlass_krank")],
            [InlineKeyboardButton("Geburt", callback_data="anlass_geburt")],
            [InlineKeyboardButton("Sonstiges", callback_data="anlass_sonst")],
        ]
        await query.message.reply_text("Für welchen Anlass möchtest du Blumen bestellen?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("anlass_"):
        user_data[chat_id]["anlass"] = data.replace("anlass_", "")
        keyboard = [
            [InlineKeyboardButton("Rosen", callback_data="art_rosen")],
            [InlineKeyboardButton("Tulpen", callback_data="art_tulpen")],
            [InlineKeyboardButton("Lilien", callback_data="art_lilien")],
            [InlineKeyboardButton("Pfingstrosen", callback_data="art_pfingstrosen")],
            [InlineKeyboardButton("Rosen-Mix", callback_data="art_mix_rosen")],
            [InlineKeyboardButton("Blumen-Mix", callback_data="art_mix_all")],
            [InlineKeyboardButton("Sonstiges", callback_data="art_sonst")],
        ]
        await query.message.reply_text("Welche Blumenart möchtest du gerne haben?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("art_"):
        user_data[chat_id]["blumenart"] = data.replace("art_", "")
        blumenart = user_data[chat_id]["blumenart"]

        # Einheitliche Straußgrößen für alle Blumenarten
        keyboard = [
            [InlineKeyboardButton("S-Strauß", callback_data="size_30")],
            [InlineKeyboardButton("M-Strauß" , callback_data="size_50")],
            [InlineKeyboardButton("L-Strauß", callback_data="size_100")],
            [InlineKeyboardButton("XL-Strauß", callback_data="size_xl")],
        ]
        await query.message.reply_text("Welche Straußgröße möchtest du?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("size_"):
        anzahl = data.replace("size_", "")
        user_data[chat_id]["rosenanzahl"] = anzahl  # Wird auch für andere Blumenarten verwendet

        # Nur bei Rosen ein Bild senden
        if user_data[chat_id].get("blumenart") == "rosen":
            bild_dateien = {
                "30": "30.jpg",
                "50": "50.jpg",
                "100": "100.jpeg",
                "xl": "100.jpeg",  # Oder ein separates XL-Bild
            }
            bild_datei = bild_dateien.get(anzahl)
            if bild_datei:
                pfad = os.path.join(BILDER_PFAD, bild_datei)
                if os.path.exists(pfad):
                    with open(pfad, "rb") as photo:
                        await query.message.reply_photo(photo=photo, caption=f"💐 Beispiel für deinen Rosenstrauß mit ({anzahl}) Rosen")
                else:
                    await query.message.reply_text(f"Bilddatei {bild_datei} nicht gefunden.")
            else:
                await query.message.reply_text("Kein Bild für diese Auswahl gefunden.")

        # Frage nach Schleierkraut
        keyboard = [
            [InlineKeyboardButton("Ja", callback_data="schleierkraut_ja")],
            [InlineKeyboardButton("Nein", callback_data="schleierkraut_nein")],
        ]
        await query.message.reply_text("Möchtest du Schleierkraut dazu?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("schleierkraut_"):
        antwort = data.replace("schleierkraut_", "")
        user_data[chat_id]["schleierkraut"] = antwort

        # Frage Papierfarbe
        keyboard = [
            [InlineKeyboardButton("Weiß", callback_data="papier_weiss")],
            [InlineKeyboardButton("Weiß-Gold", callback_data="papier_weiss_gold")],
            [InlineKeyboardButton("Schwarz", callback_data="papier_schwarz")],
            [InlineKeyboardButton("Schwarz-Gold", callback_data="papier_schwarz_gold")],
            [InlineKeyboardButton("Rosa", callback_data="papier_rosa")],
            [InlineKeyboardButton("Rosa-Weiß", callback_data="papier_rosa_weiss")],
            [InlineKeyboardButton("Blau", callback_data="papier_blau")],
            [InlineKeyboardButton("Sonstiges", callback_data="papier_sonstiges")],
        ]
        await query.message.reply_text("Welche Papierfarbe möchtest du für deinen Strauß?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("papier_"):
        papierfarbe = data.replace("papier_", "")
        user_data[chat_id]["papierfarbe"] = papierfarbe

        # Frage nach Personalisierung
        keyboard = [
            [InlineKeyboardButton("Ja", callback_data="personalisieren_ja")],
            [InlineKeyboardButton("Nein", callback_data="personalisieren_nein")],
        ]
        await query.message.reply_text("Möchtest du deinen Strauß mit Initialen personalisieren?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("personalisieren_"):
        antwort = data.replace("personalisieren_", "")
        user_data[chat_id]["personalisieren"] = antwort

        # Social Media & Zusammenfassung
        await query.message.reply_text(
            "📲 Für weitere Inspiration schau gerne auf unseren Social Media Kanälen vorbei:\n"
            "👉 Instagram: https://www.instagram.com/sarosestudios\n"
            "👉 TikTok: https://www.tiktok.com/@sarosestudios"
        )

        await query.message.reply_text(
            f"Super! Hier deine aktuelle Auswahl:\n\n"
            f"Anlass: {user_data[chat_id].get('anlass', 'Keine Angabe')}\n"
            f"Blumenart: {user_data[chat_id].get('blumenart', 'Keine Angabe')}\n"
            f"Rosenanzahl / Straußgröße: {user_data[chat_id].get('rosenanzahl', 'Keine Angabe')}\n"
            f"Schleierkraut: {user_data[chat_id].get('schleierkraut', 'Keine Angabe')}\n"
            f"Papierfarbe: {user_data[chat_id].get('papierfarbe', 'Keine Angabe')}\n"
            f"Personalisierung: {user_data[chat_id].get('personalisieren', 'Keine Angabe')}\n\n"
            "Möchtest du direkt bestellen?  Dann kopiere deine Zusammenfassung und schick sie uns als Insta DM, vielen Dank und bis bald :)"
        )

    else:
        await query.message.reply_text("Bitte wähle eine gültige Option aus dem Menü.")

# Option zum Neustart
        keyboard = [
            [InlineKeyboardButton("🔁 Neue Bestellung starten", callback_data="restart_order")],
        ]
        await query.message.reply_text("Möchtest du eine weitere Bestellung aufgeben?", reply_markup=InlineKeyboardMarkup(keyboard))


# Bot-Setup
application = ApplicationBuilder().token("7695091254:AAHf2k60crldQB38zySFNBU-p7mzyOXG8Qk").build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.run_polling()
