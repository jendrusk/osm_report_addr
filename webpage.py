from flask import Flask, render_template, request
import locdb
import config
app = Flask(__name__)

def create_josm_list(rep):
    res_lst = list()
    for feat in rep:
        if feat["type"] == "node":
            obj = "n"+str(feat["osm_id"])
        elif feat["type"] == "way":
            obj = "w"+str(feat["osm_id"])
        elif feat["type"] == "relation":
            obj = "r"+str(feat["osm_id"])
        res_lst.append(obj)
    return ",".join(res_lst)



@app.route('/')
def main_list():
    htdata = locdb.select_all(limit=100)
    header = "Ostatnie 100 changesetów z uszkodzonymi adresami"
    colnames = ["osm_id", "osm_user", "osm_changeset", "visits", "reason", "checks"]
    rows = htdata

    return render_template("main.html",
                           header = header,
                           colnames = colnames,
                           rows =rows,
                           reason_dict=config.reason_dict)


@app.route('/changeset/<chgs_id>')
def changeset_report(chgs_id):
    referer = request.headers.get("Referer")
    locdb.add_visit(chgs_id,referer)
    visits = locdb.select_visits_grouped(chgs_id)
    htdata = locdb.select_changeset(chgs_id)
    colnames = ["osm_id", "reason", "checks"]
    all_obj = create_josm_list(htdata)
    return render_template("changeset.html",
                           rows=htdata,
                           colnames=colnames,
                           reason_dict=config.reason_dict,
                           all_obj=all_obj,
                           visits=visits)




if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
