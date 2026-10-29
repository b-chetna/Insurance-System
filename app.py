from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)

claims = []
next_claim_id = 1


HTML = """
<!DOCTYPE html>
<html>
<head>

<title>Insurance Claim System - V1</title>

<style>

body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    background: #f4f6f9;
}

h1, h2 {
    color: #173b68;
}

form {
    background: white;
    padding: 25px;
    border-radius: 10px;
}

input, textarea, button {
    box-sizing: border-box;
    width: 100%;
    margin: 10px 0;
    padding: 12px;
}

button {
    background: #173b68;
    color: white;
    border: none;
    cursor: pointer;
}

.success {
    color: green;
}

</style>

</head>

<body>

<h1>Insurance Claim System - V1</h1>

<h2>Add Insurance Claim</h2>

{% if message %}
<p class="success">{{ message }}</p>
{% endif %}

<form action="/add" method="POST">

<label>Claimant Name</label>

<input
    type="text"
    name="claimant"
    required
>

<label>Policy Number</label>

<input
    type="text"
    name="policy_number"
    required
>

<label>Claim Amount</label>

<input
    type="number"
    name="amount"
    min="0.01"
    step="0.01"
    required
>

<label>Description</label>

<textarea
    name="description"
    required
></textarea>

<button type="submit">
Submit Claim
</button>

</form>

</body>
</html>
"""


@app.route("/")
def home():

    message = request.args.get("message", "")

    return render_template_string(
        HTML,
        message=message
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "version": "1"
    }), 200


@app.route("/add", methods=["POST"])
def add_claim():

    global next_claim_id

    claimant = request.form.get(
        "claimant", ""
    ).strip()

    policy_number = request.form.get(
        "policy_number", ""
    ).strip()

    description = request.form.get(
        "description", ""
    ).strip()

    amount_text = request.form.get(
        "amount", ""
    ).strip()

    if not claimant:

        return "Claimant name is required", 400

    if not policy_number:

        return "Policy number is required", 400

    if not description:

        return "Description is required", 400

    try:

        amount = float(amount_text)

    except (ValueError, TypeError):

        return "Invalid claim amount", 400

    if amount <= 0:

        return "Claim amount must be positive", 400

    claim = {

        "id": next_claim_id,

        "claimant": claimant,

        "policy_number": policy_number,

        "amount": amount,

        "description": description,

        "status": "Pending"

    }

    claims.append(claim)

    next_claim_id += 1

    return redirect(
        url_for(
            "home",
            message="Claim submitted successfully!"
        )
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )