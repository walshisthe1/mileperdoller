from flask import Flask, render_template, request
import googlemaps
from statistics import mean
import os

app = Flask(__name__)

# Replace with your API key
GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY_HERE'
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_gas_prices(latitude, longitude, fuel_type='regular'):
    # Search for gas stations within 5000 meters (about 3 miles)
    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=5000,
        type='gas_station'
    )
    
    # This would need to be replaced with actual price parsing
    # Currently, Google doesn't provide direct gas prices
    # This is a placeholder for demonstration
    if fuel_type == 'premium':
        return 4.50  # Placeholder premium price
    return 3.50  # Placeholder regular price

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        mpg = float(request.form['mpg'])
        distance = float(request.form['distance'])
        
        # Check if using auto gas price
        if 'use_auto_price' in request.form:
            # For demo, using San Francisco coordinates
            latitude = 37.7749
            longitude = -122.4194
            fuel_type = request.form.get('fuel_type', 'regular')
            gas_price = get_gas_prices(latitude, longitude, fuel_type)
        else:
            gas_price = float(request.form['gas_price'])
        
        gallons_needed = distance / mpg
        total_cost = gallons_needed * gas_price
        cost_per_mile = total_cost / distance
        
        return render_template('index.html', 
                             cost_per_mile=f"{cost_per_mile:.2f}",
                             total_cost=f"{total_cost:.2f}",
                             calculated=True,
                             auto_price=gas_price)
    
    return render_template('index.html', calculated=False)

if __name__ == '__main__':
    app.run(debug=True)
