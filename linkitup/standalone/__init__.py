import json
import requests
from collections import defaultdict
from flask import Blueprint, redirect, url_for, session, request, jsonify, current_app, abort, render_template, make_response
from flask.ext.cors import cross_origin
#from flask_debugtoolbar import DebugToolbarExtension
# 1175844

standalone = Blueprint('standalone', __name__, template_folder='templates', static_folder='../static')
plugin_base = 'http://marat.ops.few.vu.nl/'

@standalone.route('/')
def run_all():
    # assert app.debug == False
    article_id = request.args.get('article_id', '841753')
    current_app.logger.debug("Quicklink article {}".format(article_id))
    results = all_results(article_id)
    response = make_response(render_template("figshare_inline.html", results=results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def all_results(article_id='841753'):
    article_id = request.args.get('article_id', '841753')
    current_app.logger.debug("Running available plugins on article {}".format(article_id))
    article_data = json.dumps(get_public_article(article_id))
    results = {}
    results['orcid'] = orcid_results(article_data)
    for plugin in ['dbpedia', 'spotlight']:
        plugin_url = plugin_base + plugin
        # plugin_url = request.url_root + plugin
        current_app.logger.debug("About to POST to {}".format(plugin_url))
        # assert current_app.debug == False
        try:
            r = requests.post(plugin_url,
                            data=article_data,
                            headers={"content-type":"application/json"},
                            timeout=(1, 10))
            results[plugin] = r.json()['result']
        except:
            pass
    current_app.logger.debug("Sorted results: {}".format(orcid_results(article_data)))
    # assert current_app.debug == False
    return results

def orcid_results(article_data):
    plugin_url = plugin_base + 'orcid'
    try:
        r = requests.post(plugin_url,
                        data=article_data,
                        headers={"content-type":"application/json"},
                        timeout=(1, 10))
        results = r.json()['result']
    except:
        pass
    prepared_results=defaultdict(list)
    for k, v in results.items():
        prepared_results[v['original_label']].append(v)
    for v in prepared_results.values():
        # FIXME:
        v.sort(key=lambda d: float(d['subscript'][7:]), reverse=True)
    current_app.logger.debug(prepared_results)
    return prepared_results


def get_public_article(article_id):
    response = requests.get(url='http://api.figshare.com/v1/articles/{}'.format(article_id))
    results = response.json()
    if 'error' in results:
        app.logger.error(results)
        raise Exception(results['error'])
    elif results == {} :
        app.logger.error("No article found, retrieved empty response.")
        raise FigshareEmptyResponse("No articles found, retrieved empty response.")
        
    return results['items'][0]


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = 'development'
    app.debug = True
#    toolbar = DebugToolbarExtension(app)
    app.register_blueprint(
        standalone,
        url_prefix='/')
    app.run()
