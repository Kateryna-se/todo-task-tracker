import datetime

# Чтение задач из файла
def read_file():
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []
    
# Сохранение задач в файл    
def save_file(to_do_list):
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in to_do_list:
            file.write(task + "\n")

# Сохранение статистики выполненных задач
def save_done_stats(tasks):
    done_count = len([t for t in tasks if t.startswith("✅")])
    with open("done_stats.txt", "w",  encoding="utf-8") as file:
        file.write(f"Tasks completed: {done_count}\n")

# Показать задачи на сегодня с дедлайнами
def tasks_for_today(task_list):
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    now = datetime.datetime.now()
    print(f"\n📆 Tasks for {today}:")

    reminder_shown = False
    for task in task_list:
        # Проверка дедлайна
        if "📅" in task:
            try:
                deadline_str = task.split("📅")[-1].strip(" )")
                deadline = datetime.datetime.strptime(deadline_str, "%d.%m.%Y %H:%M")
                remaining = deadline - now
                if remaining.days >= 0:
                    if not reminder_shown:
                        print("\n⏰ Remaining time before deadlines:")
                        reminder_shown = True
                    print(f"🔔 {remaining.days} days left — {task}")
            except:
                continue

    found_today = False
    for task in task_list:
        if today in task:
            print("🔸", task)
            found_today = True
    if not found_today:
        print("No tasks for today ✨")

# Главное меню
tasks = read_file()

while True:
    print("\n📝 Your to_do list:")
    print("1. View all tasks")
    print("2. Add task")
    print("3. Delete task")
    print("4. Mark the task as completed ✅")
    print("5. Show tasks for today 📆")
    print("6. Exit\n")

    choice = input("Choose an action (1-6): ")

    if choice =="1":
        if tasks:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        else:
            print("No tasks yet!")

    elif choice == "2":
        task_text = input("Enter a new task: ")
        deadline_input = input("Enter a deadline (dd.mm.yyyy HH:MM): ")
        try:
            deadline = datetime.datetime.strptime(deadline_input, "%d.%m.%Y %H:%M")
        except ValueError:
            print("⚠ Invalid date format. Try again.")
            continue
        time_added = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        full_task = f"{task_text} (🕒 {time_added} 📅 {deadline_input})"
        tasks.append(full_task)
        save_file(tasks)
        print("✅ Task added!")

    elif choice == "3":
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        number = int(input("Enter the number of the task to delete: "))
        if 0 < number <= len(tasks):
            removed = tasks.pop(number - 1)
            save_file(tasks)
            print(f"❌ Task \"{removed}\" removed.")
        else:
            print("⚠ Invalid number.")

    elif choice == "4":
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        number = int(input("Enter the number of the completed task: "))
        if 0 < number <= len(tasks):
            tasks[number - 1] = "✅ " + tasks[number - 1]
            save_file(tasks)
            save_done_stats(tasks)
            print("🎉 Task marked as completed!")
        else:
                print("⚠ Invalid number.")
    
    elif choice == "5":
        tasks_for_today(tasks)

    elif choice == "6":
        print("See you later! 😊")
    else:
        print("❗Invalid choice. Try again. ")