#! /usr/bin/env python
# pylint: disable=C0111


import re
import psycopg2
import config


def get_addr_rep():
    """Pobiera raport z bazy"""
    with psycopg2.connect(config.conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(config.rep_street_sql)
            dbres = cur.fetchall()
    return dbres


def trusted_user(changeset):
    """Sprawdza czy user jest na liście zaufanych"""
    usr = changeset["user"]

    return usr in config.th_usr


def trusted_app(changeset):
    """Sprawdza czy aplikacja jest na liście zaufanych"""
    app = changeset["tag"]["created_by"]
    check = [re.compile(a).match(app) for a in config.th_app]

    return True in check


def trusted(chs):
    """Pobiera dane changesetu i sprawdza listy zaufanych aplikacji i userów"""
    changeset = config.oapi.ChangesetGet(chs)

    return trusted_user(changeset) and trusted_app(changeset)


def create_comment(feat):  # pylint: disable=W0613
    """Tworzy konentarz na podstawie danych z raportu"""
    pass


def post_comment(feat, comment):  # pylint: disable=W0613
    """Wysyła komentarz do OSM"""
    pass
    # config.oapi.ChangesetComment(feat[1], comment)
    # config.oapi.flush()


def rep_nostreet():
    """Główna pętla aplikacji"""
    rep = get_addr_rep()
    # może już tu trzeba odfiltrować zaufanych a dopiero później po nich
    # iterować?
    for feat in rep:
        if not trusted(feat[1]):
            comm = create_comment(feat)  # pylint: disable=E1111
            post_comment(feat, comm)


rep_nostreet()
