from flask import Flask, request, jsonify, render_template, session
import openai
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Load restaurant data
with open("restaurants.json", "r") as file:
    restaurant_data = json.load(file)

# OpenAI API key (ensure it's set in the environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

class RestaurantChatbot:
    def __init__(self, data):
        self.data = data

    def get_response(self, query, price_range=None, distance=None):
        """Send all restaurant data to OpenAI and let it decide."""
        
        system_message = (
            "You are a helpful restaurant recommendation chatbot. "
            "Users will ask for food recommendations, and you should suggest the best options "
            "from the provided list of restaurants. Consider their preferences, but if no exact match exists, "
            "offer something similar."
        )

        user_message = f"I am looking for {query} within {distance} miles and my budget is {price_range}. Can you recommend something?"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message + "\n\nHere is the restaurant data:\n" + json.dumps(self.data, ensure_ascii=False)}
                ],
                max_tokens=350,
                temperature=0.7
            )

            return response["choices"][0]["message"]["content"].strip()

        except openai.error.OpenAIError as e:
            print(f"API Error: {e}")
            return "Oops! Something went wrong. Want to try again?"

# Initialize chatbot
chatbot = RestaurantChatbot(data=restaurant_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_conversation', methods=['GET'])
def start_conversation():
    session['step'] = 'food'
    return jsonify({"response": "Hi! What type of food are you craving today?"})

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('user_input', '').strip()
    current_step = session.get('step', 'food')

    if current_step == 'food':
        session['food'] = user_input
        session['step'] = 'price_range'
        return jsonify({"response": "Got it! What is your budget for the meal?"})
    
    elif current_step == 'price_range':
        session['price_range'] = user_input
        session['step'] = 'distance'
        return jsonify({"response": "Thanks! How far are you willing to travel?"})
    
    elif current_step == 'distance':
        session['distance'] = user_input
        session['step'] = 'done'
        food = session.get('food')
        price_range = session.get('price_range')
        distance = int(user_input) if user_input.isdigit() else None

        recommendations = chatbot.get_response(food, price_range, distance)
        return jsonify({"response": recommendations})

    return jsonify({"response": "I'm here to help! What kind of food are you craving?"})

if __name__ == '__main__':
    app.run(debug=True)
