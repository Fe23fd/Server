import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

TELEGRAM_TOKEN = "7995767811:AAEGfr71uGGspDmkXwZt1yGaqn61jxBZHoc"
 
MODEL_NAME = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Контекст диалога
conversation_history = {}

@dp.message_handler()
async def chat_reply(message: Message):
    user_id = message.from_user.id
    user_message = message.text

    # Инициализация истории
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Добавляем сообщение пользователя
    conversation_history[user_id].append(f"User: {user_message}")

    # Ограничиваем историю (например, последние 20 сообщений)
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

    # Формируем входной контекст
    input_text = "\n".join(conversation_history[user_id]) + "\nBot:"

    # Генерация ответа
    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = model.generate(
        inputs.input_ids,
        max_length=1024,  # Настройте длину генерируемого текста
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    reply = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)

    # Добавляем ответ в историю
    conversation_history[user_id].append(f"Bot: {reply}")

    # Отправляем ответ
    await message.reply(reply)

async def main():
    dp.include_router(dp)  # Включаем диспетчер
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
