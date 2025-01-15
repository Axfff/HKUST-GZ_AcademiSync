import json
from collections import defaultdict

def extract_table3_names(data):
    # 使用字典保留原始大小写
    names_dict = {}
    for dept in data.values():
        for course in dept:
            if len(course) > 1 and course[1]:
                instructors = course[1].split('+')
                for name in instructors:
                    if name:
                        names_dict[name.lower()] = name
    return names_dict

def compare_names():
    # 读取数据
    with open('table3.json', 'r', encoding='utf-8') as f:
        table3_data = json.load(f)
    with open('faculty_pairs.json', 'r', encoding='utf-8') as f:
        faculty_data = json.load(f)

    # 提取名字映射
    table3_dict = extract_table3_names(table3_data)
    faculty_dict = {item["english_name"].lower(): item["english_name"] 
                   for item in faculty_data 
                   if "english_name" in item and item["english_name"]}

    # 比较差异
    only_in_table3 = set(table3_dict.keys()) - set(faculty_dict.keys())
    only_in_faculty = set(faculty_dict.keys()) - set(table3_dict.keys())

    # 输出结果(保持原始大小写)
    print("=== 仅在table3.json中出现的名字 ===")
    for name_lower in sorted(only_in_table3):
        print(f"  {table3_dict[name_lower]}")
    
    print("\n=== 仅在faculty_pairs.json中出现的名字 ===")
    for name_lower in sorted(only_in_faculty):
        print(f"  {faculty_dict[name_lower]}")

if __name__ == "__main__":
    compare_names()