import json

def process_faculty_data():
    # 读取API响应数据
    with open('api_response.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 存储教授信息的列表
    faculty_pairs = []
    
    # 处理每个教授的数据
    for record in data['data']['list']:
        # 获取英文名
        name = record.get('enName', '')
        
        # 获取网站链接（优先使用website，如果为空则使用permaLink）
        website = record.get('website', '') or record.get('permaLink', '')
        
        # 添加到列表
        faculty_pairs.append({
            'name': name,
            'website': website
        })
    
    # 保存处理后的数据
    with open('fa_pair.json', 'w', encoding='utf-8') as f:
        json.dump(faculty_pairs, f, ensure_ascii=False, indent=4)
    
    print(f"已处理 {len(faculty_pairs)} 位教授的信息")

if __name__ == "__main__":
    process_faculty_data()