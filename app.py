from connect_memory_with_llm import response
from flask import Flask, request, jsonify

app = Flask(__name__)


# Route for the API endpoint
@app.route('/search', methods=['GET'])
def search_csv():
    user_query = request.args.get('prompt')
    if not user_query:
        return jsonify({'error': 'Prompt parameter is required'}), 400
    try:
        matching_data = response(user_query)
        return jsonify(matching_data)
    except Exception as e:
        # Log or print error for debugging
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')

