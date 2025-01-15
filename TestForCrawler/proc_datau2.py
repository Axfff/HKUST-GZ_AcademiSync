import json
import re

# 读取JSON文件
with open('/home/nyz/test/datau2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理每个课程条目
for course in data:
    name = course['name']
    description = course['description']
    
    # 使用正则表达式拆分name字段
    match = re.match(r'^(.*?) - (.*?) \((\d+) units?\)$', name)
    if match:
        course_code = match.group(1)
        course_name = match.group(2)
        units = match.group(3)
        
        # 更新课程条目
        course['course_code'] = course_code
        course['name'] = course_name
        course['unit'] = units

# 将处理后的数据写回JSON文件
with open('/home/nyz/test/datau2_processed.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)