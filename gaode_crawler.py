#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from typing import Dict, List, Optional

class GaodeCrawler:
    def __init__(self):
        self.base_url = "https://restapi.amap.com/v3"
        # 请替换为您的高德API密钥
        self.api_key = "YOUR_AMAP_KEY"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_route_info(self, origin: str, destination: str) -> Dict:
        """获取路线规划信息"""
        url = f"{self.base_url}/direction/driving"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "extensions": "all",
            "strategy": 2,  # 考虑路况
            "waypoints": ""  # 途经点
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            data = response.json()
            return data
        except Exception as e:
            print(f"Error getting route info: {e}")
            return {}

    def get_service_areas(self, route_data: Dict) -> List[Dict]:
        """从路线数据中提取服务区信息"""
        service_areas = []
        
        if "route" not in route_data:
            return service_areas

        try:
            steps = route_data["route"]["paths"][0]["steps"]
            for step in steps:
                # 解析导航指令中的服务区信息
                if "服务区" in step["instruction"]:
                    area = {
                        "name": self._extract_name(step["instruction"]),
                        "location": step["polyline"].split(";")[0],
                        "distance": step["distance"],
                        "duration": step["duration"]
                    }
                    service_areas.append(area)
        except Exception as e:
            print(f"Error extracting service areas: {e}")

        return service_areas

    def _extract_name(self, instruction: str) -> str:
        """从导航指令中提取服务区名称"""
        try:
            # 假设服务区名称在"到达XXX服务区"中
            if "到达" in instruction and "服务区" in instruction:
                start = instruction.find("到达") + 2
                end = instruction.find("服务区") + 3
                return instruction[start:end]
        except Exception:
            pass
        return "未知服务区"

    def save_to_json(self, data: List[Dict], filename: str):
        """保存数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

def main():
    crawler = GaodeCrawler()
    
    # 深圳到北京的坐标
    origin = "114.057868,22.543099"      # 深圳
    destination = "116.397128,39.916527"  # 北京
    
    print("获取路线信息...")
    route_data = crawler.get_route_info(origin, destination)
    
    print("提取服务区信息...")
    service_areas = crawler.get_service_areas(route_data)
    
    print("保存数据...")
    crawler.save_to_json(service_areas, "gaode_service_areas.json")
    
    print(f"找到 {len(service_areas)} 个服务区")
    for area in service_areas:
        print(f"- {area['name']}")

if __name__ == "__main__":
    main()
