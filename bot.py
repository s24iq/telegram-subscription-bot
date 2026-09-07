import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "Your_Token_bot"
CHANNEL_ID = Your_id 

subscriptions = {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Activate / Renew Access", callback_data="sub")],
        [InlineKeyboardButton(text="Subscription Status", callback_data="status")]
    ])

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    welcome_text = (
        "Welcome to Channel Access Management.\n\n"
        "Manage your private channel membership using the options below."
    )
    await message.answer(welcome_text, reply_markup=main_keyboard())

@dp.callback_query(F.data == "sub")
async def subscribe_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    expiry = datetime.now() + timedelta(days=30)
    subscriptions[user_id] = expiry

    invite = await bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)

    confirmation_text = (
        "Subscription Active\n\n"
        f"Valid until: {expiry.strftime('%B %d, %Y')}\n\n"
        f"Your private invite link:\n{invite.invite_link}\n\n"
        "Note: This link is unique and can only be used once."
    )
    await call.message.edit_text(confirmation_text, reply_markup=main_keyboard())
    await call.answer()

@dp.callback_query(F.data == "status")
async def status_handler(call: types.CallbackQuery):
    expiry = subscriptions.get(call.from_user.id)

    if expiry and expiry > datetime.now():
        days_left = (expiry - datetime.now()).days
        status_text = (
            "Membership Status: Active\n\n"
            f"Days remaining: {days_left}\n"
            f"Expiration date: {expiry.strftime('%B %d, %Y')}"
        )
    else:
        status_text = (
            "Membership Status: Inactive\n\n"
            "You do not have an active subscription. Select 'Activate / Renew Access' to subscribe."
        )

    await call.message.edit_text(status_text, reply_markup=main_keyboard())
    await call.answer()

async def auto_kick_expired_users():
    while True:
        now = datetime.now()
        for uid, exp in list(subscriptions.items()):
            if now >= exp:
                try:
                    await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=uid)
                    await bot.unban_chat_member(chat_id=CHANNEL_ID, user_id=uid)
                    subscriptions.pop(uid)
                    await bot.send_message(
                        uid,
                        "Your subscription has expired, and your channel access has been revoked. Renew to regain entry."
                    )
                except Exception as e:
                    logging.error(f"Failed to revoke access for {uid}: {e}")
        await asyncio.sleep(3600)

async def main():
    asyncio.create_task(auto_kick_expired_users())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())