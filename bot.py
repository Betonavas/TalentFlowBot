from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import re
import os
from datetime import datetime

# ==========================================
# TOKEN
# ==========================================

with open("token.txt", "r", encoding="utf-8") as archivo:
    TOKEN = archivo.read().strip()

# ==========================================
# MEMORIA TEMPORAL
# ==========================================

usuarios = {}

# ==========================================
# START
# ==========================================

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    usuarios[telegram_id] = {
        "estado": "NOMBRE"
    }

    print(f"START RECIBIDO - {telegram_id}")

    await update.message.reply_text(
        "👋 Bienvenido a TalentFlow.\n\n"
        "Ingrese su nombre:"
    )

# ==========================================
# MENSAJES
# ==========================================

async def mensaje(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id
    texto = update.message.text.strip()

    if telegram_id not in usuarios:

        await update.message.reply_text(
            "Debe iniciar el proceso con /start"
        )
        return

    estado = usuarios[telegram_id]["estado"]

    # NOMBRE

    if estado == "NOMBRE":

        if not texto.replace(" ", "").isalpha():

            await update.message.reply_text(
                "❌ Nombre inválido."
            )
            return

        usuarios[telegram_id]["nombre"] = texto
        usuarios[telegram_id]["estado"] = "APELLIDO"

        await update.message.reply_text(
            "Ingrese su apellido:"
        )

    # APELLIDO

    elif estado == "APELLIDO":

        if not texto.replace(" ", "").isalpha():

            await update.message.reply_text(
                "❌ Apellido inválido."
            )
            return

        usuarios[telegram_id]["apellido"] = texto
        usuarios[telegram_id]["estado"] = "DNI"

        await update.message.reply_text(
            "Ingrese su DNI:"
        )

    # DNI

    elif estado == "DNI":

        if not re.match(r"^\d{7,8}$", texto):

            await update.message.reply_text(
                "❌ DNI inválido. Debe tener 7 u 8 números."
            )
            return

        usuarios[telegram_id]["dni"] = texto
        usuarios[telegram_id]["estado"] = "FECHA_NACIMIENTO"

        await update.message.reply_text(
            "Ingrese su fecha de nacimiento (dd-mm-aaaa):"
        )

    # FECHA NACIMIENTO

    elif estado == "FECHA_NACIMIENTO":

        try:
            datetime.strptime(texto, "%d-%m-%Y")

        except ValueError:

            await update.message.reply_text(
                "❌ Formato inválido. Ejemplo: 25-12-1995"
            )
            return

        usuarios[telegram_id]["fecha_nacimiento"] = texto
        usuarios[telegram_id]["estado"] = "EMAIL"

        await update.message.reply_text(
            "Ingrese su correo electrónico:"
        )

    # EMAIL

    elif estado == "EMAIL":

        if not re.match(
            r"^[\w\.-]+@[\w\.-]+\.\w+$",
            texto
        ):

            await update.message.reply_text(
                "❌ Correo electrónico inválido."
            )
            return

        usuarios[telegram_id]["email"] = texto
        usuarios[telegram_id]["estado"] = "PROVINCIA"

        await update.message.reply_text(
            "Ingrese su provincia:"
        )

    # PROVINCIA

    elif estado == "PROVINCIA":

        usuarios[telegram_id]["provincia"] = texto
        usuarios[telegram_id]["estado"] = "CIUDAD"

        await update.message.reply_text(
            "Ingrese su ciudad:"
        )

    # CIUDAD

    elif estado == "CIUDAD":

        usuarios[telegram_id]["ciudad"] = texto
        usuarios[telegram_id]["estado"] = "REMUNERACION"

        await update.message.reply_text(
            "Ingrese su remuneración pretendida:"
        )

    # REMUNERACION

    elif estado == "REMUNERACION":

        if not texto.isdigit():

            await update.message.reply_text(
                "❌ Ingrese solo números."
            )
            return

        usuarios[telegram_id]["remuneracion"] = texto
        usuarios[telegram_id]["estado"] = "DISPONIBILIDAD_INICIO"

        await update.message.reply_text(
            "Ingrese horario disponible desde (HH:MM):"
        )

    # DISPONIBILIDAD INICIO

    elif estado == "DISPONIBILIDAD_INICIO":

        if not re.match(
            r"^([01]\d|2[0-3]):([0-5]\d)$",
            texto
        ):

            await update.message.reply_text(
                "❌ Formato inválido. Ejemplo: 09:00"
            )
            return

        usuarios[telegram_id]["disp_inicio"] = texto
        usuarios[telegram_id]["estado"] = "DISPONIBILIDAD_FIN"

        await update.message.reply_text(
            "Ingrese horario disponible hasta (HH:MM):"
        )

    # DISPONIBILIDAD FIN

    elif estado == "DISPONIBILIDAD_FIN":

        if not re.match(
            r"^([01]\d|2[0-3]):([0-5]\d)$",
            texto
        ):

            await update.message.reply_text(
                "❌ Formato inválido. Ejemplo: 18:00"
            )
            return

        usuarios[telegram_id]["disp_fin"] = texto
        usuarios[telegram_id]["estado"] = "CV"

        await update.message.reply_text(
            "📄 Adjunte su CV en formato PDF."
        )

# ==========================================
# RECEPCIÓN DE CV
# ==========================================

async def recibir_cv(update: Update,
                     context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id

    if telegram_id not in usuarios:
        return

    if usuarios[telegram_id]["estado"] != "CV":
        return

    documento = update.message.document

    if documento is None:
        return

    if not documento.file_name.lower().endswith(".pdf"):

        await update.message.reply_text(
            "❌ Solo se aceptan archivos PDF."
        )
        return

    archivo = await documento.get_file()

    dni = usuarios[telegram_id]["dni"]

    nombre_archivo = (
        f"{dni}_{documento.file_name}"
    )

    ruta = os.path.join(
        "cvs",
        nombre_archivo
    )

    await archivo.download_to_drive(
        custom_path=ruta
    )

    usuarios[telegram_id]["cv"] = nombre_archivo

    with open(
        "candidatos.csv",
        "a",
        encoding="utf-8"
    ) as archivo_csv:

        archivo_csv.write(
            f"{telegram_id};"
            f"{usuarios[telegram_id]['nombre']};"
            f"{usuarios[telegram_id]['apellido']};"
            f"{usuarios[telegram_id]['dni']};"
            f"{usuarios[telegram_id]['fecha_nacimiento']};"
            f"{usuarios[telegram_id]['email']};"
            f"{usuarios[telegram_id]['provincia']};"
            f"{usuarios[telegram_id]['ciudad']};"
            f"{usuarios[telegram_id]['remuneracion']};"
            f"{usuarios[telegram_id]['disp_inicio']};"
            f"{usuarios[telegram_id]['disp_fin']};"
            f"{usuarios[telegram_id]['cv']};"
            f"PENDIENTE\n"
        )

    usuarios[telegram_id]["estado"] = "FINALIZADO"

    await update.message.reply_text(
        "✅ Postulación registrada correctamente.\n\n"
        "Estado: PENDIENTE"
    )

# ==========================================
# MAIN
# ==========================================

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .pool_timeout(30)
    .build()
)

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        mensaje
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        recibir_cv
    )
)

print("Bot iniciado correctamente...")

app.run_polling()