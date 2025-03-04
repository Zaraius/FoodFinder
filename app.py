from flask import Flask, render_template, request
import openai
import json

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = 'your-api-key-here'

# Sample restaurant data (you would replace this with your actual database)
# RESTAURANT_DATA = [
#     {
#         "name": "Pizza Palace",
#         "description": "Late night pizza joint with amazing toppings",
#         "price": "$",
#         "distance": 0.5,
#         "cuisine": "pizza"
#     },
#     # Add more restaurant data here
# ]

@app.route('/')
def home():
    return render_template('index.html')

# Sample restaurant data (you would replace this with your actual database)
RESTAURANT_DATA = [
    {
        "name": "Hot Doogy",
        "description": "Brazilian hot dogs and burgers",
        "price": "$$",
        "distance": 0.8,
        "cuisine": "Fast food"
    },
    {
        "name": "McDonalds",
        "description": "Classic American fast food",
        "price": "$",
        "distance": 0.3,
        "cuisine": "Fast food"
    },
    {
        "name": "Dunkin Donuts",
        "description": "Coffee and donuts",
        "price": "$",
        "distance": 1.2,
        "cuisine": "Cafe"
    },
    {
        "name": "iHop",
        "description": "Breakfast and pancakes",
        "price": "$$",
        "distance": 2.5,
        "cuisine": "American"
    },
    {
        "name": "Dave's Hot Chicken",
        "description": "Nashville-style hot chicken",
        "price": "$$",
        "distance": 1.5,
        "cuisine": "Fast food"
    }
]

@app.route('/search', methods=['POST'])
def search():
    # Simply return all restaurants for now
    return render_template('index.html', results=RESTAURANT_DATA)

    # REPLACE WITH THIS WHEN YOU GET OPENAI KEY
    # # Construct prompt for GPT
    # prompt = f"""
    # Given the following preferences:
    # Query: {query}
    # Price Range: {price_range}
    # Distance: {distance} miles
    # Cuisine Type: {cuisine}
    
    # Please analyze the following restaurant data and return the top 5 recommendations:
    # {json.dumps(RESTAURANT_DATA)}
    
    # Return only a JSON array of the top 5 matching restaurants with their details.
    # """

    # try:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant that recommends restaurants."},
    #             {"role": "user", "content": prompt}
    #         ]
    #     )
        
    #     # Parse the response and convert it to a list of restaurants
    #     results = json.loads(response.choices[0].message.content)
    #     return render_template('index.html', results=results)
    
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return render_template('index.html', error="Sorry, something went wrong!")

if __name__ == '__main__':
    app.run(debug=True) 