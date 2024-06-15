from flask import Flask, jsonify, render_template, request
import cohere
import agentops
from cohere import ChatMessage


agentops.init("INSERT_API_KEY")
co = cohere.Client(api_key='INSERT_API_KEY')

app = Flask(__name__)
chat_history = []

initial_prompt = (
        "Pretend to be a time & space traveller like Doctor Who (but not actually Doctor Who, you do not have a TARDIS etc.). "
        "You are now a tour guide focused on sharing information and interesting facts about points of interest, and helping people with their trips. "
        "Stay in character for each response. Keep answers shorter"
    )

@app.route('/')
def index():
    return render_template('chat.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')
        if user_input:
            response = co.chat(
                message=user_input,
                model='command-r-plus',
                preamble=initial_prompt,
                chat_history=chat_history,
            )
            bot_response = response.text
            chat_history.extend(
                [ChatMessage(role="USER", message=user_input),
                ChatMessage(role="CHATBOT", message=bot_response)]
            )
            return jsonify({"response": bot_response})
        return jsonify({"error": "No user input provided."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/end_session', methods=['POST'])
def end_session():
    agentops.end_session('Success')
    return jsonify({"message": "Session ended successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
