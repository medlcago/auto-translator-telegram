from telethon import events
from telethon.errors import MessageNotModifiedError
from translatepy import exceptions
from translatepy.translators.google import GoogleTranslate

from data.languages import languages
from loader import client

translator = GoogleTranslate()
language = dict(lang=languages["en"], start=True)


@client.on(events.NewMessage(outgoing=True, pattern="(?i).trlang .+"))
async def set_language(event):
    await event.delete()
    lang = event.message.message.split(" ")[1].lower()
    if lang in languages:
        language["lang"] = languages[lang]
        await client.send_message("me", f"Язык перевода изменен на {language['lang']}")
    else:
        await client.send_message("me", f"Языка с кодом {lang} не существует. Попробуйте еще раз.")


@client.on(events.NewMessage(outgoing=True, pattern=r"(?i).trstart"))
async def start_translating(event):
    await event.delete()
    language["start"] = True
    await client.send_message("me", f"Автоперевод сообщений запущен\nЯзык: {language['lang']}")


@client.on(events.NewMessage(outgoing=True, pattern=r"(?i).trstop"))
async def stop_translating(event):
    await event.delete()
    language["start"] = False
    await client.send_message("me", "Автоперевод сообщений был отключен")


@client.on(events.NewMessage(outgoing=True))
async def main(event):
    if language["start"] and not event.message.message.startswith(".tr") and event.message.message:
        try:
            message = translator.translate(event.message.message, language["lang"])
            print(message.service)
            await event.edit(message.result)
        except (exceptions.NoResult, exceptions.UnknownLanguage) as error:
            await event.delete()
            await client.send_message(
                "me",
                f"При переводе сообщения {event.message.message} на язык ({language['lang']}) возникла ошибка:\n{error}\n\nВозможно, такого языка не существует, попробуйте выбрать другой.")
        except exceptions.UnsupportedLanguage:
            await event.delete()
            await client.send_message("me",
                                      f"К сожалению, язык {language['lang']} не поддерживается. Пожалуйста, попробуйте выбрать другой.")
        except MessageNotModifiedError:
            pass
