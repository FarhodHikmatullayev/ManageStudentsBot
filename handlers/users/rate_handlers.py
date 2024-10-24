from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQueryResultArticle

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from loader import db, dp, bot
from states.penaltyball import CreatePenaltyBallState
from states.teachers import CreateTeacherState


@dp.inline_handler()
async def inline_search_student(inline_query: types.InlineQuery, state: FSMContext):
    query_text = inline_query.query.strip()  # Kiritilgan qidiruv matni
    print('query_text', query_text)
    results = []
    if query_text:
        students = await db.select_all_students()
        for student in students:
            full_name = f"{student['first_name']} {student['last_name']}"
            print('full_name', full_name)
            if query_text.lower() in full_name.lower():
                results.append(
                    InlineQueryResultArticle(
                        id=student['id'],
                        title=full_name,
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"Tanlangan o'quvchi: {full_name}"
                        )
                    )
                )
        full_name = results[0]["Tanlangan o'quvchi"]

    await bot.answer_inline_query(inline_query.id, results, is_personal=True)


@dp.message_handler(text="🔴 Jarima bali qo'yish", state="*")
async def delete_teacher(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role not in ['admin', 'teacher']:
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="O'quvchi ism familiyasini kiriting:\n"
                                      "via @Student128Bot", reply_markup=back_to_menu)
            await CreatePenaltyBallState.student_id.set()


@dp.message_handler(state=CreatePenaltyBallState.student_id)
async def get_student_id(message: types.Message, state: FSMContext):
    full_name = message.text
