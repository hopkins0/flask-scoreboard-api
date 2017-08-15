from flask import render_template, session, redirect, url_for
from . import main
from flask import current_app
from flask import request
from copy import copy, deepcopy
from flask.ext.responses import json_response
import json

import contest


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@main.route('/api/1.0/envios', methods=['GET'])
@crossdomain(origin='*')
def api_10_envios():
    last_run = request.args.get('last_run') or 0

    from app import session
    # session = contest.loadSession()
    active_contest = contest.get_info_active_contest(session)
    score_site = contest.get_runs_all(session, active_contest.contestnumber, last_run)

    response = list()
    for r in score_site:
        response.append({'usernumber':r.RunTable.usernumber,
                 'problemname': r.ProblemTable.problemname,
                 'runproblem': r.RunTable.runproblem,
                 'problemcolor': r.ProblemTable.problemcolor,
                 'problemcolorname': r.ProblemTable.problemcolorname,
                 'problemnumber': r.ProblemTable.problemnumber,
                 'rundatediff': r.RunTable.rundatediff,
                 'rundatediffans': r.RunTable.rundatediffans,
                 'yes': r.AnswerTable.yes,
                 'runanswer': r.RunTable.runanswer,
                 'runstatus': r.RunTable.runstatus,
                 'runnumber': r.RunTable.runnumber})

    return json_response({"data": response}, status_code=200)



@main.route('/api/1.0/equipos', methods=['GET'])
@crossdomain(origin='*')
def api_10_equipos():
    from app import session
    # session = contest.loadSession()
    active_contest = contest.get_info_active_contest(session)
    user_table = contest.get_user_for_contest(session, active_contest.contestnumber)

    response = list()
    for user in user_table:
        response.append({'usernumber':user.usernumber,
                 'username': user.username,
                 'userfullname': user.userfullname})

    return json_response({"data": response}, status_code=200)


@main.route('/api/1.0/problemas', methods=['GET'])
@crossdomain(origin='*')
def api_10_problemas():
    from app import session
    # session = contest.loadSession()
    active_contest = contest.get_info_active_contest(session)
    problems = contest.get_all_problems(session, active_contest.contestnumber)

    response = list()
    for p in problems:
        response.append({'number':p.problemnumber,
                 'shortname': p.problemname,
                 'fullname': p.problemfullname,
                 'basefilename': p.problembasefilename,
                 'color': p.problemcolor,
                 'colorname': p.problemcolorname})

    return json_response({"data": response}, status_code=200)


@main.route('/api/1.0/contest-activo-informacion', methods=['GET'])
@crossdomain(origin='*')
def api_10_contest_activo_info():
    from app import session
    # session = contest.loadSession()
    response = contest.get_info_active_contest(session)
    return json_response({"data": contest.object_as_dict(response)}, status_code=200)


@main.route('/api/1.0/contest-current-time', methods=['GET'])
@crossdomain(origin='*')
def api_10_remaining_time():
    from app import session
    # session = contest.loadSession()
    response = contest.get_site_clock(session)
    return json_response({"data": response}, status_code=200)
 