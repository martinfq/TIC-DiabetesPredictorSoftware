from flask import Blueprint, jsonify
from ..db.neo4j import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/test_db', methods=['GET'])
def test_db_connection():
    try:
        with db.driver.session() as session:
            result = session.run("RETURN 'Neo4j connection successful' AS message")
            message = result.single()["message"]
            return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
