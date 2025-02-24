from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

def get_hotels(destination):
    check_in = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    check_out = (datetime.now() + timedelta(days=33)).strftime("%Y-%m-%d")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = f"https://www.booking.com/searchresults.html?ss={destination}&checkin={check_in}&checkout={check_out}"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        hotels = []
        property_cards = soup.select('[data-testid="property-card"]')
        
        for card in property_cards[:10]:
            try:
                name = card.select_one('[data-testid="title"]').text.strip()
                price = card.select_one('.fcab3ed991').text.strip() if card.select_one('.fcab3ed991') else "N/A"
                rating = card.select_one('[data-testid="review-score"]').text.strip() if card.select_one('[data-testid="review-score"]') else "N/A"
                location = card.select_one('[data-testid="address"]').text.strip() if card.select_one('[data-testid="address"]') else "N/A"
                
                hotels.append({
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'location': location
                })
            except:
                continue
                
        return hotels
    except Exception as e:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<destination>')
def search(destination):
    hotels = get_hotels(destination)
    return jsonify(hotels)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
