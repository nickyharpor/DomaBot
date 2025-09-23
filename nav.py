from telethon import Button
from datetime import datetime, timedelta

def get_start_user_buttons(msg):
    return [[Button.inline(msg.get('get_recent_listing'),
                           b'get_recent_listing')],
            [Button.inline(msg.get('manage_subscription'),
                           b'manage_subscription')],
            [Button.inline(msg.get('search_domain'),
                           b'search_domain')],
            [Button.inline(msg.get('find_domains_by_owner'),
                           b'find_domains_by_owner')],
            [Button.inline(msg.get('settings'),
                           b'settings')],
            [Button.inline(msg.get('about'),
                           b'about')]]

def get_start_admin_buttons(msg):
    return get_start_user_buttons(msg)

def get_language_buttons(msg):
    return [[Button.inline(f'🇬🇧 {msg.get("english")}',
                           b'language:en')],
            [Button.inline(f'🇪🇸 {msg.get("spanish")}',
                           b'language:es')],
            [Button.inline(f'🇫🇷 {msg.get("french")}',
                           b'language:fr')],
            [Button.inline(f'🇵🇹 {msg.get("portuguese")}',
                           b'language:pt')],
            [Button.inline(f'🇷🇺 {msg.get("russian")}',
                           b'language:ru')],
            [Button.inline(f'🇸🇦 {msg.get("arabic")}',
                           b'language:ar')]]

def navigate(msg, current_page=1, total_pages=1, data_prefix=None, delimiter=':',
             mode='a'):
    current_page = int(current_page)
    total_pages = int(total_pages)
    if data_prefix:
        data_prefix += delimiter
        keyboard = []
        if mode == 'a':
            if current_page > 2:
                keyboard.append(Button.inline(msg.get('first'), str.encode(data_prefix + '1')))
            if current_page > 1:
                keyboard.append(Button.inline(msg.get('previous'), str.encode(data_prefix + str(current_page - 1))))
            if total_pages > 1:
                keyboard.append(Button.inline(str(current_page) + ' ' + msg.get('from') + ' ' + str(total_pages)))
            if total_pages > current_page:
                keyboard.append(Button.inline(msg.get('next'), str.encode(data_prefix + str(current_page + 1))))
            if total_pages > current_page + 1:
                keyboard.append(Button.inline(msg.get('last'), str.encode(data_prefix + str(total_pages))))
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

def list_domains(msg, domain_list, text, page=1, nav=None,
               prefix='info_domain', list_prefix='page_domain',
               delimiter=':'):
    keyboard = []
    domain_list.sort()
    if len(domain_list) >= page*10:
        for domain in domain_list[(page-1)*10:page*10]:
            keyboard.append([Button.inline(domain, str.encode(prefix + delimiter + domain))])
    elif len(domain_list) >= 10:
        for domain in domain_list[len(domain_list)-10:len(domain_list)]:
            keyboard.append([Button.inline(domain, str.encode(prefix + delimiter + domain))])
    else:
        for domain in domain_list:
            keyboard.append([Button.inline(domain, str.encode(prefix + delimiter + domain))])

    if not nav:
        nav = get_main_menu_button(msg)

    page_count = (len(domain_list) // 10) + 1

    buttons = paginate(msg,
                       current_page=page,
                       total_pages=page_count,
                       data_prefix=f'{list_prefix}{delimiter}{text}',
                       before=keyboard,
                       after=nav,
                       delimiter=delimiter)

    msg_text = f'{len(domain_list)} {msg.get("list_domains_text")}:'

    return msg_text, buttons



def list_listings(msg, dls, text=None, page=1, nav=None,
               prefix='get_recent_offers', list_prefix='get_recent_listing',
               delimiter=':'):
    keyboard = []
    listings = dls.get_listings(created_since=(datetime.now() - timedelta(days=7)).isoformat())
    c = 0
    for item in listings.get('items', []):
        c += 1
        price = int(item.get('price', 0))
        symbol = item.get('currency', {}).get('symbol', '???')
        decimals = int(item.get('currency', {}).get('decimals', '0'))
        name = item.get('name', '???.???')
        if round(price/(10^decimals)) > 10^12:
            pretty_price = round(price/(10^decimals))
        else:
            pretty_price = round(price / (10 ^ decimals), 4)
        keyboard.append([Button.inline(f'{name} ({pretty_price} {symbol})',
                                          str.encode(prefix + delimiter + str(name)))])

    if not nav:
        nav = get_main_menu_button(msg)

    page_count = 1

    buttons = paginate(msg,
                       current_page=page,
                       total_pages=page_count,
                       data_prefix=list_prefix,
                       before=keyboard,
                       after=nav,
                       delimiter=delimiter)
    return text, buttons