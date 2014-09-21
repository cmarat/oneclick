import json
import requests
from flask import Blueprint, redirect, url_for, session, request, jsonify, current_app, abort, render_template
from flask.ext.cors import cross_origin
from flask_debugtoolbar import DebugToolbarExtension

standalone = Blueprint('standalone', __name__, template_folder='templates', static_folder='../static')

@standalone.route('/')
@cross_origin()
def run_all():
    # assert app.debug == False
    article_id = request.args.get('article_id', '841753')
    current_app.logger.debug("Quicklink article {}".format(article_id))
    results = all_results(article_id)
    return render_template("figshare_inline.html", results=results)

def all_results(article_id='841753'):
    article_id = request.args.get('article_id', '841753')
    current_app.logger.debug("Running available plugins on article {}".format(article_id))
    results = {}
    article_data = json.dumps(get_public_article(article_id))
    for plugin in ['orcid']:
        plugin_url = 'http://marat.ops.few.vu.nl/' + plugin
        # plugin_url = request.url_root + plugin
        current_app.logger.debug("About to POST to {}".format(plugin_url))
        try:
            r = requests.post(plugin_url,
                            data=article_data,
                            headers={"content-type":"application/json"},
                            timeout=(1, 10))
            results[plugin] = r.json()['result']
        except:
            pass
    return results

def orcid_results(article_data):
    plugin_url = 'http://marat.ops.few.vu.nl/orcid'
    try:
        r = requests.post(plugin_url,
                        data=article_data,
                        headers={"content-type":"application/json"},
                        timeout=(1, 10))
        results = r.json()['result']
    except:
        pass
    for result in results:
        result['original_label']

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
    toolbar = DebugToolbarExtension(app)
    app.register_blueprint(
        standalone,
        url_prefix='/')
    app.run()
