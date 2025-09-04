from typing import Literal
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def classify_subject(prompt: str) -> Literal["employee", "timesheet", "classic", "unknown"]:
    model = genai.GenerativeModel(os.getenv("ROUTER_MODEL", "gemini-1.5-flash"))
    res = model.generate_content(
        f"""
Classify the user prompt into one of: employee, timesheet, classic, unknown.

- employee:
    Any questions, requests, or information related to employees, such as:
    * Personal information: first name, last name, full name, gender, date of birth, age.
    * Identification data: employee code, ID, username.
    * Group, department, position, job title, team, division, work location.
    * Contact details: email, phone number, address.
    * Demographics: nationality, marital status, gender, age group.
    * Qualifications, skills, education, certifications, work experience.
    * Salary, bonuses, benefits, allowances.
    * Analytics: years of service, gender ratio, group distribution, average age.
    * Any other attributes related to an employee’s profile or identity.

- timesheet:
    Any questions, requests, or information related to attendance and working hours, such as:
    * Employee name (linked to attendance records).
    * Work date, month, year.
    * Check-in time, check-out time, total hours worked, OT.
    * Attendance status: on time, late, absent, on leave.
    * Total working hours, overtime, work shifts.
    * Analytics: on-time arrival rate, total working days, leave days, diligence score, productivity.
    * Comparisons or statistics across employees or groups.
    * Any data related to time tracking or work schedules.
    "Definitions: "
        "- An employee is considered 'on time' if they check in before 8:30 AM; otherwise, they are 'late'. "
        "- An employee has worked 'full hours' if the total time between check-in and check-out is at least 9 hours. "
        "- A 'hardworking' employee is one who works full hours or more. "
        "- An employee is OT if they check out **after** 5:00 PM"
        "You can compute aggregates, totals, averages, durations, or generate lists strictly from retrieved records. "
        "Typical tasks include analyzing check-in/check-out times, total hours worked, late arrivals, absences, overtime, "
        "on-time rates, and productivity trends. "
        "Respond concisely and focus on the requested statistics or insights."
    - For the timesheet result, response the number of matching instead of list all the result.
- classic:
    Questions belonging to the “classic” category as defined by the system.

- unknown:
    Any other content not fitting the categories above.

Reply with only one token: employee|timesheet|classic|unknown.
Prompt: {prompt}
"""

    )
    text = (res.text or "").strip().lower()
    if text not in {"employee", "timesheet", "classic"}:
        return "unknown"
    return text  # type: ignore


