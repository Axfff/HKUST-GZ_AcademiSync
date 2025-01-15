from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

# 设置Firefox选项
firefox_options = Options()
firefox_options.add_argument("--headless")

# 设置Firefox驱动
service = Service('/snap/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=firefox_options)

# 访问目标URL
url = 'https://facultyprofiles.hkust-gz.edu.cn/'
driver.get(url)

# 等待页面加载完成
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "basic-info-wrap")))

# 获取所有教授信息
faculty_pairs = []
faculty_elements = driver.find_elements(By.CLASS_NAME, "basic-info-wrap")

# 存储原始窗口句柄
original_window = driver.current_window_handle

for element in faculty_elements:
    try:
        # 获取英文名
        english_name = element.find_element(By.CLASS_NAME, "english-name").text
        
        # 获取View Profile按钮
        view_btn = element.find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "view-btn")
        
        # 滚动到按钮位置
        driver.execute_script("arguments[0].scrollIntoView(true);", view_btn)
        time.sleep(1)
        
        # 使用JavaScript点击按钮
        driver.execute_script("arguments[0].click();", view_btn)
        
        # 等待新窗口打开
        time.sleep(2)
        
        # 切换到新窗口
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
                
        # 获取URL
        profile_url = driver.current_url
        
        # 关闭新窗口
        driver.close()
        
        # 切回原始窗口
        driver.switch_to.window(original_window)
        time.sleep(1)
        
        # 存储配对信息
        faculty_pairs.append({
            "english_name": english_name,
            "profile_url": profile_url
        })
        print(f"Successfully processed: {english_name}")
        
    except Exception as e:
        print(f"Error processing faculty: {e}")
        continue

# 保存到JSON文件
with open('faculty_pairs.json', 'w', encoding='utf-8') as f:
    json.dump(faculty_pairs, f, ensure_ascii=False, indent=4)
# 关闭浏览器
driver.quit()

print(f"已保存 {len(faculty_pairs)} 位教授的信息")