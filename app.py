import streamlit as st
import pandas as pd
from ortools.sat.python import cp_model

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SHIFTS = ["Morning", "Evening"]

def build_shifts():
    return [f"{d}-{sh}" for d in DAYS for sh in SHIFTS]

def solve_schedule(employees, max_shifts, need, availability):
    shifts = build_shifts()
    model = cp_model.CpModel()

    # Decision vars
    x = {}
    for e in employees:
        for s in shifts:
            x[(e, s)] = model.NewBoolVar(f"x_{e}_{s}")

    # Understaffing
    u = {s: model.NewIntVar(0, 1000, f"u_{s}") for s in shifts}

    # Fairness helper
    t = model.NewIntVar(0, len(shifts), "t")

    # Coverage
    for s in shifts:
        model.Add(sum(x[(e, s)] for e in employees) + u[s] >= need[s])

    # Availability
    for e in employees:
        for s in shifts:
            if availability.loc[e, s] == 0:
                model.Add(x[(e, s)] == 0)

    # Max shifts + fairness
    for e in employees:
        total = sum(x[(e, s)] for s in shifts)
        model.Add(total <= max_shifts[e])
        model.Add(total <= t)

    # Objective
    model.Minimize(1000 * sum(u[s] for s in shifts) + 10 * t)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, None

    schedule = pd.DataFrame(0, index=employees, columns=shifts)
    for e in employees:
        for s in shifts:
            schedule.loc[e, s] = solver.Value(x[(e, s)])

    understaff = pd.Series({s: solver.Value(u[s]) for s in shifts})
    t_val = solver.Value(t)

    return schedule, understaff, t_val

st.title("Employee Shift Scheduler (Optimization)")

st.sidebar.header("Inputs")

n_employees = st.sidebar.slider("Number of employees", 3, 20, 8)
employees = [f"E{i+1}" for i in range(n_employees)]

default_max = st.sidebar.slider("Default max shifts per employee", 1, 14, 5)

st.sidebar.subheader("Staffing requirements")
need_morning = st.sidebar.slider("Workers needed per Morning shift", 1, 10, 2)
need_evening = st.sidebar.slider("Workers needed per Evening shift", 1, 10, 2)

shifts = build_shifts()
need = {}
for s in shifts:
    need[s] = need_morning if s.endswith("Morning") else need_evening

st.sidebar.subheader("Max shifts per employee")
max_shifts = {}
for e in employees:
    max_shifts[e] = st.sidebar.number_input(f"{e} max shifts", 0, 14, default_max)

st.subheader("Availability (1 = available, 0 = not available)")
availability = pd.DataFrame(1, index=employees, columns=shifts)
availability = st.data_editor(availability, use_container_width=True)

if st.button("Solve Schedule"):
    schedule, understaff, t_val = solve_schedule(employees, max_shifts, need, availability)

    if schedule is None:
        st.error("No feasible solution found. Try adjusting availability or max shifts.")
    else:
        st.success("Optimal schedule found")

        st.subheader("Schedule (1 = assigned)")
        st.dataframe(schedule, use_container_width=True)

        st.subheader("Understaffing by shift")
        st.dataframe(understaff.to_frame("Understaff"), use_container_width=True)

        st.subheader("Fairness metric")
        st.write(f"Maximum shifts assigned to any employee: {t_val}")

        st.download_button(
            "Download schedule as CSV",
            schedule.to_csv().encode("utf-8"),
            file_name="schedule.csv",
            mime="text/csv"
        )
