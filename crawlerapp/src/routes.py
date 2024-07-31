from flask import Blueprint, request, jsonify
from ..util.crawler_util import start_crawl
from ..constants import HTTP_OK_RESPONSE_CODE, HTTP_BAD_REQUEST, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR

main = Blueprint('main', __name__)

@main.route('/v1/crawl', methods=["GET"])
def crawl():
    return handle_request(request)

@main.route('/health', methods=["GET"])
def health_check():
    try:
        return jsonify(status='UP'), HTTP_OK_RESPONSE_CODE
    except Exception:
        return jsonify(status='DOWN'), HTTP_INTERNAL_SERVER_ERROR

def handle_request(request):
    """ Helper function to handle requests """
    if request.method == 'GET':
        url = request.args.get('url', "")
        if len(url) == 0:
            return jsonify(errorMsg="Url missing in request"), HTTP_BAD_REQUEST
        
        return jsonify(status=start_crawl(url)), HTTP_OK_RESPONSE_CODE
    else:
        return jsonify(errorMsg='Resource Unavailable !!'), HTTP_NOT_FOUND