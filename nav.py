from telethon import Button

def get_start_user_buttons(msg):
    return [[Button.inline(msg.get('get_recent_listing'),
                           b'get_recent_listing')],
            [Button.inline(msg.get('get_recent_offers'),
                           b'get_recent_offers')],
            [Button.inline(msg.get('manage_event_subscription'),
                           b'manage_event_subscription')],
            [Button.inline(msg.get('about'),
                           b'about')]]

def get_start_admin_buttons(msg):
    return get_start_user_buttons(msg)

def navigate(msg, current_page=1, total_pages=1, data_prefix=None, delimiter=':',
             mode='a'):
    current_page = int(current_page)
    total_pages = int(total_pages)
    if data_prefix:
        data_prefix += delimiter
        keyboard = []
        if mode == 'a':
            if total_pages > current_page + 1:
                keyboard.append(Button.inline(msg.get('last'), str.encode(data_prefix + str(total_pages))))
            if total_pages > current_page:
                keyboard.append(Button.inline(msg.get('next'), str.encode(data_prefix + str(current_page + 1))))
            if total_pages > 1:
                keyboard.append(Button.inline(str(current_page) + ' ' + msg.get('from') + ' ' + str(total_pages)))
            if current_page > 1:
                keyboard.append(Button.inline(msg.get('previous'), str.encode(data_prefix + str(current_page - 1))))
            if current_page > 2:
                keyboard.append(Button.inline(msg.get('first'), str.encode(data_prefix + '1')))
        return keyboard
    else:
        return None

def paginate(msg, current_page=1, total_pages=1, data_prefix=None, delimiter=':',
             before=None, after=None):
    if data_prefix:
        paginator = navigate(msg, current_page, total_pages, data_prefix, delimiter)
        if before or after:
            paginator = [paginator]
        if before:
            paginator = before + paginator
        if after:
            paginator.append(after)
        return paginator
    else:
        return None

def get_main_menu_button(msg):
    return [Button.inline(msg.get('main_menu'), b'main_menu')]

def get_clear_button():
    return Button.clear()

def list_listings(db, msg, dls, text=None, page=1, nav=None,
               prefix='view_progress_report', list_prefix='list_progress_reports',
               delimiter=':', employee=None):
    response_text = 'Latest domains listed:'
    listings = dls.get_listings()
    for item in listings.get('items', []):
        price = int(item.get('price', 0))
        symbol = item.get('currency', {}).get('symbol', '???')
        decimals = item.get('currency', {}).get('decimals', 0)
        name = item.get('name', '???.???')
        if decimals > 0:
            price = round(price / decimals, 4)
        button_text = f'{name} ({price} {symbol})'

    q = None
    page_count = db.page_count('progress_report', query=q)
    progress_reports = db.find('progress_report', query=q, page=page, sort_by='submission_time')
    keyboard, tmp_keyboard = [], []

    if not text:
        text = msg.get('latest_progress_reports')
        text += ':\n'

    for c, progress_report in enumerate(progress_reports):
        tmp_keyboard.append(Button.inline('',
                                          str.encode(prefix + delimiter + str(progress_report.get('_id')))))
        if True:  # c % 2 != 0:
            keyboard.append(tmp_keyboard)
            tmp_keyboard = []

    if len(tmp_keyboard) != 0:
        keyboard.append(tmp_keyboard)

    if not nav:
        nav = get_main_menu_button(msg)

    buttons = paginate(msg,
                       current_page=page,
                       total_pages=page_count,
                       data_prefix=list_prefix,
                       before=keyboard,
                       after=nav,
                       delimiter=delimiter)
    return text, buttons