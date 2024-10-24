from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from keyboards.default.teacher_actions import teacher_actions_default_keyboard
from loader import dp, db

from states.teachers import CreateTeacherState, UpdateTeacherState


@dp.message_handler(text="🔙 Orqaga", state=[CreateTeacherState.first_name, UpdateTeacherState.teacher_id])
@dp.message_handler(text="👩‍🏫 O'qituvchilar", state="*")
async def get_actions_for_teachers(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.reply(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                 "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                            reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role != "admin":
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=teacher_actions_default_keyboard)




