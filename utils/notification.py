from utils.misc import is_termux, run_system_command


def notify(content, title):
    on_mobile = is_termux()
    if on_mobile:
        run_system_command(
            f"termux-notification -t '{title}' -c '{content}' --led-color '#a575ff' --priority 'high'",
            timeout=5, 
            retry=True
            )
    else:
        from plyer import notification
        from playsound3 import playsound

        notification.notify(
            title=title,
            message=content,
            app_icon=None,
            timeout=15
        )