from roku import Roku
from time import sleep
import argparse
from utility_functions import get_app_config, send_log_info


config = get_app_config()
roku_ip_address = config.get("roku_ip_address")
roku = Roku(roku_ip_address)


def run_diagnostics():
    print("====DIAGNOSTIC INFO====")
    print("ACTIVE APP:", roku.active_app)
    # roku.info()
    for app in roku.apps:
        app_functions = []
        for fn in dir(app):
            app_functions.append(fn)
        print("====APP PROPERTIES AND FUNCTIONS====")
        print(" | ".join(app_functions))
        break
    print("=====ROKU COMMANDS====")
    print(roku.commands)


def run_dev_channel(program):
    def launch_dev_channel():
        print("start: launch_dev_channel")
        roku.poweron()
        sleep(10)
        dev_channel = roku["dev"]
        dev_channel.launch()
        sleep(5)
        print("finish: launch_dev_channel")

    def go_to_video(clicks=0, down_first=False):
        print("start: go_to_video")
        if clicks:
            if down_first:
                sleep(1)
                roku.down()
                sleep(1)
            for click in range(clicks):
                print(click)
                roku.select()
                sleep(1)
            roku.up()
            sleep(1)
        print("finish: go_to_video")

    if program == "Program 1":
        launch_dev_channel()
        roku.select()

    if program == "Program 2":
        launch_dev_channel()
        go_to_video(clicks=1, down_first=True)
        roku.select()

    if program == "Program 3":
        launch_dev_channel()
        go_to_video(clicks=2, down_first=True)
        roku.select()

    if program == "Program Loop":
        number_of_plays = 4
        launch_dev_channel()
        roku.select()
        sleep(10)
        for this_iteration in range(1, number_of_plays):
            print("this_iteration", this_iteration)
            roku.back()
            go_to_video(clicks=1, down_first=True)
            roku.select()
            sleep(10)
        roku.home()
        sleep(5)


def run_youtube():
    youtube_channel = roku["YouTube"]
    youtube_channel.launch()
    sleep(7)
    roku.back()
    sleep(5)
    sleep(1)
    roku.left()
    sleep(1)
    for i in range(5):
        roku.down()
        sleep(1)
    for i in range(3):
        roku.right()
        sleep(1)
    roku.select()
    roku.right()
    sleep(1)
    roku.right()
    sleep(1)
    roku.select()
    sleep(1)
    roku.left()
    sleep(1)
    roku.down()
    sleep(1)
    roku.select()
    for i in range(60):
        print(i)
        sleep(1)
    roku.home()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", dest="program", type=str, help="Add program")
    args = parser.parse_args()
    program = args.program
    if program:
        send_log_info(f"Running {program}")
        print(program)
    if program in ["Program 1", "Program 2", "Program 3", "Program Loop"]:
        print("running dev channel")
        run_dev_channel(program)
    elif program == "Program 4":
        roku.poweron()
        sleep(10)
        pluto_app = roku[74519]
        pluto_app.launch()
        # sleep(5)
        # roku.down()
        # sleep(1)
        # roku.select()
    elif program == "Program 5":
        roku.poweron()
        sleep(10)
        sling_app = roku[46041]
        sling_app.launch()
    elif program == "Program 6":
        roku.poweron()
        sleep(10)
        run_youtube()
    elif program == "Power Off":
        roku.poweroff()

    else:
        run_diagnostics()


run()
