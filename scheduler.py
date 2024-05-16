from crontab import CronTab
import requests
import json
import os
from utility_functions import send_log_info, get_app_config

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def get_python_command_path():
    python_venv_path = ".venv/bin/python3"
    python_command_path = os.path.join(SCRIPT_DIR, python_venv_path)
    return python_command_path


def get_python_script_path(script_name):
    python_script_name = script_name
    python_script_path = os.path.join(SCRIPT_DIR, python_script_name)
    return python_script_path


def get_saved_automation_schedule_path():
    saved_automation_schedule_file = "automation_schedule.json"
    saved_automation_schedule_path = os.path.join(
        SCRIPT_DIR, saved_automation_schedule_file
    )
    return saved_automation_schedule_path


def get_cron_job_command(
    python_command_path, python_script_path, arg_name=None, arg_value=None
):
    command = f"{python_command_path} {python_script_path}"
    if arg_name and arg_value:
        command = f"{command} --{arg_name} '{arg_value}'"
    return command


def add_roku_logger_cron_job():
    python_command_path = get_python_command_path()
    python_script_path = get_python_script_path("roku_logging.py")
    command = get_cron_job_command(python_command_path, python_script_path)
    schedule = "*/10 * * * *"
    comment = "roku_logger"
    add_cron_job(command, schedule, comment)
    return None


def add_scheduler_cron_job():
    python_command_path = get_python_command_path()
    python_script_path = get_python_script_path("scheduler.py")
    command = get_cron_job_command(python_command_path, python_script_path)
    schedule = "*/5 * * * *"
    comment = "scheduler"
    add_cron_job(command, schedule, comment)
    return None


def list_cron_jobs():
    cron = CronTab(user=True)
    # Iterate through all cron jobs
    for job in cron:
        # print(job.command)
        print(str(job))
        break
    return True


def remove_all_cron_jobs():
    cron = CronTab(user=True)
    for job in cron:
        cron.remove(job)
    cron.write()


def remove_cron_job(command, schedule):
    cron = CronTab(user=True)
    # Iterate through all cron jobs
    removed = False
    for job in cron:
        # Check if both command and schedule match
        if job.command == command and str(job) == schedule:
            cron.remove(job)
            removed = True
    if removed:
        cron.write()
        print(f"Removed cron job with command '{command}' and schedule '{schedule}'")
    else:
        print(
            f"No matching cron job found for command '{command}' and schedule '{schedule}'"
        )


def add_cron_job(command, schedule, comment):
    cron = CronTab(user=True)
    job = cron.new(command=command, comment=comment)
    job.setall(schedule)
    cron.write()


def get_automation_schedule():
    config = get_app_config()
    url = config["schedule_url"]
    automation_schedule = json.loads(requests.get(url).content.decode())
    return automation_schedule


def main():
    # Example: add a job to run 'script.py' every day at 6 PM
    saved_automation_schedule_path = get_saved_automation_schedule_path()
    if not os.path.exists(saved_automation_schedule_path):
        saved_schedule = {}
        with open(saved_automation_schedule_path, "w") as f:
            json.dump(saved_schedule, f)

    with open(saved_automation_schedule_path) as f:
        saved_schedule = json.load(f)

    automation_schedule = get_automation_schedule()
    log_entries = {"new_programs_added": 0, "programs_deleted": 0, "jobs_added": 0}
    schedule_changed = False
    for key in automation_schedule.keys():
        if key not in saved_schedule:
            log_entries["new_programs_added"] += 1
            schedule_changed = True

    for key in saved_schedule.keys():
        if key not in automation_schedule:
            log_entries["programs_deleted"] += 1
            schedule_changed = True

    if schedule_changed:
        with open(saved_automation_schedule_path, "w") as f:
            json.dump(automation_schedule, f)

        remove_all_cron_jobs()
        add_roku_logger_cron_job()
        add_scheduler_cron_job()

        python_command_path = get_python_command_path()
        python_script_path = get_python_script_path("run_roku.py")

        for counter, job in enumerate(automation_schedule.values(), start=1):
            program = job["name"]
            schedule = job["schedule"]
            comment = job["uid"]
            command = get_cron_job_command(
                python_command_path,
                python_script_path,
                arg_name="program",
                arg_value=program,
            )
            add_cron_job(command, schedule, comment)
            log_entries["jobs_added"] = counter

    else:
        print("no schedule changes!")

    if any(list(log_entries.values())):
        send_log_info(json.dumps(log_entries))


if __name__ == "__main__":
    main()
