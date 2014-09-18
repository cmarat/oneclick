import json
import requests
from time import time
from functools import wraps
from requests import post
from flask import Blueprint, redirect, url_for, session, request, jsonify, current_app, abort
from flask.ext.cors import cross_origin

from linkitup.util.rdf import get_trig
from linkitup.util.provenance import trail_to_prov
from linkitup.util.figshare import get_public_article

# BOOKMARKLET CODE
# location.href = "http://localhost:5000/quicklink/" + location.href.split("/").pop()


quicklink = Blueprint('quicklink', __name__)

# TEST_JSON = json.dumps({"article_id":841753,"authors":[{"first_name":"Marat","full_name":"Marat Charlaganov","id":431618,"last_name":"Charlaganov"},{"first_name":"G. j. a.","full_name":"G. J. A. Sevink","id":566877,"last_name":"Sevink"},{"first_name":"J. g. e. m.","full_name":"J. G. E. M. Fraaije","id":566878,"last_name":"Fraaije"}],"categories":[{"id":109,"name":"Computational Physics"}],"defined_type":"paper","description":"<p>We developed a new hybrid model for efficient modeling of complete vesicles with molecular detail. Combining elements of Brownian dynamics (BD) and dynamic density functional theory (DDFT), we reduce the computational load of an existing coarse grained particle-based dissipative particle dynamics (DPD) model by representing the solvent as a continuum variable or a field, in a consistent manner. Both particle and field representations are spatially unrestricted and there is no need to treat boundaries explicitly. We focus on developing a general framework for deriving the parameters in this hybrid approach from existing DPD representations, and validate this new method via a comparison to DPD results. In addition, we consider a few proof of principle calculations for large systems, including a vesicle of realistic dimensions ($45 nm radius) containing O (104) lipids simulated for O (106) time steps, to illustrate the performance of the new method.</p>","description_nohtml":"We developed a new hybrid model for efficient modeling of complete vesicles with molecular detail. Combining elements of Brownian dynamics (BD) and dynamic density functional theory (DDFT), we reduce the computational load of an existing coarse grained particle-based dissipative particle dynamics (DPD) model by representing the solvent as a continuum variable or a field, in a consistent manner. Both particle and field representations are spatially unrestricted and there is no need to treat boundaries explicitly. We focus on developing a general framework for deriving the parameters in this hybrid approach from existing DPD representations, and validate this new method via a comparison to DPD results. In addition, we consider a few proof of principle calculations for large systems, including a vesicle of realistic dimensions ($45 nm radius) containing O (104) lipids simulated for O (106) time steps, to illustrate the performance of the new method.","files":[{"download_url":"http://files.figshare.com/1268063/hybrid.pdf","id":1268063,"mime_type":"application/pdf","name":"hybrid.pdf","size":"1.25 MB","thumb":"http://previews.figshare.com/1268063/250_1268063.png"}],"links":[{"id":13110,"link":"http://dx.doi.org/10.6084/m3.figshare.1036529"},{"id":13109,"link":"http://dbpedia.org/resource/Calculation"},{"id":12916,"link":"http://dx.doi.org/10.6084/m3.figshare.1032677"},{"id":5708,"link":"http://linkitup.data2semantics.org"},{"id":10267,"link":"http://en.wikipedia.org/wiki/Lipid_bilayer"},{"id":9728,"link":"http://dbpedia.org/resource/Computational_physics"},{"id":9729,"link":"http://dblp.l3s.de/d2r/resource/authors/Marat_Charlaganov"},{"id":12915,"link":"http://dblp.l3s.de/d2r/resource/authors/J._G._E._M._Fraaije"},{"id":9727,"link":"http://orcid.org/0000-0003-1262-856X"},{"id":9151,"link":"http://dx.doi.org/10.1039/C2SM27492B#sthash.zw5JAY0t.dpuf"}],"master_publisher_id":0,"published_date":"12:58, May 21, 2014","status":"Public","tags":[{"id":241462,"name":"RDF=1036529"},{"id":240873,"name":"RDF=1032677"},{"id":48156,"name":"Enriched with LinkItUp"},{"id":192590,"name":"lipid bilayer"},{"id":856,"name":"simulated"}],"title":"Coarse-grained hybrid simulation of liposomes","total_size":"1.25 MB","version":1})

@quicklink.route('/<article_id>')
@cross_origin()
def run_all(article_id=841753):
    results = {}
    article_data = json.dumps(get_public_article(article_id))
    for plugin in ['orcid', 'dbpedia', 'spotlight']:
        plugin_url = request.url_root + plugin
        current_app.logger.debug("About to POST to {}".format(plugin_url))
        try:
            r = requests.post(plugin_url,
                            data=article_data,
                            headers={"content-type":"application/json"},
                            timeout=(2, 30))
            results[plugin] = r.json()['result']
        except:
            pass
    return jsonify(results)

# def nanopub():
#     data = request.get_json()
#     details = data['details']
#     selected = data['selected']
#     provenance_trail = data['provenance']
#     app.logger.debug(provenance_trail)
#     app.logger.debug("Getting trig")
#     graphTrig = get_trig(details, selected, provenance_trail)
#     return graphTrig


# if __name__ == '__main__':
#     from flask import Flask
#     app = Flask(__name__)
#     app.secret_key = 'development'
#     app.debug = True
#     app.register_blueprint(quicklink, url_prefix='/quicklink')
#     app.run()


