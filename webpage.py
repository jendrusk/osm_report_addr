from flask import Flask, render_template
import locdb
import config
app = Flask(__name__)

@app.route('/')
def hello_world():
    htdata = locdb.select_all(limit=100)
    header = "Ostatnie 100 changesetów z uszkodzonymi adresami"
    colnames = ["osm_id", "osm_user", "osm_changeset", "reason", "checks"]
    rows = htdata

    return render_template("main.html",
                           header = header,
                           colnames = colnames,
                           rows =rows,
                           reason_dict=config.reason_dict)






if __name__ == "__main__":
    app.run()
