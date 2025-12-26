#testkommentar
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

# Function to load zodiac signs and their date ranges
def load_zodiac_signs(filename='zodiacSigns.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    zodiac_signs = []
    for sign in root.findall('sign'):
        name = sign.find('name').text
        start_date = datetime.strptime(sign.find('startDate').text + '2024', '%d.%m.%Y')
        end_date = datetime.strptime(sign.find('endDate').text + '2024', '%d.%m.%Y')
        zodiac_signs.append((name, start_date, end_date))
    return zodiac_signs

# Function to determine the zodiac sign based on date of birth
def get_zodiac_sign(date_of_birth, zodiac_signs):
    birth_date = datetime.strptime(date_of_birth, '%d.%m.%Y')
    birth_date_str = birth_date.strftime('%m%d')
    for name, start_date, end_date in zodiac_signs:
        start_str = start_date.strftime('%m%d')
        end_str = end_date.strftime('%m%d')
        if start_str > end_str:
            if birth_date_str >= start_str or birth_date_str <= end_str:
                return name
        else:
            if start_str <= birth_date_str <= end_str:
                return name
    return "Unknown"

user_choice = input("Do you want to list all Bundestagsmembers since 1947 or just the current? (Type 'all' for all members or 'current' for current members): ").strip().lower()

tree = ET.parse('MDB_STAMMDATEN.XML')
root = tree.getroot()

zodiac_signs = load_zodiac_signs()

people_info = []

for mdb in root.findall('.//MDB'):
    if user_choice == "current":
        wahlperioden = mdb.findall('.//WAHLPERIODE')
        if wahlperioden:
            last_wahlperiode = wahlperioden[-1]
            mdbwp_bis = last_wahlperiode.find('.//MDBWP_BIS')
            if mdbwp_bis is not None and mdbwp_bis.text:
                continue
    
    person_id = mdb.find('ID').text if mdb.find('ID') is not None else "No ID"
    first_name = mdb.find('.//VORNAME').text if mdb.find('.//VORNAME') is not None else "No First Name"
    last_name = mdb.find('.//NACHNAME').text if mdb.find('.//NACHNAME') is not None else "No Last Name"
    date_of_birth = mdb.find('.//GEBURTSDATUM').text if mdb.find('.//GEBURTSDATUM') is not None else "No Date of Birth"
    partei_kurz = mdb.find('.//PARTEI_KURZ').text if mdb.find('.//PARTEI_KURZ') is not None else "No Party"
    
    zodiac_sign = get_zodiac_sign(date_of_birth, zodiac_signs) if date_of_birth != "No Date of Birth" else "Unknown"
    
    people_info.append((person_id, first_name, last_name, date_of_birth, partei_kurz, zodiac_sign))

# Group people by their zodiac signs
grouped_by_zodiac = defaultdict(list)
for person in people_info:
    grouped_by_zodiac[person[5]].append(person)

# Write the output to a text file
output_filename = 'current_people_by_zodiac.txt' if user_choice == 'current' else 'all_people_by_zodiac.txt'
with open(output_filename, 'w') as file:
    file.write(f"Total Abgeordnete: {len(people_info)}\n\n")
    
    # Write the summary of zodiac signs
    for zodiac, count in sorted(grouped_by_zodiac.items(), key=lambda x: len(x[1]), reverse=True):
        file.write(f"{zodiac} {len(grouped_by_zodiac[zodiac])} Abgeordnete\n")
    file.write("\n")
    
    # Write the detailed list for each zodiac sign
    for zodiac, people in grouped_by_zodiac.items():
        file.write(f"{zodiac} {len(people)} Abgeordnete\n")
        for person in people:
            file.write(f"{person[0]}, '{person[1]}', '{person[2]}', '{person[3]}', '{person[4]}', '{person[5]}'\n")
        file.write("\n")

print(f"Output written to {output_filename}")
