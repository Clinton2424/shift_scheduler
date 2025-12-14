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
Demo video link= https://www.loom.com/share/ce75ccbaad564f36b08e1d68fc9b4463
You can access the deployed Streamlit application here:

https://shiftscheduler-gfgqcxdmp3w6hliqgdf7ae.streamlit.app/

The app allows users to generate an optimal weekly employee shift schedule based on staffing requirements, employee availability, and workload constraints.

pip install -r requirements.txt

streamlit run app.py
Analytics & Optimization Approach

This project applies prescriptive analytics using mathematical optimization.

Decision Variables

𝑥
𝑒
,
𝑠
=
1
x
e,s
	​

=1 if employee e is assigned to shift s, otherwise 0.

Constraints

Coverage constraints: each shift must meet required staffing levels.

Availability constraints: employees can only be assigned to shifts they are available for.

Workload constraints: each employee has a maximum number of shifts.

Fairness constraint: limits the maximum number of shifts assigned to any single employee.

Objective Function

The objective minimizes:

total understaffing across all shifts, and

imbalance in employee workload.

This is solved using OR-Tools CP-SAT, ensuring an optimal and interpretable schedule.

Technologies Used

Python

Streamlit

OR-Tools (CP-SAT solver)

Pandas


