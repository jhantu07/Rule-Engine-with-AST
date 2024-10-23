from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ast_builder import create_ast, evaluate_ast

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Rule model
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Rule {self.id}: {self.rule_string}>"

# Create the database and tables
with app.app_context():
    db.create_all()  # Create database tables

# Dummy storage for rules
rules = []

# Create a new rule
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule')
    rule_ast = create_ast(rule_string)  # Generate AST
    new_rule = Rule(rule_string=rule_string)
    db.session.add(new_rule)  # Add new rule to the session
    db.session.commit()  # Commit the session to save to the database
    rules.append(rule_ast)  # Optionally keep it in memory as well
    return jsonify({"message": "Rule created successfully", "rule": str(rule_ast)})

# Combine rules
@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rules_from_db = Rule.query.all()  # Fetch all rules from the database
    combined_rule = " AND ".join([rule.rule_string for rule in rules_from_db])
    return jsonify({"combined_rule": combined_rule})

# Evaluate rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    data = request.json.get('data')  # User data
    rules_from_db = Rule.query.all()  # Fetch all rules from the database
    if not rules_from_db:
        return jsonify({"result": False, "message": "No rules available for evaluation."})

    # For now, let's just evaluate the first rule
    rule_ast = create_ast(rules_from_db[0].rule_string)  # Assume the first rule
    result = evaluate_ast(rule_ast, data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
