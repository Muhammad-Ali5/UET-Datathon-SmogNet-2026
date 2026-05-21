import pandas as pd
import json
import os
import requests
from pathlib import Path

try:
    from .config import OPENWEATHER_API_KEY
except ImportError:
    try:
        from config import OPENWEATHER_API_KEY
    except ImportError:
        OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your-openweather-api-key")

# Pakistan Coordinates mapping for real-time OpenWeatherMap API
CITY_COORDS = {
    "Lahore": {"lat": 31.5204, "lon": 74.3587},
    "Karachi": {"lat": 24.8607, "lon": 67.0011},
    "Islamabad": {"lat": 33.6844, "lon": 73.0479},
    "Peshawar": {"lat": 34.0151, "lon": 71.5249},
    "Quetta": {"lat": 30.1798, "lon": 66.9750}
}

def fetch_realtime_pollution(city_name):
    """
    Fetch real-time air pollution details from OpenWeatherMap Air Pollution API.
    Returns:
        dict: containing pollutants if successful, otherwise None
    """
    coords = CITY_COORDS.get(city_name)
    if not coords or not OPENWEATHER_API_KEY:
        print(f"[{city_name}] Skipping real-time fetch: Missing coordinates or API Key.")
        return None

    lat = coords["lat"]
    lon = coords["lon"]
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    
    try:
        print(f"[{city_name}] Querying live OpenWeatherMap Air Pollution API ({lat}, {lon})...")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "list" in data and len(data["list"]) > 0:
            components = data["list"][0]["components"]
            # returns dict with keys: co, no, no2, o3, so2, pm2_5, pm10, nh3
            return components
        else:
            print(f"[{city_name}] OpenWeatherMap API returned empty list.")
    except Exception as e:
        print(f"[{city_name}] Error querying OpenWeatherMap API: {e}")
    return None


# File paths
BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
DATASETS_DIR = ROOT_DIR / "datasets" / "Testing"
AQI_DATA_PATH = ROOT_DIR / "frontend" / "aqi_data.json"

# Pakistan Map Coordinates
CITY_MAP_COORDS = {
    "Lahore": {"top": "25%", "left": "52%"},
    "Karachi": {"top": "75%", "left": "33%"},
    "Islamabad": {"top": "15%", "left": "60%"},
    "Peshawar": {"top": "16%", "left": "50%"},
    "Quetta": {"top": "48%", "left": "28%"}
}

# Local landmarks/districts for anomalies
CITY_LANDMARKS = {
    "Lahore": ["Gulberg Zone", "Walled City", "North Industrial Area", "Model Town", "Allama Iqbal Town"],
    "Karachi": ["Kemari Port", "Clifton District", "S.I.T.E. Industrial Area", "Korangi Bypass", "Nazimabad"],
    "Islamabad": ["Blue Area", "Sector F-6", "I-9 Industrial Zone", "Srinagar Highway", "Sector G-11"],
    "Peshawar": ["Hayatabad Ring Rd", "Karkhano Market", "Peshawar Cantt", "University Road", "GT Road Cluster"],
    "Quetta": ["Cantonment Area", "Jinnah Road Hub", "Sariab Road District", "Double Road", "Airport Road Zone"]
}

# WHO 24h limits for compliance calculation
WHO_LIMITS = {
    "pm25": 15,
    "pm10": 45,
    "no2": 25,
    "o3": 100,
    "so2": 40,
    "co": 4000
}

def calculate_us_aqi_pm25(pm25):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500)
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25 <= c_high:
            return round(i_low + (i_high - i_low) / (c_high - c_low) * (pm25 - c_low))
    return 500 if pm25 > 500.4 else 0

