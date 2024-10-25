from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQueryResultArticle
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.mark_keyboards import marks_keyboard
from loader import db, dp, bot
from states.penaltyball import CreatePenaltyBallState


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
            await message.answer(text="👤 O'quvchi ism familiyasini kiriting:", reply_markup=back_to_menu)
            await CreatePenaltyBallState.student_id.set()


@dp.message_handler(state=CreatePenaltyBallState.student_id)
async def get_student_id(message: types.Message, state: FSMContext):
    full_name = message.text
    try:
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
    except:
        await message.answer(text="⚠️ Bunday o'quvchi topilmadi", reply_markup=back_to_menu)
        return
    students = await db.select_students(first_name=first_name, last_name=last_name)
    if not students:
        await message.answer(text="⚠️ Bunday o'quvchi topilmadi", reply_markup=back_to_menu)
        return
    student = students[0]
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    await state.update_data(student_id=student['id'], rated_by=user['id'])
    await message.answer(text=f"⚖️ {full_name} uchun jarima bali tanlang:", reply_markup=marks_keyboard)
    await CreatePenaltyBallState.ball.set()


@dp.callback_query_handler(text="yes", state=CreatePenaltyBallState.ball)
async def save_penalty_ball_final_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    student_id = data.get('student_id')
    rated_by = data.get('rated_by')
    ball = data.get('ball')
    penalty_ball = await db.create_penalty_ball(
        student_id=student_id,
        rated_by_id=rated_by,
        ball=ball
    )
    await call.message.answer(text="✅ Muvaffaqiyatli saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

@dp.callback_query_handler(text="no", state=CreatePenaltyBallState.ball)
async def cancel_save_penalty_ball(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="🔴 Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreatePenaltyBallState.ball)
async def get_penalty_ball(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(ball=mark)
    data = await state.get_data()
    student_id = data.get('student_id')
    student = await db.select_student(student_id=student_id)
    student_full_name = f"{student['first_name']} {student['last_name']}"
    text = (f"📚 O'quvchi: {student_full_name}\n"
            f"🚫 Jazo bali: {mark}")
    await call.message.edit_text(text=text)
    await call.message.answer(text="Ushbu jazo balini saqlaysizmi❓", reply_markup=confirm_keyboard)
