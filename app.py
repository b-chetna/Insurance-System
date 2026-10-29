from flask import (
    Flask,
    request,
    jsonify,
    render_template_string,
    redirect,
    url_for
)

app = Flask(__name__)

claims = []
next_claim_id = 1


HTML = """
<!DOCTYPE html>
<html>
<head>

<title>Insurance Claim System</title>

<style>

body {
    font-family: Arial, sans-serif;
    max-width: 1100px;
    margin: 40px auto;
    padding: 20px;
    background: #f4f6f9;
}

h1, h2 {
    color: #173b68;
}

form, .claims-section {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
}

input, textarea, button, select {
    box-sizing: border-box;
    width: 100%;
    margin: 8px 0;
    padding: 10px;
}

button {
    background: #173b68;
    color: white;
    border: none;
    cursor: pointer;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th, td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
}

th {
    background: #173b68;
    color: white;
}

tr:nth-child(even) {
    background: #f2f2f2;
}

.success {
    color: green;
}

</style>

</head>

<body>

<h1>Insurance Claim System - V3</h1>

{% if message %}
<p class="success">{{ message }}</p>
{% endif %}

<h2>Add Claim</h2>

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

<h2>View Claims</h2>

<div class="claims-section">

{% if claims %}

<table>

<thead>

<tr>
    <th>ID</th>
    <th>Claimant</th>
    <th>Policy Number</th>
    <th>Amount</th>
    <th>Description</th>
    <th>Status</th>
    <th>Update Status</th>
</tr>

</thead>

<tbody>

{% for claim in claims %}

<tr>

<td>{{ claim.id }}</td>

<td>{{ claim.claimant }}</td>

<td>{{ claim.policy_number }}</td>

<td>{{ "%.2f"|format(claim.amount) }}</td>

<td>{{ claim.description }}</td>

<td>{{ claim.status }}</td>

<td>

<form
    action="/update/{{ claim.id }}"
    method="POST"
>

<select name="status" required>

<option
    value="Pending"
    {% if claim.status == "Pending" %}selected{% endif %}
>
Pending
</option>

<option
    value="Approved"
    {% if claim.status == "Approved" %}selected{% endif %}
>
Approved
</option>

<option
    value="Rejected"
    {% if claim.status == "Rejected" %}selected{% endif %}
>
Rejected
</option>

</select>

<button type="submit">
Update
</button>

</form>

</td>

</tr>

{% endfor %}

</tbody>

</table>

{% else %}

<p>No claims submitted yet.</p>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/")
def home():

    message = request.args.get("message", "")

    return render_template_string(
        HTML,
        claims=claims,
        message=message
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "version": "3"
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


@app.route("/claims")
def view_claims():

    return jsonify(claims), 200


@app.route(
    "/update/<int:claim_id>",
    methods=["POST"]
)
def update_claim(claim_id):

    new_status = request.form.get(
        "status", ""
    )

    allowed_statuses = {
        "Pending",
        "Approved",
        "Rejected"
    }

    if new_status not in allowed_statuses:

        return "Invalid claim status", 400

    for claim in claims:

        if claim["id"] == claim_id:

            claim["status"] = new_status

            return redirect(
                url_for(
                    "home",
                    message="Claim status updated successfully!"
                )
            )

    return "Claim not found", 404


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )