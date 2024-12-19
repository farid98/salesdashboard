import pandas as pd
from geopy.geocoders import Nominatim
import time

# Load your data (replace with your actual file)
df = pd.read_csv("dummy_sales_data.csv")

# Ensure columns are present
if "City" not in df.columns or "State" not in df.columns:
    raise ValueError("Data must have 'City' and 'State' columns.")

# Create a unique list of city-state combinations
df["City_State"] = df["City"] + ", " + df["State"]
unique_locations = df["City_State"].unique()

# Initialize geocoder (User-Agent required by Nominatim)
geolocator = Nominatim(user_agent="my_geocoder")

# Dictionary to store location to (lat, lon) mapping
location_coords = {}

for loc in unique_locations:
    # Geocode each city-state
    try:
        # To avoid hitting rate limits, you might want to slow down requests:
        time.sleep(1)  # Pause for a second between requests (adjust as needed)

        location = geolocator.geocode(loc + ", USA")
        # Adding ", USA" might help if you know it's US data

        if location:
            location_coords[loc] = (location.latitude, location.longitude)
        else:
            location_coords[loc] = (None, None)
    except Exception as e:
        print(f"Error geocoding {loc}: {e}")
        location_coords[loc] = (None, None)

# Create a DataFrame of the coordinates
coord_df = pd.DataFrame(location_coords.items(), columns=["City_State", "Coords"])
coord_df[["Latitude", "Longitude"]] = pd.DataFrame(
    coord_df["Coords"].tolist(), index=coord_df.index
)
coord_df.drop(columns="Coords", inplace=True)

# Merge coordinates back into the original DataFrame
df = df.merge(coord_df, on="City_State", how="left")

# Now df has 'Latitude' and 'Longitude' columns for each row
print(df.head())

# Optionally, save the updated data to a new CSV
df.to_csv("dummy_sales_data_with_coords.csv", index=False)
