from pyrogram import Client, filters

# Initialize the client
api_id = '14776716'
api_hash = '69fc778931cdcfe5f40253c20a8767ac'
session_name = 'userbot_session'
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# ID of the user from whom messages will be accepted
USER_ID = 7232670177  # Replace with the correct ID



@app.on_message(filters.private)
@app.on_edited_message(filters.private)
async def receive_message_from_user(client, message):
    if message.from_user.id == USER_ID:
        try:
            print("Message received:", message.text)
            if message.reply_markup and message.reply_markup.inline_keyboard:
                # Iterate over the inline keyboard buttons
                for i, row in enumerate(message.reply_markup.inline_keyboard):
                    for j, button in enumerate(row):
                        print(f"Found button: {button.text}")
                        if button.text == "✅ Approve":
                            # Click the button
                            await message.click(i, j)
                            print("Clicked the '✅ Approve' button.")
                            return  # Exit after clicking
            else:
                print("No inline keyboard found in the message.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the client
app.run()
