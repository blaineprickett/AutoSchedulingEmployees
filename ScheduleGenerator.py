import csv

class Employee:
    def __init__(self, name, position, availability, preferences):
        self.name = name
        self.position = position
        self.availability = availability  # Now a dictionary like {'Monday': ['Day', 'Night'], 'Tuesday': ['Night']}
        self.preferences = preferences
        self.hours_assigned = 0

class Scheduler:
    def __init__(self, business_needs):
        self.business_needs = business_needs
        self.schedule = {day: {time: {position: [] for position, count in business_needs[day][time].items()} for time in business_needs[day].keys()} for day in business_needs.keys()}

    def assign_shift(self, employee, day, time):
        if time == "Day":
            hours = 7.5
        elif time == "Night":
            hours = 7
        else:  # SundayNight
            hours = 7.5

        # Check if adding the shift will exceed a Student Worker's 20-hour limit
        if employee.position == "Student Worker" and employee.hours_assigned + hours > 20:
            return False

        if len(self.schedule[day][time][employee.position]) < self.business_needs[day][time][employee.position]:
            self.schedule[day][time][employee.position].append(employee.name)
            employee.hours_assigned += hours
            return True
        return False

    def create_schedule(self, employees):
        for day, times in self.business_needs.items():
            for time, positions in times.items():
                # First, try to accommodate employee preferences
                for employee in employees:
                    if day in employee.availability and time in employee.availability[day] and time in employee.preferences:
                        self.assign_shift(employee, day, time)

                # Then, fill remaining shifts based on availability
                for position, need in positions.items():
                    for employee in employees:
                        if day in employee.availability and time in employee.availability[day] and len(self.schedule[day][time][position]) < need and employee.name not in self.schedule[day][time][position] and employee.position == position:
                            self.assign_shift(employee, day, time)

        return self.schedule

def count_day_shifts(schedule, employee):
    count = 0
    for day, times in schedule.items():
        for time, positions in times.items():
            if time == "Day":
                for position, employees in positions.items():
                    if employee in employees:
                        count += 1
    return count

def export_schedule_to_csv(schedule, employees_list, filename='schedule.csv'):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
    time_slots = {
        'Day': '8:30 AM - 4:00 PM',
        'Night': '3:30 PM - 10:30 PM',
        'SundayNight': '1:00 PM - 8:30 PM',
    }
    
    # Create a dictionary of employee names to their positions using the list of Employee objects
    unique_employees = {employee.name: employee.position for employee in employees_list}

    # Sort employees by the number of day shifts they have, in descending order
    sorted_employees = sorted(unique_employees, key=lambda x: count_day_shifts(schedule, x), reverse=True)

    rows = []
    for employee_name in sorted_employees:
        row = [employee_name, unique_employees[employee_name]]
        for day in days:
            shifts = []
            for time, time_label in time_slots.items():
                if (day == 'Sunday' and time == 'Night'):
                    time_label = time_slots['SundayNight']  # Use Sunday's unique time slot
                if time == 'SundayNight' and day != 'Sunday':
                    continue
                roles = [role for role, names in schedule[day].get(time, {}).items() if employee_name in names]
                if roles:
                    shifts.append(time_label)
            row.append(', '.join(shifts))
        rows.append(row)

    headers = ['Employee Name', 'Position'] + days

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

# Example usage
marisa = Employee("Marisa", "Supervisor", {'Monday': ['Night'], 'Tuesday': ['Night'], 'Wednesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Night'])
ashley = Employee("Ashley", "Team Lead", {'Monday': ['Day'], 'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day'])
shala = Employee("Shala", "Cook", {'Monday': ['Day'], 'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day'])
shauntel = Employee("Shauntel", "Food Service Worker", {'Monday': ['Day'], 'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day'])
silicia = Employee("Silicia", "Food Service Worker", {'Monday': ['Day'], 'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day'])
isaiah = Employee("Isaiah", "Dish Washer", {'Monday': ['Day'], 'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day'])
tammy = Employee("Tammy", "Food Prep Helper", {'Monday': ['Night'], 'Tuesday': ['Night'], 'Wednesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Night'])
demetrius = Employee("Demetrius", "Food Service Worker", {'Monday': ['Night'], 'Tuesday': ['Night'], 'Wednesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Night'])
surya = Employee("Surya", "Student Worker", {'Tuesday': ['Night'], 'Sunday': ['Night']}, ['Night'])
dasarath = Employee("Dasarath", "Student Worker", {'Tuesday': ['Night'], 'Sunday': ['Night']}, ['Night'])
vyoma = Employee("Vyoma", "Student Worker", {'Tuesday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Friday': ['Day']}, ['Day', 'Night'])
neeraj = Employee("Neeraj", "Student Worker", {'Monday': ['Day'], 'Wednesday': ['Day'], 'Thursday': ['Day'], 'Sunday': ['Night']}, ['Day', 'Night'])
ganesh = Employee("Ganesh", "Student Worker", {'Monday': ['Day'], 'Tuesday': ['Night'], 'Wednesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Day', 'Night'])
jaswanth = Employee("Jaswanth", "Student Worker", {'Tuesday': ['Night'], 'Wednesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Night'])
chandana = Employee("Chandana", "Student Worker", {'Monday': ['Night'], 'Tuesday': ['Night'], 'Thursday': ['Night'], 'Sunday': ['Night']}, ['Night'])

business_needs = {
    'Monday': {
        'Day': {
            'Supervisor': 1,
            'Team Lead': 1,
            'Cook': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        },
        'Night': {
            'Supervisor': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        }
    },
    'Tuesday': { 
        'Day': {
            'Supervisor': 1,
            'Team Lead': 1,
            'Cook': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        },
        'Night': {
            'Supervisor': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        } 
    },  # Repeat the structure for other days
    'Wednesday': {
        'Day': {
            'Supervisor': 1,
            'Team Lead': 1,
            'Cook': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        },
        'Night': {
            'Supervisor': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        } 
    },
    'Thursday': {'Day': {
            'Supervisor': 1,
            'Team Lead': 1,
            'Cook': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        },
        'Night': {
            'Supervisor': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        } 
    },
    'Friday': {
        'Day': {
            'Supervisor': 1,
            'Team Lead': 1,
            'Cook': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        },
    },
    'Sunday': {
        'Night': {
            'Supervisor': 1,
            'Food Prep Helper': 1,
            'Food Service Worker': 3,
            'Dish Washer': 2,
            'Student Worker': 5
        }   # Only night structure
    }
}

import os

def get_unique_filename(path):
    # Extracting the directory, base filename, and extension from the path
    directory, filename = os.path.split(path)
    base_filename, extension = os.path.splitext(filename)
    
    counter = 1
    while os.path.exists(path):
        path = os.path.join(directory, f"{base_filename}_{counter}{extension}")
        counter += 1

    return path
# 1. Set up the employees list
employees_list = [marisa, ashley, shala, shauntel, silicia, isaiah, tammy, demetrius, surya, dasarath, vyoma, neeraj, ganesh, jaswanth, chandana]

# 2. Create the schedule
scheduler = Scheduler(business_needs)
schedule = scheduler.create_schedule(employees_list)

# 3. Define the filename
filename = get_unique_filename('C:/Users/Cprickett/Downloads/schedule.csv')

# 4. Export the schedule to a CSV file
export_schedule_to_csv(schedule, employees_list, filename)  # Note: Using the updated function

# 5. Print the "Done" message
print("Done")



