#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module vẽ bản đồ - tạo file HTML bản đồ với Folium
"""

import folium


def create_single_vehicle_map(lat1, lon1, lat2, lon2, name1, name2, 
                               geometry, distance_km, duration_hrs, 
                               vehicle_type, output_file):
    """
    Vẽ bản đồ cho một loại phương tiện.
    
    Args:
        lat1, lon1: Tọa độ điểm bắt đầu
        lat2, lon2: Tọa độ điểm đích
        name1, name2: Tên địa điểm
        geometry: GeoJSON geometry từ OSRM
        distance_km: Khoảng cách (km)
        duration_hrs: Thời gian (giờ)
        vehicle_type: "driving" hoặc "bike"
        output_file: Tên file output
        
    Returns:
        str: Đường dẫn file đã lưu
    """
    vehicle_name = "Ô tô" if vehicle_type == "driving" else "Xe máy"
    vehicle_icon = "🚗" if vehicle_type == "driving" else "🏍️"
    color = 'blue' if vehicle_type == "driving" else 'orange'
    
    # Tính toán center và zoom
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    
    if distance_km < 10:
        zoom = 13
    elif distance_km < 50:
        zoom = 11
    elif distance_km < 200:
        zoom = 9
    else:
        zoom = 7
    
    # Tạo bản đồ
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
    
    # Thêm markers
    folium.Marker(
        [lat1, lon1],
        popup=f"<b>Điểm đầu</b><br>{name1}",
        tooltip="Bắt đầu",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [lat2, lon2],
        popup=f"<b>Điểm cuối</b><br>{name2}",
        tooltip="Kết thúc",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Vẽ đường
    latlon = [(lat, lon) for lon, lat in geometry["coordinates"]]
    folium.PolyLine(
        latlon,
        color=color,
        weight=5,
        opacity=0.7,
        popup=f"<b>{vehicle_icon} {vehicle_name}</b><br>{distance_km:,.1f} km<br>{duration_hrs*60:.0f} phút"
    ).add_to(m)
    
    # Lưu file
    m.save(output_file)
    return output_file


def create_comparison_map(lat1, lon1, lat2, lon2, name1, name2,
                          geom_car, km_car, hrs_car,
                          geom_bike, km_bike, hrs_bike,
                          output_file="route_comparison.html"):
    """
    Vẽ bản đồ so sánh giữa ô tô và xe máy.
    
    Returns:
        tuple: (output_file, comparison_data)
    """
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Markers
    folium.Marker(
        [lat1, lon1],
        popup=f"<b>Điểm đầu</b><br>{name1}",
        tooltip="Bắt đầu",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [lat2, lon2],
        popup=f"<b>Điểm cuối</b><br>{name2}",
        tooltip="Kết thúc",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Vẽ đường ô tô (màu xanh dương)
    latlon_car = [(lat, lon) for lon, lat in geom_car["coordinates"]]
    folium.PolyLine(
        latlon_car,
        color='blue',
        weight=5,
        opacity=0.7,
        popup=f"<b>🚗 Ô tô</b><br>{km_car:,.1f} km<br>{hrs_car*60:.0f} phút"
    ).add_to(m)
    
    # Vẽ đường xe máy (màu đỏ)
    latlon_bike = [(lat, lon) for lon, lat in geom_bike["coordinates"]]
    folium.PolyLine(
        latlon_bike,
        color='red',
        weight=5,
        opacity=0.7,
        popup=f"<b>🏍️ Xe máy</b><br>{km_bike:,.1f} km<br>{hrs_bike*60:.0f} phút"
    ).add_to(m)
    
    # Thêm chú thích
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Chú thích:</b></p>
    <p><span style="color:blue">━━━</span> Ô tô: {km_car:.1f} km</p>
    <p><span style="color:red">━━━</span> Xe máy: {km_bike:.1f} km</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Lưu file
    m.save(output_file)
    
    # Tính toán so sánh
    diff_km = abs(km_car - km_bike)
    diff_min = abs(hrs_car * 60 - hrs_bike * 60)
    
    comparison = {
        "car_km": km_car,
        "car_min": hrs_car * 60,
        "bike_km": km_bike,
        "bike_min": hrs_bike * 60,
        "diff_km": diff_km,
        "diff_min": diff_min,
        "shorter": "car" if km_car < km_bike else ("bike" if km_bike < km_car else "same")
    }
    
    return output_file, comparison

