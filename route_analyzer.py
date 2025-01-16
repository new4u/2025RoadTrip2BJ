#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ServiceArea:
    name: str
    arrival_time: str
    duration_from_start: str
    features: Dict
    traffic_level: str
    special_notes: Optional[str] = None

@dataclass
class City:
    name: str
    arrival_time: str
    duration_from_start: str

class RouteAnalyzer:
    def __init__(self, schedule_file: str):
        with open(schedule_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.trip_info = self.data['trip_info']
        self.cities = [City(**city) for city in self.data['cities']]
        self.service_areas = [ServiceArea(**area) for area in self.data['service_areas']]
        self.important_notes = self.data['important_notes']

    def get_route_summary(self) -> Dict:
        """获取路线概要"""
        return {
            "total_cities": len(self.cities),
            "total_service_areas": len(self.service_areas),
            "estimated_duration": self.trip_info['estimated_duration'],
            "total_distance": self.trip_info['total_distance']
        }

    def get_service_areas_by_traffic(self, level: str) -> List[ServiceArea]:
        """按人流量获取服务区"""
        return [area for area in self.service_areas 
                if area.traffic_level == level]

    def get_charging_service_areas(self) -> List[ServiceArea]:
        """获取有充电设施的服务区"""
        return [area for area in self.service_areas 
                if area.features.get('charging', False)]

    def get_rest_recommendations(self) -> List[Dict]:
        """获取休息建议"""
        recommendations = []
        start_time = datetime.strptime(self.trip_info['start_time'], '%Y-%m-%d %H:%M:%S')
        
        # 建议每4小时休息一次
        rest_interval = timedelta(hours=4)
        next_rest = start_time + rest_interval
        
        for area in self.service_areas:
            area_time = datetime.strptime(
                f"{start_time.date()} {area.arrival_time}", 
                '%Y-%m-%d %H:%M:%S'
            )
            
            # 如果到达时间跨天
            if area.arrival_time < self.service_areas[0].arrival_time:
                area_time += timedelta(days=1)
            
            if area_time >= next_rest:
                recommendations.append({
                    "service_area": area.name,
                    "arrival_time": area.arrival_time,
                    "features": area.features,
                    "traffic_level": area.traffic_level,
                    "special_notes": area.special_notes
                })
                next_rest = area_time + rest_interval
        
        return recommendations

    def save_analysis(self, filename: str):
        """保存分析结果"""
        analysis = {
            "route_summary": self.get_route_summary(),
            "rest_recommendations": self.get_rest_recommendations(),
            "charging_areas": [
                {
                    "name": area.name,
                    "arrival_time": area.arrival_time,
                    "traffic_level": area.traffic_level
                }
                for area in self.get_charging_service_areas()
            ],
            "traffic_analysis": {
                level: [
                    {
                        "name": area.name,
                        "arrival_time": area.arrival_time
                    }
                    for area in self.get_service_areas_by_traffic(level)
                ]
                for level in ["low", "medium", "high"]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)

def main():
    analyzer = RouteAnalyzer('route_schedule.json')
    
    print("路线概要:")
    summary = analyzer.get_route_summary()
    print(f"- 途经城市: {summary['total_cities']}个")
    print(f"- 服务区数量: {summary['total_service_areas']}个")
    print(f"- 预计行驶时间: {summary['estimated_duration']}")
    print(f"- 总距离: {summary['total_distance']}公里")
    
    print("\n休息建议:")
    for i, rec in enumerate(analyzer.get_rest_recommendations(), 1):
        print(f"{i}. {rec['service_area']} ({rec['arrival_time']})")
        if rec['special_notes']:
            print(f"   特别提醒: {rec['special_notes']}")
    
    print("\n充电服务区:")
    for area in analyzer.get_charging_service_areas():
        print(f"- {area.name} ({area.arrival_time})")
    
    print("\n保存分析结果...")
    analyzer.save_analysis('route_analysis.json')
    print("分析完成！")

if __name__ == "__main__":
    main()
