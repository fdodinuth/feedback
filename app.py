from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.get_json()  # Parse JSON data
    rating = feedback_data.get('rating')
    feedback_text = feedback_data.get('feedback')

    # Save feedback to a JSON file (feedback.json)
    feedback = {'rating': rating, 'feedback': feedback_text}
    with open('feedback.json', 'a') as file:
        json.dump(feedback, file)
        file.write('\n')

    return jsonify({'status': 'success'}), 200

@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')

@app.route('/view_feedback')
def view_feedback():
    # Read the feedback from the JSON file
    feedbacks = []
    try:
        with open('feedback.json', 'r') as file:
            feedbacks = [json.loads(line) for line in file]
    except FileNotFoundError:
        pass

    return render_template('view_feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
