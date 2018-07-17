#! /usr/bin/env python
# pylint: disable=C0111


import re
import psycopg2
import config
import query


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


def trusted(feat):
    """Pobiera dane changesetu i sprawdza listy zaufanych aplikacji i userów"""
    changeset = config.oapi.ChangesetGet(feat["changeset"])

    return trusted_user(changeset) and trusted_app(changeset)


def create_comment(feat):  # pylint: disable=W0613
    """Tworzy konentarz na podstawie danych z raportu"""
    pass


def get_Object(feat, back):
    """Pobiera obiekt dla rekordu raportu (feat) z możliwością cofnięcia się o x wersji (back)"""
    if feat[3] == "node":
        return config.oapi.NodeGet(feat["osm_id"], feat["version"] - back)
    elif feat[3] == "way":
        return config.oapi.WayGet(feat["osm_id"], feat["version"] - back)
    elif feat[3] == "relation":
        return config.oapi.RelationGet(feat["osm_id"], feat["version"] - back)


def damaged_now(feat):
    """Pobiera z OSM poprzednią wersję obiektu i sprawdza czy uszkodzenie powstało w wyniku tego changesetu"""
    if feat[4] > 1:
        obj_now = get_Object(feat,0)
        obj_before = get_Object(feat,1)
        return addr_edited(obj_now, obj_before) and addr_Valid(obj_before)
    else:
        return True


def addr_edited(obj_now, obj_before):
    """Sprawdza czy dane adresowe były edytowane w ramach tego changesetu"""
    return (
        obj_now["tag"]["addr:city"] != obj_before["tag"]["addr:city"] and
        obj_now["tag"]["addr:place"] != obj_before["tag"]["addr:place"] and
        obj_now["tag"]["addr:street"] != obj_before["tag"]["addr:street"] and
        obj_now["tag"]["addr:housenumber"] != obj_before["tag"]["addr:housenumber"])

def addr_Valid(obj):
    """Sprawdza czy dane adresowe są poprawne"""
    return (
        (
            obj["tag"]["addr:city"] is not None and
            obj["tag"]["addr:place"] is None and
            obj["tag"]["addr:street"] is not None and
            obj["tag"]["addr:housenumber"] is not None
        ) or (
            obj["tag"]["addr:city"] is None and
            obj["tag"]["addr:place"] is not None and
            obj["tag"]["addr:street"] is None and
            obj["tag"]["addr:housenumber"] is not None
        )
    )



def post_comment(feat, comment):  # pylint: disable=W0613
    """Wysyła komentarz do OSM"""
    pass
    # config.oapi.ChangesetComment(feat[1], comment)
    # config.oapi.flush()


def rep_nostreet():
    """Główna pętla aplikacji"""
    rep = get_addr_rep()
    for feat in rep:
        if not trusted(feat) and damaged_now(feat):
            comm = create_comment(feat)  # pylint: disable=E1111
            post_comment(feat, comm)

### START ###
rep_nostreet()
