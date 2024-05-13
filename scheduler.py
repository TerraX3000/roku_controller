from crontab import CronTab
import requests
import json


def list_cron_jobs():
    cron = CronTab(user=True)
    # Iterate through all cron jobs
    for job in cron:
        # print(job.command)
        print(str(job))
        break
    return True


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


def add_cron_job(command, schedule):
    cron = CronTab(user=True)
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()


def get_automation_schedule():
    url = "https://riddleofthering.quest/app/static/automation_schedule.json"
    automation_schedule = json.loads(requests.get(url).content.decode())
    return automation_schedule


def main():
    # Example: add a job to run 'script.py' every day at 6 PM
    # 9 * * * * /home/kenkranz/roku_controller/.venv/bin/python3 /home/kenkranz/roku_controller/hello_world.py
    python_path = "/home/kenkranz/roku_controller/.venv/bin/python3"
    python_script = "/home/kenkranz/roku_controller/hello_world.py"
    cron_time = "42 * * * *"

    # add_cron_job(f"{python_path} {python_script}", cron_time)
    # list_cron_jobs()
    automation_schedule = get_automation_schedule()
    for program in automation_schedule:
        print(program)

    # remove_cron_job(f"{python_path} {python_script}", cron_time)
    # list_cron_jobs()


if __name__ == "__main__":
    main()
