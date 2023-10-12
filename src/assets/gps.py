import re

def dms_to_decimal(gps_data):
    # Define a regular expression pattern to extract degrees, minutes, and direction.
    pattern = r'(\d+)°(\d+)’([NSWE])/(\d+)°(\d+)’([NSWE])'
    
    # Use re.search to find the matches in the input GPS data.
    match = re.search(pattern, gps_data)
    
    if match:
        # Extract the relevant components.
        lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = match.groups()
        
        # Convert degrees and minutes to decimal degrees.
        latitude = float(lat_deg) + float(lat_min) / 60
        longitude = float(lon_deg) + float(lon_min) / 60
        
        # Determine the sign for latitude and longitude based on the direction.
        if lat_dir in ['S', 's', 'W', 'w']:
            latitude = -latitude
        if lon_dir in ['S', 's', 'W', 'w']:
            longitude = -longitude
        
        return f"{latitude:.6f}, {longitude:.6f}"
    else:
        return "Invalid GPS data format"

# Example usage:
for gps_data in ['00°00’N/77°46’W', '00°12’N/76°51’W']:
    decimal_coords = dms_to_decimal(gps_data)
    print(decimal_coords)