import geocoder
import overpy


def find_hospitals_near_me(radius=1000):
    # Get your current device location
    location = geocoder.ip('me')
    # latitude = 13.092345436432021
    latitude = 13.02249
    longitude = 80.01816

    # Initialize the Overpass API
    api = overpy.Overpass()

    # Define the bounding box for your search (within a certain radius)
    min_lat = latitude - (radius / 111000)
    max_lat = latitude + (radius / 111000)
    min_lon = longitude - (radius / (111000 * abs(latitude)))
    max_lon = longitude + (radius / (111000 * abs(latitude)))

    # Query for hospitals within the bounding box
    query = f"""
        [out:json];
        node["amenity"="hospital"]({min_lat},{min_lon},{max_lat},{max_lon});
        out;
    """

    result = api.query(query)

    # Process the results
    hospital_info = []

    for node in result.nodes:
        hospital_latitude = float(node.lat)
        hospital_longitude = float(node.lon)
        name = node.tags.get("name", "Unknown")

        # Calculate the distance using geodesic
        distance = geocoder.distance((latitude, longitude), (hospital_latitude, hospital_longitude))

        hospital_info.append({"name": name, "distance": distance})

    return hospital_info


if __name__ == "__main__":
    hospitals_near_me = find_hospitals_near_me(radius=3000)

    if hospitals_near_me:
        print("Hospitals near your location:")
        for hospital in hospitals_near_me:
            print(f"- {hospital['name']}, Distance: {hospital['distance']:.2f} kilometers")
    else:
        print("No hospitals found near your location.")

