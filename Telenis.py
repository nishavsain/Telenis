import os
import random
import asyncio
import time
from telethon import TelegramClient
from telethon.errors import RPCError, ChatWriteForbiddenError, ChatAdminRequiredError

# === BRANDING FUNCTION ===
def show_branding():
    os.system('cls' if os.name == 'nt' else 'clear')
    logos = [
        r"""
    )  (    (        )                   
 ( /(  )\ ) )\ )  ( /(   (               
 )\())(()/((()/(  )\())  )\     (   (    
((_)\  /(_))/(_))((_)\((((_)(   )\  )\   
 _((_)(_)) (_))   _((_))\ _ )\ ((_)((_)  
| \| ||_ _|/ __| | || |(_)_\(_)\ \ / /   
| .` | | | \__ \ | __ | / _ \   \ V /    
|_|\_||___||___/ |_||_|/_/ \_\   \_/     

       Made with ❤️ by Nishav
""",
        r"""
███╗   ██╗██╗███████╗██╗  ██╗ █████╗ ██╗   ██╗
████╗  ██║██║██╔════╝██║  ██║██╔══██╗╚██╗ ██╔╝
██╔██╗ ██║██║███████╗███████║███████║ ╚████╔╝ 
██║╚██╗██║██║╚════██║██╔══██║██╔══██║  ╚██╔╝  
██║ ╚████║██║███████║██║  ██║██║  ██║   ██║   
╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   

       Made with ❤️ by Nishav
""",
        r"""
░▒▓███████▓▒░░▒▓█▓▒░░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒▒▓█▓▒░       
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░░▒▓█▓▒▒▓█▓▒░       
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██▓▒░         

         Made with ❤️ by Nishav
"""
    ]
    print(random.choice(logos))

# === TELEGRAM API CONFIG ===
api_id = 20215532  # Your Telegram API ID
api_hash = '60768aee6fa3376771196ccb8c93fd22'  # Your Telegram API hash

# === MAIN FUNCTION ===
async def send_to_groups():
    show_branding()

    message_text = input("📝 Enter the message to send to all groups:\n> ")
    hours = int(input("⏰ Enter delay hours between rounds: "))
    minutes = int(input("⏰ Enter delay minutes between rounds: "))
    INTERVAL = (hours * 3600) + (minutes * 60)

    client = TelegramClient('gmail_bot_session', api_id, api_hash)
    await client.start()
    print("\n✅ Logged in successfully.\n")

    dialogs = await client.get_dialogs()
    writable_groups = []

    for dialog in dialogs:
        if dialog.is_group:
            try:
                permissions = await client.get_permissions(dialog.entity, 'me')
                if getattr(permissions, 'send_messages', True):
                    writable_groups.append(dialog)
            except (ChatWriteForbiddenError, ChatAdminRequiredError, RPCError):
                continue
            except Exception:
                continue

    print(f"📂 Found {len(writable_groups)} writable groups.\n")

    while True:
        for group in list(writable_groups):
            try:
                print(f"📤 Sending to: {group.name}")
                await client.send_message(group.entity, message_text)
                await asyncio.sleep(2)
            except RPCError as e:
                err_msg = str(e).lower()
                if any(bad in err_msg for bad in [
                    "chat_send_plain_forbidden",
                    "you can't write",
                    "user_banned_in_channel"
                ]):
                    print(f"🚫 Removed {group.name}: {err_msg}")
                    writable_groups.remove(group)
                else:
                    print(f"⚠️ Skipping {group.name} due to RPC error: {err_msg}")
                    writable_groups.remove(group)
            except Exception as e:
                print(f"⚠️ Skipping {group.name} due to unexpected error: {e}")
                writable_groups.remove(group)

        print(f"\n⏳ Waiting {hours}h {minutes}m before next round...\n")
        await asyncio.sleep(INTERVAL)

# === ENTRY POINT ===
if __name__ == "__main__":
    try:
        asyncio.run(send_to_groups())
    except Exception as e:
        print(f"🚨 Fatal error: {e}")
        print("💡 Tip: If you see 'database is locked', delete the session file and restart.")
