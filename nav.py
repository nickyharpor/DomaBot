from telethon import Button

def get_start_user_buttons(msg):
    return [[Button.inline(msg.get('manage_event_subscription'),
                           b'manage_event_subscription')],
            [Button.inline(msg.get('about'),
                           b'about')]]

def get_start_admin_buttons(msg):
    return get_start_user_buttons(msg)