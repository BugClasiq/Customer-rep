from flask import Blueprint, request, jsonify, current_app

from ai.engine import generate_response

chat_bp = Blueprint("chat", __name__, url_prefix="/api")


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or data.get("text") or "").strip()
    history = data.get("history") if isinstance(data.get("history"), list) else []

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = generate_response(message, chat_history=history,
                                   app_context=current_app.app_context())
    except Exception:
        current_app.logger.exception("Chat assistant failed")
        return jsonify({
            "error": "Assistant unavailable. Check GROQ_API_KEY, the database connection and the seed data."
        }), 503

    return jsonify({
        "response": result["response"],
        "intent": result["intent"],
        "context": result["context"],
        "chat_history": result["chat_history"],
    }), 200
