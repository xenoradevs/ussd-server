
"""
Implements a USSD server that allows users to purchase stamps via USSD.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store user sessions and their states
user_sessions = {}

# USSD algorithm constants
MAIN_MENU = "1. Buy Stamps\n2. Exit"
STAMP_TYPES = {"1": "Type A", "2": "Type B", "3": "Type C"}
PAYMENT_OPTIONS = {"1": "Confirm Purchase", "2": "Cancel Transaction"}

# USSD session states
SESSION_STATE_MAIN_MENU = "main_menu"
SESSION_STATE_QUANTITY = "quantity"
SESSION_STATE_CONFIRMATION = "confirmation"
SESSION_STATE_PAYMENT = "payment"

# Mock function to simulate payment initiation


def initiate_payment():
    """
    Initiates a payment transaction.

    Returns:
        bool: True if payment was successfully initiated, False otherwise.
    """
    # Implement actual payment initiation logic here
    return True

# Mock function to generate a coupon code


def generate_coupon_code():
    """
    Generates a unique coupon code.

    Returns:
        str: A string representing the generated coupon code.
    """
    # Implement actual coupon code generation logic here
    return "ABC123"

# USSD application logic


def ussd_algorithm(session_id, user_input):
    """
    Implements the USSD algorithm for a mobile payment system.

    Args:
        session_id (str): The unique identifier for the user's session.
        user_input (str): The user's input.

    Returns:
        str: The response to be sent back to the user.

    """
    if session_id not in user_sessions:
        user_sessions[session_id] = {"state": SESSION_STATE_MAIN_MENU}

    state = user_sessions[session_id]["state"]

    if state == SESSION_STATE_MAIN_MENU:
        response = MAIN_MENU

    elif state == SESSION_STATE_QUANTITY:
        stamp_type = STAMP_TYPES.get(user_input)
        if stamp_type:
            response = f"Enter quantity for {stamp_type}:"
            user_sessions[session_id]["selected_stamp_type"] = stamp_type
            user_sessions[session_id]["state"] = SESSION_STATE_CONFIRMATION
        else:
            response = "Invalid selection. Please try again."

    elif state == SESSION_STATE_CONFIRMATION:
        if user_input == "1":
            response = "1. Orange Money\n2. MTN Mobile Money\nSelect payment method:"
            user_sessions[session_id]["state"] = SESSION_STATE_PAYMENT
        elif user_input == "2":
            response = "Transaction canceled. Goodbye!"
            del user_sessions[session_id]
        else:
            response = "Invalid selection. Please try again."

    elif state == SESSION_STATE_PAYMENT:
        if user_input == "1" or user_input == "2":
            payment_success = initiate_payment()  # Mock payment initiation
            if payment_success:
                coupon_code = generate_coupon_code()  # Mock coupon code generation
                response = f"Your Coupon code is {coupon_code}\nThank you for your purchase!"
                del user_sessions[session_id]
            else:
                response = "Payment failed. Please try again."
        else:
            response = "Invalid selection. Please try again."

    return response


@app.route('/ussd', methods=['POST'])
def ussd_callback():
    """
    This function handles the USSD callback from the mobile network operator.
    It retrieves the session ID and user input from the request, passes them to the
    ussd_algorithm function to generate a response, and returns the response as a JSON object.
    """
    session_id = request.form.get('sessionId')
    user_input = request.form.get('text')

    response = ussd_algorithm(session_id, user_input)

    return jsonify({"text": response, "sessionState": "continue"})


if __name__ == '__main__':
    app.run(debug=True)
