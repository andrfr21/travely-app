from flask import Flask, request, jsonify, render_template
import requests
import time

app = Flask(__name__)

# -------------------------
# Pages existantes
# -------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/creer_voyage')
def creer_voyage():
    return render_template('creer_voyage.html')

@app.route('/fonctionnement')
def fonctionnement():
    return render_template('fonctionnement.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/se_connecter')
def se_connecter():
    return render_template('se_connecter.html')

@app.route('/a_propos')
def a_propos():
    # Si tu n'as pas a_propos.html, garde cette route ou enlève-la.
    return render_template('a_propos.html')

# -------------------------
# Nouvelles pages IA & suivi
# -------------------------
@app.route('/assistant')
def assistant():
    return render_template('assistant.html')

@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/mes_voyages')
def mes_voyages():
    return render_template('mes_voyages.html')

@app.route('/carte')
def carte():
    return render_template('carte.html')

# -------------------------
# Mock APIs "branchables"
# -------------------------
@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    Réponse IA factice (pour la démo). On branchera OpenAI/Anthropic plus tard.
    Le front enverra éventuellement aussi des préférences utilisateur.
    """
    payload = request.get_json(silent=True) or {}
    user_msg = payload.get('message', '').strip()
    if not user_msg:
        return jsonify({"reply": "Dis-moi ta prochaine destination ✈️"}), 200
    # Petite "latence" simulée pour l'effet streaming (facultatif)
    time.sleep(0.2)
    return jsonify({
        "reply": (
            f"Super idée ! Je te prépare un itinéraire pour: {user_msg} ✨\n"
            f"Souhaites-tu des activités plutôt culture, gastronomie ou nature ?"
        )
    }), 200

@app.route('/api/suggestions')
def api_suggestions():
    """
    Pagination pour le défilement infini de l'accueil.
    """
    page = int(request.args.get('page', 1))
    base = (page - 1) * 12
    items = [{"title": f"Destination {base + i + 1}", "subtitle": "Locations de vacances"} for i in range(12)]
    next_page = page + 1 if page < 5 else None
    return jsonify({"items": items, "next": next_page})

@app.route('/api/positions')
def api_positions():
    """
    Points d'un itinéraire (mock) pour la carte.
    """
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {"type":"Feature","geometry":{"type":"Point","coordinates":[2.3522,48.8566]},"properties":{"label":"Paris"}},
            {"type":"Feature","geometry":{"type":"Point","coordinates":[7.2619,43.7102]},"properties":{"label":"Nice"}},
            {"type":"Feature","geometry":{"type":"Point","coordinates":[11.2558,43.7696]},"properties":{"label":"Florence"}}
        ]
    }
    return jsonify(geojson)

# -------------------------
# /search existant (mocké) — à brancher plus tard
# -------------------------
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    destination = data['destination']
    start_date = data['start_date']
    end_date = data['end_date']
    budget = data['budget']
    type_of_trip = data['type_of_trip']
    
    accommodation_results = query_accommodation_api(destination, start_date, end_date, budget, type_of_trip)
    activity_results = query_activity_api(destination, start_date, end_date)

    return jsonify({
        'accommodations': accommodation_results,
        'activities': activity_results
    })

def query_accommodation_api(destination, start_date, end_date, budget, type_of_trip):
    # Endpoints de démonstration (placeholders) — à remplacer par de vrais
    booking_api_url = "https://api.booking.com/v1/hotels"
    airbnb_api_url = "https://api.airbnb.com/v2/search_results"

    booking_params = {
        'destination': destination,
        'check_in': start_date,
        'check_out': end_date,
        'price_max': budget,
        'type': type_of_trip
    }

    airbnb_params = {
        'location': destination,
        'check_in': start_date,
        'check_out': end_date,
        'max_price': budget,
    }

    # Mock d'appels
    try:
        booking_response = requests.get(booking_api_url, params=booking_params, timeout=3)
    except Exception:
        class _R: 
            status_code = 200
            def json(self): 
                return {'hotels':[{'name':'Hotel Demo Booking','price':120},{'name':'Booking Plaza','price':180}]}
        booking_response = _R()

    try:
        airbnb_response = requests.get(airbnb_api_url, params=airbnb_params, timeout=3)
    except Exception:
        class _R:
            status_code = 200
            def json(self):
                return {'listings':[{'title':'Airbnb Cosy','price':90},{'title':'Loft Central','price':150}]}
        airbnb_response = _R()

    accommodations = []
    if booking_response.status_code == 200:
        accommodations.extend(booking_response.json().get('hotels', []))
    if airbnb_response.status_code == 200:
        accommodations.extend(airbnb_response.json().get('listings', []))
    return accommodations

def query_activity_api(destination, start_date, end_date):
    # Endpoints de démonstration — à remplacer
    tripadvisor_api_url = "https://api.tripadvisor.com/v2/activities"
    viator_api_url = "https://api.viator.com/v1/tours"

    tripadvisor_params = {
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
    }
    viator_params = {
        'location': destination,
        'start_date': start_date,
        'end_date': end_date,
    }

    try:
        tripadvisor_response = requests.get(tripadvisor_api_url, params=tripadvisor_params, timeout=3)
    except Exception:
        class _R:
            status_code = 200
            def json(self):
                return {'activities':[{'name':'Visite guidée','price':35},{'name':'Cours de cuisine','price':55}]}
        tripadvisor_response = _R()

    try:
        viator_response = requests.get(viator_api_url, params=viator_params, timeout=3)
    except Exception:
        class _R:
            status_code = 200
            def json(self):
                return {'tours':[{'name':'Tour à vélo','price':29},{'name':'Excursion vin','price':69}]}
        viator_response = _R()

    activities = []
    if tripadvisor_response.status_code == 200:
        activities.extend(tripadvisor_response.json().get('activities', []))
    if viator_response.status_code == 200:
        activities.extend(viator_response.json().get('tours', []))
    return activities

if __name__ == '__main__':
    app.run(debug=True)
