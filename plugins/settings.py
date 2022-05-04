from pyrogram import emoji
from database import database
from pystark import Stark, Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Stark.cmd('settings', description='تكوين إعدادات البوت الشخصية.', private_only=True)
async def settings(_, msg: Message):
    text, markup = await user_settings(msg.from_user.id)
    await msg.react(text, reply_markup=markup)


async def user_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    tick = ' ✔'
    cross = ' ✖️ '
    ask_emojis = "Ask for Emojis"
    ask_emojis_msg = f"اضبطهـا على ✓ إذا كنت تريد أن يطلب البوت الرموز التعبيرية التي سيتم تعيينها على ملصق الفيديو أثناء الإضافة إلى الحزمة. إذا تم التعيين على × ، فستستخدم جميع الملصقات الرموز التعبيرية الافتراضية ، وهي - {emoji.RED_HEART}"
    get_webm = "Get WEBM"
    get_webm_msg = f"اضبطهـا على ✓ إذا كنت تريد الحصول على ملفات webm عند إرسال أي ملصق فيديو موجود. بهذه الطريقة ، يمكنك إضافة ملصقات من حزم الأشخاص الآخرين باستخدام الملصقات. إذا كان خطأ ، سيتجاهل البوت الملصق."
    kang_mode = "Kang Mode"
    kang_mode_msg = "اضبطهـا على ✓ إذا كنت تريد إضافة ملصقات إلى حزمتك عن طريق إرسال ملصق فيديو من حزمة موجودة. بهذه الطريقة ، يمكنك إضافة ملصقات من حزم أشخاص آخرين إلى حزمك. إذا كان × ، سيتجاهل البوت الملصق"
    default_emojis = "Default Emojis"
    default_emojis_msg = f"قم بتعيين الرموز التعبيرية الافتراضية لاستخدامها في ملصقاتك. إذا لم يتم تعيين شيء, {emoji.RED_HEART} سوف يستخدم."
    text = f'**الاعـدادات** \n\n'
    ask_emojis_db = data['ask_emojis']
    get_webm_db = data['get_webm']
    kang_mode_db = data['kang_mode']
    default_emojis_db = data['default_emojis']
    general_text = "**{}** : {} \n{} \n\n"
    if ask_emojis_db:
        text += general_text.format(ask_emojis, 'True', ask_emojis_msg)
        ask_emojis += tick
    else:
        text += general_text.format(ask_emojis, 'False', ask_emojis_msg)
        ask_emojis += cross
    if get_webm_db:
        text += general_text.format(get_webm, 'True', get_webm_msg)
        get_webm += tick
    else:
        text += general_text.format(get_webm, 'False', get_webm_msg)
        get_webm += cross
    if kang_mode_db:
        text += general_text.format(kang_mode, 'True', kang_mode_msg)
        kang_mode += tick
    else:
        text += general_text.format(kang_mode, 'False', kang_mode_msg)
        kang_mode += cross
    if default_emojis_db:
        text += general_text.format(default_emojis, default_emojis_db, default_emojis_msg)
        default_emojis += ' - SET'
    else:
        text += general_text.format(default_emojis, 'Not Set', default_emojis_msg)
        default_emojis += ' - NOT SET'
    text += '- استخدم الأزرار أدناه لتغيير القيم.'
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(ask_emojis, callback_data="emojis")],
        [InlineKeyboardButton(default_emojis, callback_data="default_emojis")],
        [InlineKeyboardButton(kang_mode, callback_data="kang_mode")],
        [InlineKeyboardButton(get_webm, callback_data="webm")],
    ])
    return text, markup


async def default_emojis_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    data = data['default_emojis']
    if data:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('تغييـر الايموجيـات', callback_data="change_default_emojis")],
            [InlineKeyboardButton('حـذف الايموجـي الاسـاسي', callback_data="remove_default_emojis")],
            [InlineKeyboardButton('<-- رجـوع', callback_data="back")],
        ])
        text = f'- الرموز التعبيرية الافتراضية الحالية هي `{data}` \n\n- استخدم الأزرار أدناه لتغييرها أو إزالتها'
    else:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('اضـافه ايموجيـات', callback_data="change_default_emojis")],
            [InlineKeyboardButton('<-- رجـوع', callback_data="back")],
        ])
        text = 'لم يتم تعيين رموز تعبيرية حاليًا. استخدم الزر أدناه لإضافتهم.'
    return text, markup
