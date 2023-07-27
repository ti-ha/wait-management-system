from flask import Blueprint
from wms import *
from middlewares import backend, token_optional, token_required, call
from flask import request, jsonify

service_blueprint = Blueprint("service", __name__)

@service_blueprint.route("/servicerequests/queue", methods = ['GET'], endpoint='show_request_queue')
@token_required
def show_request_queue(current_user):
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Access denied"}), 401
    
    return call(
        None,
        backend.srm_handler.jsonify
    )

@service_blueprint.route("/servicerequests/history", methods = ['GET'], endpoint='show_request_history')
@token_required
def show_request_history(current_user):
    if current_user.__class__ is not Manager:
        return jsonify({"error": "Must be a Manager to make this request"}), 401
    
    return call(
        None,
        backend.srm_handler.srm.jsonify_history
    )

@service_blueprint.route("/servicerequests/queue", methods = ['POST'], endpoint="add_request_to_queue")
def add_request_to_queue():
    """
    JSON FORMAT:
    {
        "subject": "string",
        "summary": "string",
        "table_id": int
    }
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        obj = request.json
        try:
            subject = obj["subject"]
            summary = obj["summary"]
            table_id = obj["table_id"]
        except KeyError:
            return jsonify({"error": "Incorrect fields"}), 400
        
        table = backend.table_handler.id_to_table(table_id)
        if not table:
            return jsonify({"error": "Table not found"}), 400


    return call(
        {"message": "Added request to queue"},
        backend.srm_handler.srm.add_request,
        table, 
        subject, 
        summary
    )

@service_blueprint.route("/servicerequests/<id>", methods = ['GET'], endpoint="get_service_request")
@token_required
def get_service_request(current_user, id):
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a Staff Member to perform this request"}), 401
    
    return call(
        None,
        backend.srm_handler.srm.get_request_json,
        int(id)
    )

@service_blueprint.route("/servicerequests/<id>", methods = ['PATCH'], endpoint="update_service_request")
def update_service_request(id):
    """
    JSON FORMAT:
    {
        "subject": "string"
        "summary": "string"
    """
    obj = request.json
        
    subject = obj["subject"] if "subject" in obj else None
    summary = obj["summary"] if "summary" in obj else None

    if subject == None and summary == None:
        return jsonify({"error": "No arguments supplied"}), 400
    
    return call(
        {"message": "Updated request successfully"},
        backend.srm_handler.srm.update_request,
        int(id),
        subject,
        summary
    )

@service_blueprint.route("/servicerequests/<id>", methods = ['DELETE'], endpoint="delete_service_request")
@token_required
def delete_service_request(current_user, id):
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a Staff Member to perform this request"}), 401
    
    return call(
        {"message": "Deleted service request from queue"},
        backend.srm_handler.srm.remove_request,
        int(id)
    )


@service_blueprint.route("/servicerequests/<id>/state", methods = ['POST'], endpoint = "transition_service_request_state")
@token_required
def transition_service_request_state(current_user, id):
    """
        Empty post request to update the state of a service request
    """
    if current_user.__class__ not in [Manager, KitchenStaff, WaitStaff]:
        return jsonify({"error": "Must be a Staff Member to perform this request"}), 401
    
    return call(
        {"message": "Updated state successfully"},
        backend.srm_handler.srm.transition_request_state,
        int(id)
    )

@service_blueprint.route("/servicerequests/<id>/assign", methods = ['POST'], endpoint = "assign_request_to_me")
@token_required
def assign_request_to_me(current_user, id):
    if current_user.__class__ is not WaitStaff:
        return jsonify({"error": "Must be a WaitStaff to perform this request"}), 401
    
    return call(
        {"message": f"Assigned service request to user {current_user.id}"},
        backend.srm_handler.assign_request_to_user,
        int(id),
        current_user.id
    )

@service_blueprint.route("/servicerequests/<id>/unassign", methods = ['POST'], endpoint = "unassign_request_from_me")
@token_required
def unassign_request_from_me(current_user, id):
    if current_user.__class__ is not WaitStaff:
        return jsonify({"error": "Must be a WaitStaff to perform this request"})
    
    return call(
        {"message": f"Unassigned service request from user {current_user.id}"},
        backend.srm_handler.unassign_request_from_user,
        int(id),
        current_user.id
    )

@service_blueprint.route("/servicerequests/me", methods = ['GET'], endpoint = "view_my_requests")
@token_required
def view_my_requests(current_user):
    if current_user.__class__ is not WaitStaff:
        return jsonify({"error": "Must be a WaitStaff to perform this request"})
    
    return call(
        None,
        backend.srm_handler.get_requests_of_user,
        current_user.id
    )