def calculate_us_aqi_pm10(pm10):
    breakpoints = [
        (0.0, 54.0, 0, 50),
        (55.0, 154.0, 51, 100),
        (155.0, 254.0, 101, 150),
        (255.0, 354.0, 151, 200),
        (355.0, 424.0, 201, 300),
        (425.0, 504.0, 301, 400),
        (505.0, 604.0, 401, 500)
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm10 <= c_high:
            return round(i_low + (i_high - i_low) / (c_high - c_low) * (pm10 - c_low))
    return 500 if pm10 > 604.0 else 0

def get_aqi_status(aqi):
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy for Sensitive Groups"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"

def classify_dominant_source(row):
    pm2_5 = row['components_pm2_5']
    pm10 = row['components_pm10']
    nh3 = row['components_nh3']
    co = row['components_co']
    no = row['components_no']
    no2 = row['components_no2']
    so2 = row['components_so2']
    
    # Rule-based fallback classifier
    if nh3 > 80 and co > 2000:
        return "Crop Burning", "agricultural"
    if no > 50 and no2 > 50:
        return "Vehicular Traffic", "vehicular"
    if so2 > 30:
        return "Industrial Emissions", "industrial"
    if pm10 > pm2_5 * 2.5:
        return "Dust Storm suspension", "industrial"  # Map dust to industrial/mixed
    return "Mixed Pollution", "vehicular"

def generate_aqi_data():
    if not DATASETS_DIR.exists():
        print(f"Datasets directory not found at {DATASETS_DIR}")
        return

    csv_mapping = {
        "Islamabad": "islamabad_complete_data_july_to_dec_2024.csv",
        "Karachi": "karachi_complete_data_july_to_dec_2024.csv",
        "Lahore": "lahore_complete_data_july_to_dec_2024.csv",
        "Peshawar": "peshawar_complete_data_july_to_dec_2024.csv",
        "Quetta": "quetta_complete_data_july_to_dec_2024.csv"
    }

    cities_data = {}
    recent_alerts = []

    for city_name, filename in csv_mapping.items():
        filepath = DATASETS_DIR / filename
        if not filepath.exists():
            print(f"File {filename} not found in {DATASETS_DIR}")
            continue

        # Load CSV
        df = pd.read_csv(filepath)
        
        # Take the last 24 rows for recent trend details
        df_recent = df.tail(24).copy()
        
        # Current (latest) row (make a copy to prevent warnings)
        latest_row = df.iloc[-1].copy()
        
        pm25_val = float(latest_row['components_pm2_5'])
        pm10_val = float(latest_row['components_pm10'])
        no2_val = float(latest_row['components_no2'])
        o3_val = float(latest_row['components_o3'])
        so2_val = float(latest_row['components_so2'])
        co_val = float(latest_row['components_co'])
        nh3_val = float(latest_row['components_nh3'])
        no_val = float(latest_row.get('components_no', 0.0))
        
        # Query OpenWeatherMap Air Pollution API
        api_data = fetch_realtime_pollution(city_name)
        if api_data:
            print(f"[{city_name}] Successfully integrated real-time API values.")
            pm25_val = float(api_data.get('pm2_5', pm25_val))
            pm10_val = float(api_data.get('pm10', pm10_val))
            no2_val = float(api_data.get('no2', no2_val))
            o3_val = float(api_data.get('o3', o3_val))
            so2_val = float(api_data.get('so2', so2_val))
            co_val = float(api_data.get('co', co_val))
            nh3_val = float(api_data.get('nh3', nh3_val))
            no_val = float(api_data.get('no', no_val))
            
            # Sync latest_row Series for subsequent logic (dominant source, round check, etc.)
            latest_row['components_pm2_5'] = pm25_val
            latest_row['components_pm10'] = pm10_val
            latest_row['components_no2'] = no2_val
            latest_row['components_o3'] = o3_val
            latest_row['components_so2'] = so2_val
            latest_row['components_co'] = co_val
            latest_row['components_nh3'] = nh3_val
            latest_row['components_no'] = no_val
            
            # Update the last row of df_recent to keep historical metrics, trends, and anomalies completely aligned
            df_recent.iloc[-1, df_recent.columns.get_loc('components_pm2_5')] = pm25_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_pm10')] = pm10_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_no2')] = no2_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_o3')] = o3_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_so2')] = so2_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_co')] = co_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_nh3')] = nh3_val
            df_recent.iloc[-1, df_recent.columns.get_loc('components_no')] = no_val
            
            from datetime import datetime
            updated_time = f"Live API {datetime.now().strftime('%I:%M %p')}"
        else:
            print(f"[{city_name}] Query failed or offline; using historical fallback values.")
            updated_time = "Just updated (Historical)"

        # Calculate AQI
        aqi_pm25 = calculate_us_aqi_pm25(pm25_val)
        aqi_pm10 = calculate_us_aqi_pm10(pm10_val)
        current_aqi = max(aqi_pm25, aqi_pm10)
        status = get_aqi_status(current_aqi)

        # Determine dominant pollutant
        pollutant_ratios = {
            "PM2.5": pm25_val / WHO_LIMITS["pm25"],
            "PM10": pm10_val / WHO_LIMITS["pm10"],
            "NO2": no2_val / WHO_LIMITS["no2"],
            "O3": o3_val / WHO_LIMITS["o3"]
        }
        dominant_p = max(pollutant_ratios, key=pollutant_ratios.get)
        dominant_val = f"{round(pm25_val if dominant_p == 'PM2.5' else (pm10_val if dominant_p == 'PM10' else (no2_val if dominant_p == 'NO2' else o3_val)))} µg/m³"
        
        ratio = pollutant_ratios[dominant_p]
        if ratio > 3.0:
            dom_status = "Toxic"
        elif ratio > 1.0:
            dom_status = "Elevated"
        else:
            dom_status = "Compliant"

        # Trends (sample 7 intervals from last 24 hours)
        # Using every 4th hour: [-24, -20, -16, -12, -8, -4, -1]
        indices = [-24, -20, -16, -12, -8, -4, -1]
        trend_rows = [df_recent.iloc[idx] for idx in indices]
        
        trend_labels = []
        trend_pm25 = []
        trend_no2 = []
        trend_o3 = []
        
        for r in trend_rows:
            # datetime format typically: "d/m/yyyy H:MM" or "yyyy-mm-dd H:MM"
            dt_str = str(r['datetime'])
            time_part = dt_str.split()[-1] # extract "H:MM"
            # Format time part to HH:MM
            parts = time_part.split(':')
            if len(parts) >= 2:
                time_part = f"{int(parts[0]):02d}:{int(parts[1]):02d}"
            trend_labels.append(time_part)
            trend_pm25.append(round(float(r['components_pm2_5'])))
            trend_no2.append(round(float(r['components_no2'])))
            trend_o3.append(round(float(r['components_o3'])))

        # Heatmap (last 7 US AQI values)
        heatmap_aqi = []
        for idx in range(-7, 0):
            r = df_recent.iloc[idx]
            aqi_val = max(calculate_us_aqi_pm25(float(r['components_pm2_5'])), calculate_us_aqi_pm10(float(r['components_pm10'])))
            heatmap_aqi.append(aqi_val)

        # Count spikes in last 24h (where AQI > 150)
        spikes_24h = 0
        for i in range(len(df_recent)):
            r = df_recent.iloc[i]
            aqi_val = max(calculate_us_aqi_pm25(float(r['components_pm2_5'])), calculate_us_aqi_pm10(float(r['components_pm10'])))
            if aqi_val > 150:
                spikes_24h += 1

        # Anomalies listing
        anomalies_list = []
        landmarks = CITY_LANDMARKS[city_name]
        
        # Check for spike hours in the last 24 hours
        spike_indices = []
        for i in range(len(df_recent)):
            r = df_recent.iloc[i]
            aqi_val = max(calculate_us_aqi_pm25(float(r['components_pm2_5'])), calculate_us_aqi_pm10(float(r['components_pm10'])))
            if aqi_val > 150:
                spike_indices.append(i)

        # Build up to 3 actual anomaly events
        limit_anom = min(3, len(spike_indices))
        for idx in range(limit_anom):
            pos = spike_indices[-(idx + 1)]
            row_spk = df_recent.iloc[pos]
            spk_aqi = max(calculate_us_aqi_pm25(float(row_spk['components_pm2_5'])), calculate_us_aqi_pm10(float(row_spk['components_pm10'])))
            spk_source, spk_type = classify_dominant_source(row_spk)
            
            icon = "🏭"
            if "Vehicular" in spk_source: icon = "🚗"
            elif "Crop" in spk_source: icon = "🌾"
            elif "Dust" in spk_source: icon = "🌪️"
            
            dt_str = str(row_spk['datetime'])
            time_part = dt_str.split()[-1]
            parts = time_part.split(':')
            if len(parts) >= 2:
                hr = int(parts[0])
                mn = int(parts[1])
                ampm = "AM" if hr < 12 else "PM"
                hr_12 = hr % 12
                if hr_12 == 0: hr_12 = 12
                time_part = f"{hr_12:02d}:{mn:02d} {ampm}"

            anomalies_list.append({
                "icon": icon,
                "title": spk_source,
                "level": "High" if spk_aqi > 200 else "Medium",
                "location": landmarks[idx % len(landmarks)],
                "time": time_part
            })

        # Fallback if no anomalies found in last 24h, provide a default compliant one
        if not anomalies_list:
            anomalies_list.append({
                "icon": "🍃",
                "title": "Clean Air Zone",
                "level": "Low",
                "location": landmarks[0],
                "time": "Continuous"
            })

        # Source distribution weights (Normalized based on ratios)
        # Vehicular: NO2 ratio
        # Industrial: SO2/PM10 ratio
        # Agricultural: NH3 ratio
        r_veh = max(0.1, no2_val / WHO_LIMITS["no2"])
        r_ind = max(0.1, so2_val / WHO_LIMITS["so2"])
        r_agr = max(0.1, nh3_val / 80.0) # Normal NH3 threshold
        
        tot_ratio = r_veh + r_ind + r_agr
        dist_veh = round((r_veh / tot_ratio) * 100)
        dist_ind = round((r_ind / tot_ratio) * 100)
        dist_agr = 100 - dist_veh - dist_ind # ensures sum is exactly 100

        # AI Alert text
        main_source, _ = classify_dominant_source(latest_row)
        ai_alert_title = f"{city_name}: {main_source} surge detected."
        
        if current_aqi > 150:
            ai_alert_msg = f"Concentration levels of {dominant_p} have exceeded WHO safe limits by {round(ratio, 1)}x. Respiratory threat is High. Avoid outdoor exercise and wear filters."
        else:
            ai_alert_msg = f"Air quality index remains in the safe zone. Atmospheric parameters comply with WHO limits. No safety masks needed."

        # Map coords
        coords = CITY_MAP_COORDS[city_name]

        # Calculate alerts counts
        alerts_today = spikes_24h * 2
        delivered = int(alerts_today * 0.9)
        failed = alerts_today - delivered

        # Compile city object
        cities_data[city_name] = {
            "aqi": current_aqi,
            "status": status,
            "updated": updated_time,
            "pollutants": {
                "pm25": round(pm25_val),
                "pm10": round(pm10_val),
                "no2": round(no2_val),
                "o3": round(o3_val),
                "so2": round(so2_val),
                "co": round(co_val),
                "nh3": round(nh3_val),
                "no": round(float(latest_row['components_no']))
            },
            "activeSpikes": spikes_24h,
            "alertsToday": alerts_today,
            "deliveredAlerts": delivered,
            "failedAlerts": failed,
            "dominantPollutant": dominant_p,
            "dominantValue": dominant_val,
            "dominantStatus": dom_status,
            "trends24h": {
                "labels": trend_labels,
                "pm25": trend_pm25,
                "no2": trend_no2,
                "o3": trend_o3
            },
            "heatmap": heatmap_aqi,
            "anomalies": anomalies_list,
            "sourceDistribution": {
                "industrial": dist_ind,
                "agricultural": dist_agr,
                "vehicular": dist_veh
            },
            "aiAlert": {
                "title": ai_alert_title,
                "message": ai_alert_msg
            },
            "mapCoord": coords
        }

        # Seed global recent alerts table from worst spikes
        if current_aqi > 150:
            recent_alerts.append({
                "status": "Delivered",
                "time": "Just updated",
                "message": f"SmogNet Warning: {city_name} AQI peaked at {current_aqi} ({status}). Dominant source: {main_source}.",
                "recipient": "+923109661075"
            })

    # Default fallback alerts if empty
    if not recent_alerts:
        recent_alerts = [
            {
                "status": "Delivered",
                "time": "1 hour ago",
                "message": "Air Quality Advisory: Ambient atmospheric indices stable across major cities.",
                "recipient": "+923109661075"
            }
        ]

    # Output structure
    output_json = {
        "cities": cities_data,
        "recentAlerts": recent_alerts[:5]
    }

    # Write to file
    with open(AQI_DATA_PATH, "w") as f:
        json.dump(output_json, f, indent=2)
    
    print(f"Processed CSV datasets. Wrote output directly to {AQI_DATA_PATH}")

if __name__ == "__main__":
    generate_aqi_data()
