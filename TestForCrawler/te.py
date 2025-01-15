import json

def convert_name(name):
    """Convert 'LASTNAME, FIRSTNAME' to 'FIRSTNAME LASTNAME'"""
    lastname, firstname = name.split(',')
    return f"{firstname.strip()} {lastname.strip()}"

def process_json(filepath):
    # Read JSON
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Process each department
    for dept in data:
        courses = data[dept]
        for course in courses:
            # Split instructors string and convert each name
            instructors = course[1].split('+')
            converted = [convert_name(name) for name in instructors]
            # Join back with '+'
            course[1] = '+'.join(converted)
    
    # Save modified JSON
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    process_json('table3.json')