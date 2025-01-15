from bs4 import BeautifulSoup
import json

def parse_courses(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    course_pairs = []
    
    # Find all course divs
    courses = soup.find_all('div', class_='course')
    
    for course in courses:
        # Get course title
        course_title = ' '.join(course.find('h2').text.strip().split()[:2])
        # Get all instructors
        instructors = []
        instructor_links = course.find_all('a', href=lambda x: x and 'instructor' in x)
        for link in instructor_links:
            instructor_name = link.text.strip()
            if instructor_name not in instructors:  # Remove duplicates
                instructors.append(instructor_name)
        
        # Join instructors with '+'
        instructors_str = '+'.join(instructors)
        
        # Add to results
        if instructors_str:  # Only add if there are instructors
            course_pairs.append((course_title, instructors_str))
    
    return course_pairs
course_codes = ["AIAA", "AMAT", "BSBE", "CMAA", "DSAA", "EOAS", "FTEC", "FUNH", "INFH", "INTR", "IOTA", "IPEN", "LANG", "MICS", "PDEV", "PLED", "ROAS", "SEEN", "SMMG", "SOCH", "SYSH", "UCMP", "UCUG", "UFUG", "UGOD"]

# Example usage
if __name__ == "__main__":
    all_courses = {}
    for code in course_codes:
        file_path = f'/home/nyz/test/{code}.html'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            pairs = parse_courses(html_content)
            all_courses[code] = pairs
        except FileNotFoundError:
            print(f"File {file_path} not found.")
    
    with open('/home/nyz/test/table3.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_courses, json_file, ensure_ascii=False, indent=4)