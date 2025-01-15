import re
from bs4 import BeautifulSoup
import json

# 定义结构体
class Course:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Course(Name: {self.name}, Description: {self.description})"

# 课程列表
list = ["AIAA","AMAT", "BSBE", "CMAA", "DSAA", "EOAS", "FTEC", "FUNH", "INFH", "INTR", "IOTA", "IPEN", "LANG", "MICS", "PDEV", "PLED", "ROAS", "SEEN", "SMMG", "SOCH", "SYSH", "UCMP", "UCUG", "UFUG", "UGOD"]

# 创建结构体数组
all_courses = []

# 读取HTML文件
for subject in list:
    with open(f'/home/nyz/test/{subject}.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 查找所有h2标签
    h2_tags = soup.find_all('h2')
    
    # 查找所有DESCRIPTION
    description_tags = soup.find_all('th', text='DESCRIPTION')
    
    # 遍历h2标签和DESCRIPTION标签
    for h2, desc in zip(h2_tags, description_tags):
        name = h2.get_text(strip=True)
        description = desc.find_next_sibling('td').get_text(strip=True)
        all_courses.append(Course(name, description))

# 存储为JSON文件
with open('/home/nyz/test/datau2.json', 'w', encoding='utf-8') as jsonfile:
    json.dump([course.__dict__ for course in all_courses], jsonfile, ensure_ascii=False, indent=4)