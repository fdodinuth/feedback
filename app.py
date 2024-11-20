from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Route to handle feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.get_json()  # Parse JSON data
    rating = feedback_data.get('rating')
    feedback_text = feedback_data.get('feedback')

    # Save feedback to a JSON file (feedback.json)
    feedback = {'rating': rating, 'feedback': feedback_text}
    try:
        # Open file in append mode to add new feedback
        with open('feedback.json', 'a') as file:
            json.dump(feedback, file)
            file.write('\n')
    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)}), 500

    return jsonify({'status': 'success'}), 200

# Route to show feedback submission form
@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')

# Route to display submitted feedback
@app.route('/view_feedback')
def view_feedback():
    feedbacks = []
    try:
        with open('feedback.json', 'r') as file:
            feedbacks = [json.loads(line) for line in file]
    except FileNotFoundError:
        pass  # If file doesn't exist, just return an empty list of feedbacks

    return render_template('view_feedback.html', feedbacks=feedbacks)

# Route to download feedback.json file
@app.route('/download_feedback')
def download_feedback():
    try:
        if os.path.exists('feedback.json'):
            with open('feedback.json', 'r') as file:
                feedback_data = file.read()
            response = jsonify(feedback_data)
            response.headers["Content-Disposition"] = "attachment; filename=feedback.json"
            response.mimetype = "application/json"
            return response
        else:
            return jsonify({'status': 'failure', 'error': 'Feedback file not found'}), 404
    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
