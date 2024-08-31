from flask import Flask, request, g
import logging
import time
from devlabs_recommender_system.recommender import recommend_architect
from devlabs_recommender_system.utils.logger import setup_logging
from devlabs_recommender_system.utils.response_wrapper import success_response, error_response

app = Flask(__name__)
setup_logging()

@app.before_request
def log_request_info():
    g.start_time = time.time()
    g.ip_address = request.remote_addr
    g.method = request.method
    g.route = request.path

@app.after_request
def log_response_info(response):
    duration = time.time() - g.start_time
    logging.info(f"IP: {g.ip_address} | Method: {g.method} | Route: {g.route} | Duration: {duration:.2f}s | Status: {response.status_code}")
    return response

@app.route('/api', methods=['GET'])
def index():
    return success_response(message="This service is running properly")

@app.route('/api/architects/recommend', methods=['POST'])
def get_architect_recommendations():
    payload = request.get_json()
    project_data = payload.get('project')
    architects_data = payload.get('architects')
    
    recommendations = recommend_architect(project_data, architects_data)

    return success_response(data=recommendations, message="Recommendations generated successfully")

@app.errorhandler(404)
def page_not_found(e):
    return error_response(message="Not Found", status_code=404)

@app.errorhandler(500)
def internal_server_error(e):
    return error_response(message="Internal Server Error", status_code=500)

if __name__ == "__main__":
    app.run(debug=True)