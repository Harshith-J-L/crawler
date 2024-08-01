from flask import Blueprint, request, jsonify, Response, render_template
from ..util.crawler_util import start_crawl
from ..constants import HTTP_OK_RESPONSE_CODE, HTTP_BAD_REQUEST, HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """ Render a simple HTML page with a button to download the sitemap and show a message """
    return render_template('index.html')

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
    try:
        if request.method == 'GET':
            url = request.args.get('url', "")
            if len(url) == 0:
                return jsonify(errorMsg="Url missing in request"), HTTP_BAD_REQUEST
            
            status, crawl_response = start_crawl(url)
            if status == "ok":
                response = Response(crawl_response, mimetype='application/xml')

                """ Setting Content-Disposition to attachment prompting browser to download the file """
                response.headers.set('Content-Disposition', 'attachment', filename='sitemap.xml')
                return response
            return jsonify(status=crawl_response), HTTP_INTERNAL_SERVER_ERROR
        else:
            return jsonify(errorMsg='Resource Unavailable !!'), HTTP_NOT_FOUND
    except Exception:
        return jsonify(status='Something Went Wrong'), HTTP_INTERNAL_SERVER_ERROR