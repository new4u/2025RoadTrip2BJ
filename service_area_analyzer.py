#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ServiceArea:
    name: str
    highway: str
    location: str
    popularity: int  # 1-5星评级
    facilities: Dict
    peak_hours: List[str]
    special_notes: Optional[str] = None

class ServiceAreaAnalyzer:
    def __init__(self):
        # 基于《高速公路服务区出行热度分析报告》的数据
        self.service_areas_data = {
            "京港澳高速G4": {
                "广州服务区": {
                    "location": "广东省广州市白云区",
                    "popularity": 5,
                    "facilities": {
                        "餐饮": ["快餐", "地方特色", "便利店"],
                        "休息": ["休息室", "淋浴间", "母婴室"],
                        "充电": {
                            "特斯拉超充": 8,
                            "国标快充": 12
                        },
                        "停车": {
                            "小车位": 200,
                            "大车位": 50
                        }
                    },
                    "peak_hours": ["11:00-13:00", "17:00-19:00"],
                    "special_notes": "粤式早茶，24小时营业"
                },
                "长沙服务区": {
                    "location": "湖南省长沙市望城区",
                    "popularity": 4,
                    "facilities": {
                        "餐饮": ["快餐", "湘菜", "便利店"],
                        "休息": ["休息室", "淋浴间"],
                        "充电": {
                            "特斯拉超充": 6,
                            "国标快充": 8
                        },
                        "停车": {
                            "小车位": 150,
                            "大车位": 40
                        }
                    },
                    "peak_hours": ["12:00-14:00", "18:00-20:00"],
                    "special_notes": "臭豆腐小吃"
                },
                "信阳服务区": {
                    "location": "河南省信阳市浉河区",
                    "popularity": 4,
                    "facilities": {
                        "餐饮": ["快餐", "豫菜", "便利店"],
                        "休息": ["休息室", "淋浴间", "母婴室"],
                        "充电": {
                            "特斯拉超充": 4,
                            "国标快充": 10
                        },
                        "停车": {
                            "小车位": 160,
                            "大车位": 45
                        }
                    },
                    "peak_hours": ["11:30-13:30", "17:30-19:30"],
                    "special_notes": "信阳毛尖茶室"
                }
            },
            "京开高速G45": {
                "德州服务区": {
                    "location": "山东省德州市陵城区",
                    "popularity": 4,
                    "facilities": {
                        "餐饮": ["快餐", "鲁菜", "便利店"],
                        "休息": ["休息室", "淋浴间", "母婴室"],
                        "充电": {
                            "特斯拉超充": 10,
                            "国标快充": 15
                        },
                        "停车": {
                            "小车位": 180,
                            "大车位": 45
                        }
                    },
                    "peak_hours": ["11:30-13:30", "17:30-19:30"],
                    "special_notes": "德州扒鸡"
                },
                "衡水服务区": {
                    "location": "河北省衡水市桃城区",
                    "popularity": 3,
                    "facilities": {
                        "餐饮": ["快餐", "冀菜", "便利店"],
                        "休息": ["休息室", "淋浴间"],
                        "充电": {
                            "特斯拉超充": 4,
                            "国标快充": 8
                        },
                        "停车": {
                            "小车位": 120,
                            "大车位": 35
                        }
                    },
                    "peak_hours": ["12:00-14:00", "18:00-20:00"],
                    "special_notes": "衡水老白干展示"
                }
            },
            "广深高速G4": {
                "东莞服务区": {
                    "location": "广东省东莞市道滘镇",
                    "popularity": 5,
                    "facilities": {
                        "餐饮": ["快餐", "粤式点心", "便利店"],
                        "休息": ["休息室", "淋浴间", "母婴室"],
                        "充电": {
                            "特斯拉超充": 12,
                            "国标快充": 16
                        },
                        "停车": {
                            "小车位": 220,
                            "大车位": 40
                        }
                    },
                    "peak_hours": ["10:30-12:30", "16:30-18:30"],
                    "special_notes": "东莞小吃街，24小时营业"
                }
            }
        }

    def get_service_areas(self) -> List[ServiceArea]:
        """获取所有服务区信息"""
        areas = []
        for highway, highway_data in self.service_areas_data.items():
            for name, data in highway_data.items():
                area = ServiceArea(
                    name=name,
                    highway=highway,
                    location=data["location"],
                    popularity=data["popularity"],
                    facilities=data["facilities"],
                    peak_hours=data["peak_hours"],
                    special_notes=data.get("special_notes")
                )
                areas.append(area)
        return areas

    def get_popular_areas(self, min_rating: int = 4) -> List[ServiceArea]:
        """获取高评分服务区"""
        return [area for area in self.get_service_areas() 
                if area.popularity >= min_rating]

    def get_areas_with_tesla_chargers(self) -> List[ServiceArea]:
        """获取有特斯拉充电桩的服务区"""
        return [area for area in self.get_service_areas() 
                if area.facilities.get("充电", {}).get("特斯拉超充", 0) > 0]

    def save_to_json(self, filename: str):
        """保存数据到JSON文件"""
        areas = self.get_service_areas()
        data = [vars(area) for area in areas]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存数据时出错: {e}")

def main():
    analyzer = ServiceAreaAnalyzer()
    
    print("分析服务区数据...")
    
    # 获取所有服务区
    all_areas = analyzer.get_service_areas()
    print(f"\n找到 {len(all_areas)} 个服务区:")
    for area in all_areas:
        print(f"- {area.name} ({area.highway}): {area.popularity}星级")
    
    # 获取高评分服务区
    popular_areas = analyzer.get_popular_areas()
    print(f"\n{len(popular_areas)} 个高评分服务区:")
    for area in popular_areas:
        print(f"- {area.name}: {area.popularity}星级")
    
    # 获取有特斯拉充电桩的服务区
    tesla_areas = analyzer.get_areas_with_tesla_chargers()
    print(f"\n{len(tesla_areas)} 个服务区有特斯拉充电桩:")
    for area in tesla_areas:
        chargers = area.facilities["充电"]["特斯拉超充"]
        print(f"- {area.name}: {chargers}个充电桩")
    
    # 保存数据
    analyzer.save_to_json("service_areas_analysis.json")

if __name__ == "__main__":
    main()
