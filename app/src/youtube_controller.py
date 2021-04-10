from flask import request
from app.helpers import response
from app import app
from youtube_validation import ScrapValidation
from youtube_service import YoutubeService


@app.route('/youtube/scrap', methods=['POST'])
def get_scrap():
    form = ScrapValidation(request.form)
    if not form.validate():
        errors = []
        for fieldName, errorMessages in form.errors.items():
            errors.append({fieldName: errorMessages})

        return response.error_response(422, 'Failed', errors)

    # Should be dependency injected
    youtube_service = YoutubeService()
    values = youtube_service.get_scrap(form=form)

    return response.success_response(200, 'Success', values)
