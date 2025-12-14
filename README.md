\# Employee Shift Scheduler (Optimization) — Prescriptive Analytics



\## Problem

Creating weekly employee schedules is hard because you must meet staffing needs while respecting employee availability and workload limits.



\## Solution

This app builds an optimal weekly schedule (Mon–Sun, Morning/Evening) using optimization. Users set:

\- number of employees

\- required workers per shift

\- max shifts per employee

\- availability (0/1 table)



The app returns:

\- the recommended schedule (who works which shift)

\- understaffing per shift (if constraints make full coverage impossible)

\- a fairness metric (maximum shifts assigned to any employee)



\## Optimization Model

Decision variable:

\- x\[e,s] = 1 if employee e is assigned to shift s, else 0



Constraints:

\- Coverage: sum\_e x\[e,s] + understaff\[s] >= need\[s]

\- Availability: x\[e,s] = 0 if employee e is not available for shift s

\- Max shifts: sum\_s x\[e,s] <= max\_shifts\[e]

\- Fairness helper: sum\_s x\[e,s] <= t for all employees



Objective:

\- Minimize (1000 \* total understaffing) + (10 \* t)



\## Tech Stack

\- Python

\- Streamlit (web app)

\- OR-Tools CP-SAT (optimization)

\- Pandas



\## Run Locally

```bash

pip install -r requirements.txt

streamlit run app.py



