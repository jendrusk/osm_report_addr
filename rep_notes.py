#! /usr/bin/env python
# pylint: disable=C0111


import re
import psycopg2
import config
import query
import locdb


def get_addr_rep(): # TODO:Zastanawiam się czy nie oprzeć tego o OverpassAPI
    """Pobiera raport z bazy"""
    with psycopg2.connect(config.conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(query.rep_street_sql)
            records = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
    res = list()
    for rec in records:
        rd = dict()
        for val, col in zip(rec, colnames):
            rd[col] = val
        res.append(rd)
    return res


def trusted_user(changeset):
    """Sprawdza czy user jest na liście zaufanych"""
    usr = changeset["user"]

    return usr in config.th_usr


def trusted_app(changeset):
    """Sprawdza czy aplikacja jest na liście zaufanych"""
    app = changeset["tag"]["created_by"]
    check = [re.compile(a).match(app) for a in config.th_app]

    return True in check


def fill_trusted(feat):
    """Pobiera dane changesetu i sprawdza listy zaufanych aplikacji i userów"""
    changeset = config.oapi.ChangesetGet(feat["changeset"])
    feat["trusted_user"] = trusted_user(changeset)
    feat["trusted_app"] = trusted_app(changeset)
    feat["app"] = changeset["tag"]["created_by"]

    return feat


def group_by_changeset(rep):
    """Grupuje liste błędów po changesecie"""
    res = []
    broken = [x for x in rep if not x["trusted"] and x["damaged_now"] ]
    chgs_set = set([x["changeset"] for x in broken])
    for chgs in chgs_set:
        res_chgs = dict()
        chgs_data = [x for x in broken if x["changeset"] == chgs]
        res_chgs["changeset"] = chgs_data[0]["changeset"]
        res_chgs["user"] = chgs_data[0]["user"]
        res_chgs["reasons"] = list()
        reas_set = set([x["reason"] for x in chgs_data])
        for reas in reas_set:
            res_reas_d = dict()
            res_reas_d["reason"] = reas
            res_reas_d["items"] = list()
            items_list = [x for x in chgs_data if x["reason"] == reas]
            for item in items_list:
                item_dict = {
                    "osm_id" : item["osm_id"],
                    "type" : item["type"]
                }
                res_reas_d["items"].append(item_dict)
            res_chgs["reasons"].append(res_reas_d)
        res.append(res_chgs)
    return res


def create_comments(rep):  # pylint: disable=W0613
    """Grupuje listę błędów po changesecie i dodaje komentarze na podstawie danych z raportu"""
    rep_group = group_by_changeset(rep)
    a=1
    #TODO:Dokończyć


def get_Object(feat, ver):
    """Pobiera obiekt dla rekordu raportu (feat) z możliwością cofnięcia się o x wersji (back)"""
    if feat["type"] == "node":
        return config.oapi.NodeGet(feat["osm_id"], ver)
    elif feat["type"] == "way":
        return config.oapi.WayGet(feat["osm_id"], ver)
    elif feat["type"] == "relation":
        return config.oapi.RelationGet(feat["osm_id"], ver)


def damaged_now(feat):
    """Pobiera z OSM poprzednią wersję obiektu i sprawdza czy uszkodzenie powstało w wyniku tego changesetu"""
    if int(feat["version"]) > 1:
        obj_now = get_Object(feat, int(feat["version"]))
        obj_before = get_Object(feat,int(feat["version"])-1)
        return addr_edited(obj_now, obj_before) and addr_Valid(obj_before)
    else:
        return True


def addr_edited(obj_now, obj_before):
    """Sprawdza czy dane adresowe były edytowane w ramach tego changesetu"""

    now_tag_ = obj_now.get("tag")
    before_tag_ = obj_before.get("tag")
    return (
        now_tag_.get("addr:city") != before_tag_.get("addr:city") and
        now_tag_.get("addr:place") != before_tag_.get("addr:place") and
        now_tag_.get("addr:street") != before_tag_.get("addr:street") and
        now_tag_.get("addr:housenumber") != before_tag_.get("addr:housenumber"))

def addr_Valid(obj):
    """Sprawdza czy dane adresowe są poprawne"""
    obj_tag_ = obj.get("tag")
    return (
        (
            obj_tag_.get("addr:city") is not None and
            obj_tag_.get("addr:place") is None and
            obj_tag_.get("addr:street") is not None and
            obj_tag_.get("addr:housenumber") is not None
        ) or (
            obj_tag_.get("addr:city") is None and
            obj_tag_.get("addr:place") is not None and
            obj_tag_.get("addr:street") is None and
            obj_tag_.get("addr:housenumber") is not None
        )
    )


def post_comment(feat, comment):  # pylint: disable=W0613
    """Wysyła komentarz do OSM"""
    pass
    # config.oapi.ChangesetComment(feat[1], comment)
    # config.oapi.flush()

def validate_report(rep):
    res = []
    for feat in rep:
        feat = fill_trusted(feat)
        feat["damaged_now"] = damaged_now(feat)
        res.append(feat)
    return res

def rep_nostreet():
    """Główna pętla aplikacji"""
    # workflow:
    # 1. pobrać raport z bazy
    # 2. sprawdzić czy user lub aplikacja nie jest zaufana oraz czy błąd powstał w tym changesecie
    # 3. sprawdzone dodać do bazy
    rep = get_addr_rep()
    rep_val = validate_report(rep)
    locdb.insert(rep_val)


### START ###
rep_nostreet()
