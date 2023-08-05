import json
import traceback

import decorator
from flask import current_app, Response


def jsonapify(data=None, errors=None):
    if not data and not errors:
        raise RuntimeError("Either data or errors MUST be provided.")
    if data and errors:
        raise RuntimeError("You cannot specify both data and errors.")

    if data:
        content = {'data': data}
        status = 200
    else:
        content = {'errors': errors}
        status = 500

    return Response(
        json.dumps(content),
        status=status,
        mimetype='application/vnd.api+json'
    )


@decorator.decorator
def jsonapify_wrap(f, *args, **kwargs):
    try:
        return jsonapify(data=f(*args, **kwargs))
    except Exception as e:
        return jsonapify(errors=[
            {'title': str(e), 'detail': traceback.format_exc()}
            if current_app.config['DEBUG'] else
            {'title': 'Something went wrong!'}
        ])
