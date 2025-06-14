from flask import Flask, request, jsonify
from connect_memory_with_llm import response

# Initialize Flask app
app = Flask(__name__)

# Define the API endpoint for the question-answering service
@app.route('/rag', methods=['GET'])
def query():
    # Get the 'query' parameter from the GET request
    user_query = request.args.get('query')  # Renaming to 'user_query' for clarity

    # Check if the 'query' parameter is provided
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Call the response function with the user query
    result = response(user_query)

    # Return the result as a JSON response
    return jsonify({
        "result": result,  # Assuming result is a tuple, and we want the answer text
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5000)


