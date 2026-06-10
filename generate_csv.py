import os
import re
import csv

def generate_maps_csv(directory_path='.'):
    output_file = 'google_maps_import.csv'
    restaurants = []

    # 尋找所有 markdown 檔案
    for filename in os.listdir(directory_path):
        if not filename.endswith('.md') or filename == 'GEMINI.md':
            continue
            
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 使用正則表達式尋找餐廳名稱 (從 H1 或分店資訊中提取)
            # 這裡我們用比較簡單的方式：直接從檔案內抓取所有 "店名" 或 "地址"
            
            # 尋找主要餐廳地址 (格式通常為 - **地址**: 台北市...)
            main_address_match = re.search(r'-\s*\*\*地址\*\*:\s*([^\n]+)', content)
            
            if main_address_match:
                # 嘗試從標題 (# 餐廳名) 抓取主要餐廳名稱，如果沒有則用檔名
                title_match = re.search(r'^#\s+([^\n]+)', content)
                name = title_match.group(1).strip() if title_match else filename.replace('.md', '')
                address = main_address_match.group(1).split('（')[0].split('(')[0].strip() # 濾除括號內的說明
                restaurants.append({'Name': name, 'Address': address})
            
            # 尋找可能的分店資訊
            # 假設分店資訊格式為:
            # - **店名**: 京都清水
            # - **地址**: 新北市林口區忠孝路51號
            branches = re.finditer(r'-\s*\*\*店名\*\*:\s*([^\n]+)\n\s*-\s*\*\*地址\*\*:\s*([^\n]+)', content)
            for branch in branches:
                branch_name = branch.group(1).strip()
                branch_address = branch.group(2).split('（')[0].split('(')[0].strip()
                # 加上主店名以便辨識
                title_match = re.search(r'^#\s+([^\n]+)', content)
                main_name = title_match.group(1).strip() if title_match else ""
                if main_name and main_name not in branch_name:
                    branch_name = f"{branch_name} ({main_name}姐妹店/分店)"
                    
                restaurants.append({'Name': branch_name, 'Address': branch_address})

    # 寫入 CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Address'])
        writer.writeheader()
        writer.writerows(restaurants)
        
    print(f"Successfully generated {output_file}! Total {len(restaurants)} restaurants included.")

if __name__ == '__main__':
    generate_maps_csv()
