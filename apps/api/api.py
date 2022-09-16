from apps.api import bp
from flask import jsonify, request, current_app
from apps import api_response

from apps.glassdoor_scraper.main import glassdoor_scraper


@bp.route("/get_job", methods=["POST"])
def get_job():
    data = request.get_json()
    url = data.get("url", False)
    target_num = data.get("target_num", False)

    if url and target_num :
        gd = glassdoor_scraper()    
        result = gd.scrape(             
            url,
            target_num
            )
        return api_response("success","Success get data job", result)
    else :
        return api_response("error","Error get data job", [])