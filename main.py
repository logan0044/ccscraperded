from pyrogram import Client
import os

app = Client("session", api_id=14522411, api_hash='b69418d12b33394e39723dd6c61f480b')


@app.on_message()
async def my_handler(client, message):
    if not message.text:
        return

    if "/scrape " in message.text:
        args = message.text.split("/scrape ")[1].split(" ")
        card_number = args[0]
        channel = args[1]
        file = open(f"scrape_{card_number}.txt", "w")
        count_cards = 0

        async for _message in app.iter_history(channel):
            if not _message.text:
                continue

            if "CC" in _message.text:
                card_data_text = _message.text.split("CC => ")[1].split("\n")[0]
                card_data = card_data_text.split("|")
                if card_data[0] == card_number:
                    file.write(card_data_text + "\n")

                    count_cards += 1

        file.close()

        if count_cards >= 10:
            await app.send_document(chat_id=message.chat.id, document=f"scrape_{card_number}.txt")
        else:
            await message.reply("Cards not found.", quote=True)

        os.remove(f"scrape_{card_number}.txt")

app.run()
