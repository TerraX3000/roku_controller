from roku import Roku
from utility_functions import send_log_info, get_app_config

config = get_app_config()
roku_ip_address = config.get("roku_ip_address")
roku = Roku(roku_ip_address)


def add_heartbeat_log():
    config = get_app_config()
    logger_url = config.get("logger_url")
    try:
        roku_active_app = roku.active_app
    except:
        roku_active_app = "unable to get Roku active app"
    log_entry = f"Roku Active App | {roku_active_app}"
    url = logger_url + "&log=" + log_entry
    print(url)
    send_log_info(log_entry)


add_heartbeat_log()
