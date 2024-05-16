from crontab import CronTab
import requests
import json
import os
from utility_functions import send_log_info_to_streamlit


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
    url = "https://riddleofthering.quest/app/static/automation_schedule.json"
    automation_schedule = json.loads(requests.get(url).content.decode())
    return automation_schedule


def main():
    # Example: add a job to run 'script.py' every day at 6 PM
    script_dir = os.path.dirname(os.path.realpath(__file__))
    python_venv_path = ".venv/bin/python3"
    python_command_path = os.path.join(script_dir, python_venv_path)
    python_script_name = "run_roku.py"
    python_script_path = os.path.join(script_dir, python_script_name)
    saved_automation_schedule_file = "automation_schedule.json"
    saved_automation_schedule_path = os.path.join(
        script_dir, saved_automation_schedule_file
    )
    print(python_command_path)
    print(python_script_path)
    if not os.path.exists(saved_automation_schedule_path):
        saved_schedule = {}
        with open(saved_automation_schedule_path, "w") as f:
            json.dump(saved_schedule, f)

    with open(saved_automation_schedule_path) as f:
        saved_schedule = json.load(f)

    automation_schedule = get_automation_schedule()
    log_entries = {"new_program_found": 0, "program_deleted": 0, "jobs_added": 0}
    schedule_changed = False
    for key in automation_schedule.keys():
        if key not in saved_schedule:
            log_entries["new_program_found"] += 1
            schedule_changed = True

    for key in saved_schedule.keys():
        if key not in automation_schedule:
            log_entries["program_deleted"] += 1
            schedule_changed = True

    if schedule_changed:
        with open(saved_automation_schedule_path, "w") as f:
            json.dump(automation_schedule, f)
        remove_all_cron_jobs()
        for counter, job in enumerate(automation_schedule.values(), start=1):
            program = job["name"]
            schedule = job["schedule"]
            comment = job["uid"]
            command = (
                f"{python_command_path} {python_script_path} --program '{program}'"
            )
            add_cron_job(command, schedule, comment)
            log_entries["jobs_added"] = counter
    else:
        print("no schedule changes!")
    if any(list(log_entries.values())):
        send_log_info_to_streamlit(json.dumps(log_entries))


if __name__ == "__main__":
    main()
