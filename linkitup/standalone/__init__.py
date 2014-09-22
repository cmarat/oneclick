import json
import requests
from collections import defaultdict
from flask import request, current_app, render_template, make_response
from flask import Blueprint

# Example article_id 1175844

standalone = Blueprint(
    'standalone',
    __name__,
    template_folder='templates')
plugin_base = 'http://marat.ops.few.vu.nl/'


@standalone.route('/')
def bookmarklet_links():
    # assert app.debug == False
    article_id = request.args.get('article_id', '841753')
    current_app.logger.debug("Quicklink article {}".format(article_id))
    results = find_all_links(article_id)
    response = make_response(
        render_template("figshare_inline.html", results=results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def find_all_links(article_id):
    article_data = json.dumps(get_public_article(article_id))
    results = {}
    results['orcid'] = process_orcid(post_to_plugin('orcid', article_data))
    for plugin in ['dbpedia', 'spotlight']:
        results[plugin] = post_to_plugin(plugin, article_data)
    return results


def process_orcid(orcid_results):
    prepared_results = defaultdict(list)
    for k, v in orcid_results.items():
        prepared_results[v['original_label']].append(v)
    for v in prepared_results.values():
        # FIXME:
        v.sort(key=lambda d: float(d['subscript'][7:]), reverse=True)
    return prepared_results


def post_to_plugin(plugin, article_data):
    plugin_url = plugin_base + plugin
    try:
        r = requests.post(
            plugin_url,
            data=article_data,
            headers={"content-type": "application/json"},
            timeout=(1, 10))
        results = r.json()['result']
    except:
        results = {}
    return results


def get_public_article(article_id):
    response = requests.get(
        url='http://api.figshare.com/v1/articles/{}'.format(article_id))
    results = response.json()
    if 'error' in results:
        app.logger.error(results)
        raise Exception(results['error'])
    elif results == {}:
        app.logger.error("No article found, retrieved empty response.")
        raise Exception("No articles found, retrieved empty response.")
    return results['items'][0]


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = 'development'
    app.debug = True
    app.register_blueprint(
        standalone,
        url_prefix='/')
    app.run()
