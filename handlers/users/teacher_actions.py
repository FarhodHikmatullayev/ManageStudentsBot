from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.all_teachers import all_teachers_default_keyboard
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.change_profile_keyboards import next_change_default_keyboard
from keyboards.default.confirm_action_for_teachers import delete_teacher_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.default.teacher_actions import teacher_actions_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.teachers import DeleteTeacherState, CreateTeacherState, UpdateTeacherState


# for delete
@dp.message_handler(text="🗑️ O'chirish", state=DeleteTeacherState.teacher_id)
async def delete_teacher_final_function(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print('data', data)
    teacher_id = data.get("teacher_id")
    teachers = await db.select_users(role='teacher', id=teacher_id)
    if teachers:
        user_id = teachers[0]['id']
        await db.update_user(user_id=user_id, role='user')
        await message.answer(text="📣 O'qituvchi muvaffaqiyatli o'chirildi ✅", reply_markup=back_to_menu)
    else:
        await message.answer(text="📢 Bu O'qituvchi allaqachon o'chirilgan", reply_markup=back_to_menu)
    await state.finish()


@dp.message_handler(text="🗑️ O'qituvchini o'chirish", state="*")
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
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            markup = await all_teachers_default_keyboard()
            await message.answer(text="O'chirmoqchi bo'lgan o'qituvchini tanlang 👇", reply_markup=markup)
            await DeleteTeacherState.teacher_id.set()


@dp.message_handler(text="🔙 Orqaga", state=DeleteTeacherState.teacher_id)
async def back_to_actions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Kerakli amalni tanlang 👇", reply_markup=teacher_actions_default_keyboard)


@dp.message_handler(text="🔙 O'qituvchilarga qaytish", state=DeleteTeacherState.teacher_id, user_id=ADMINS)
async def back_to_groups_list(message: types.Message, state: FSMContext):
    markup = await all_teachers_default_keyboard()
    await message.answer(text="O'chirmoqchi bo'lgan o'qituvchini tanlang 👇", reply_markup=markup)
    await DeleteTeacherState.teacher_id.set()


@dp.message_handler(state=DeleteTeacherState.teacher_id)
async def delete_teacher(message: types.Message, state: FSMContext):
    teacher_full_name = message.text

    teachers = await db.select_users(full_name=teacher_full_name, role='teacher')
    if not teachers:
        await message.answer(text="⚠️ O'qituvchi topilmadi", reply_markup=go_back_default_keyboard)
        return
    teacher = teachers[0]
    await state.update_data(teacher_id=teacher['id'])

    text = (f"📚 O'qituvchi ma'lumotlari 👇\n"
            f"👨‍🏫 F.I.Sh: {teacher_full_name}\n")
    await message.answer(text=text)
    await message.answer(text="💬 O'qituvchini o'chirasizmi?\n"
                              "O'chirish tumasini bosing 👇", reply_markup=delete_teacher_default_keyboard)


# for create
@dp.message_handler(text="➕ O'qituvchi qo'shish", state="*")
async def start_adding_teacher(message: types.Message, state: FSMContext):
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
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
            return
        else:
            markup = await all_users_default_keyboard()
            await message.answer(
                text="🆕 Yangi o'qituvchi qo'shish uchun foydalanuvchilardan birini tanlang: 👇",
                reply_markup=markup
            )
            await CreateTeacherState.first_name.set()


@dp.callback_query_handler(text='yes', state=CreateTeacherState.first_name)
async def save_teacher(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    user = await db.update_user(
        user_id=user_id,
        role='teacher'
    )

    await call.message.answer(text="✅ O'qituvchi qo'shildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateTeacherState.first_name, text="no")
async def cancel_saving_teacher(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="🔴 Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateTeacherState.first_name)
async def get_teacher_full_name(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    try:
        first_name = teacher_full_name.split()[0]
        last_name = teacher_full_name.split()[1]
    except:
        await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi", reply_markup=go_back_default_keyboard)
        return
    users = await db.select_users(full_name=teacher_full_name)
    if not users:
        await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi",
                             reply_markup=go_back_default_keyboard)
        return

    await state.update_data(first_name=first_name, last_name=last_name, user_id=users[0]['id'])
    text = (f"📚 O'qituvchi ma'lumotlari quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 F.I.Sh: {teacher_full_name}\n")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)


# for update
@dp.message_handler(text="✏️ O'qituvchini o'zgartirish", state="*")
async def start_adding_teacher(message: types.Message, state: FSMContext):
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
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
            return
        else:
            markup = await all_teachers_default_keyboard()
            await message.answer(
                text="🆕 O'qituvchini o'zgartirish uchun ulardan birin tanlang: 👇",
                reply_markup=markup
            )
            await UpdateTeacherState.teacher_id.set()


@dp.message_handler(state=UpdateTeacherState.teacher_id)
async def get_teacher_id(message: types.Message, state: FSMContext):
    teacher_full_name = message.text
    try:
        first_name = teacher_full_name.split()[0]
        last_name = teacher_full_name.split()[1]
    except:
        await message.answer(text="⚠️ Bunday o'qituvchi topilmadi", reply_markup=go_back_default_keyboard)
        return
    teachers = await db.select_users(full_name=teacher_full_name, role="teacher")
    if not teachers:
        await message.answer(text="⚠️ Bunday o'qituvchi topilmadi",
                             reply_markup=go_back_default_keyboard)
        return

    await state.update_data(
        first_name=first_name,
        last_name=last_name,
        teacher_id=teachers[0]['id'],
    )
    await message.answer(text="🔤 O'qituvchi uchun yangi ism kiriting:\n"
                              "❌ Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherState.first_name.set()


@dp.message_handler(state=UpdateTeacherState.first_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.first_name)
async def get_teacher_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    if first_name != "Keyingi 🔜":
        await state.update_data(first_name=first_name)
    await message.answer(text="🔤 O'qituvchi uchun yangi familiya kiriting:\n"
                              "❌ Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmasini bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await UpdateTeacherState.last_name.set()


@dp.callback_query_handler(text='yes', state=UpdateTeacherState.last_name)
async def update_teacher(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get('teacher_id')
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    user = await db.update_user(
        user_id=teacher_id,
        full_name=f"{first_name} {last_name}",
    )

    await call.message.answer(text="✅ O'qituvchi o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=UpdateTeacherState.last_name, text="no")
async def cancel_updating_teacher(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'zgartirish rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateTeacherState.last_name, text="Keyingi 🔜")
@dp.message_handler(state=UpdateTeacherState.last_name)
async def get_teacher_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    if last_name != "Keyingi 🔜":
        print('last_name', last_name)
        await state.update_data(last_name=last_name)
    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    teacher_full_name = f"{first_name} {last_name}"
    text = (f"📚 O'qituvchi ma'lumotlari quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 F.I.Sh: {teacher_full_name}\n")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)
