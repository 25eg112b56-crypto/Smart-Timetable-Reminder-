import streamlit as st
import datetime

st.set_page_config(page_title="Smart Timetable Assistant")

st.title("📅 Smart Timetable & Reminder Assistant")

name = st.text_input("Enter Your Name")
class_time = st.text_input("Class Timings (Example: Mon–Fri 9AM–4PM)")

st.markdown("### 🗓 Select Study Days")
days_selected = st.multiselect(
    "Choose days for study timetable",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

free_start = st.time_input("Daily Free Time Start")
free_end = st.time_input("Daily Free Time End")

break_minutes = st.number_input("Break time between tasks (minutes)", min_value=5, max_value=60, value=10)

st.markdown("### 📚 Enter Your Tasks")

tasks = []
dates = []

for i in range(1, 6):
    task = st.text_input(f"Task {i}")
    date = st.date_input(f"Due Date {i}", key=f"date{i}")
    if task:
        tasks.append(task)
        dates.append(date)

if st.button("Generate Smart Timetable"):

    today = datetime.date.today()

    st.markdown("## 🎯 Your Smart Weekly Timetable")

    st.write("**Name:**", name)
    st.write("**Class Timings:**", class_time)
    st.write("**Free Time:**", free_start, "-", free_end)
    st.write("**Selected Days:**", ", ".join(days_selected))

    start_dt = datetime.datetime.combine(today, free_start)
    end_dt = datetime.datetime.combine(today, free_end)

    total_minutes = int((end_dt - start_dt).total_seconds() / 60)

    if len(tasks) == 0 or len(days_selected) == 0:
        st.warning("Please select at least one task and one day")
    else:
        total_break_time = break_minutes * (len(tasks) - 1)
        study_minutes = total_minutes - total_break_time

        if study_minutes <= 0:
            st.error("Not enough time after breaks. Reduce break time or increase free time.")
        else:
            slot = study_minutes // len(tasks)

            for day in days_selected:
                st.markdown(f"### 🗓 {day} Timetable")

                current = start_dt

                for i, task in enumerate(tasks):
                    next_time = current + datetime.timedelta(minutes=slot)
                    st.write(f"{current.time()} – {next_time.time()}  ➝  {task}")
                    current = next_time

                    if i < len(tasks) - 1:
                        break_end = current + datetime.timedelta(minutes=break_minutes)
                        st.write(f"{current.time()} – {break_end.time()}  ➝  Break 💤")
                        current = break_end

    st.markdown("### ⏰ Reminders")

    for i in range(len(tasks)):
        days = (dates[i] - today).days
        st.write(f"• {tasks[i]} due in {days} days")