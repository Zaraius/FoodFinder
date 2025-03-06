from flask import Flask, render_template, request
import pandas as pd
import openai
import os
import json

class RestaurantChatbot:
    def __init__(self, csv_path):
        self.client = openai
        self.client.api_key = os.environ["OPENAI_API_KEY"]
        # Load the CSV file using pandas with explicit encoding
        try:
            self.df = pd.read_csv(csv_path, encoding='utf-8', encoding_errors='ignore')
        except UnicodeDecodeError:
            self.df = pd.read_csv(csv_path, encoding='latin-1')
        
    def get_response(self, query, price_range=None, distance=None):
        # Convert dataframe to a more structured format
        restaurants_list = self.df.to_dict('records')
        # Convert to JSON string and back to ensure clean serialization
        restaurants_data = json.dumps(restaurants_list, ensure_ascii=False).encode('utf-8').decode('utf-8')
        
        # Construct the system message
        system_message = """You are a helpful assistant that recommends restaurants based on user preferences. 
        Analyze the restaurant data and provide the top 5 most relevant recommendations.
        Format your response as a list of dictionaries with 'name', 'description', and 'price' keys.
        Keep descriptions concise and relevant to the query."""

        # Construct the user message with all preferences
        user_message = f"Based on this restaurant data, "
        user_message += f"find the best restaurants matching these criteria:\n"
        user_message += f"Query: {query}\n"
        if price_range:
            user_message += f"Price Range: {price_range}\n"
        if distance:
            user_message += f"Distance: Within {distance} miles\n"
        user_message += "\nProvide exactly 5 recommendations in this format:\n"
        user_message += "[{'name': 'Restaurant Name', 'description': 'Brief description', 'price': 'Price range'}]"

        user_message = user_message.encode("utf-8", "ignore").decode("utf-8")
        restaurants_data = restaurants_data.encode("utf-8", "ignore").decode("utf-8")
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": f"I'll analyze this data: {restaurants_data}"}
                ],
                temperature=0.7
            )
            
            # Extract the response and convert it to Python object
            response_text = response.choices[0].message['content']
            try:
                # First try json.loads
                results = json.loads(response_text)
                return results
            except json.JSONDecodeError:
                try:
                    # Fallback to ast.literal_eval
                    import ast
                    results = ast.literal_eval(response_text)
                    return results
                except:
                    return [{"name": "Error", "description": "Could not parse results", "price": "N/A"}]
                
        except Exception as e:
            print(f"Error: {e}")
            return [{"name": "Error", "description": str(e), "price": "N/A"}]

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbot once when starting the server
chatbot = RestaurantChatbot(
    csv_path='mvp_database_cleaned.csv'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    price_range = request.form.get('price_range', '')
    distance = request.form.get('distance', '')

    try:
        results = chatbot.get_response(query, price_range, distance)
        return render_template('index.html', results=results)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Sorry, something went wrong!")

if __name__ == '__main__':
    app.run(debug=True)