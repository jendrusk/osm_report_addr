#! /usr/bin/env python

import psycopg2
import re
from config import *


def get_addr_rep():
    """Pobiera raport z bazy"""
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(rep_street_sql)
            dbres = cur.fetchall()
    return dbres


def thrusted_user(changeset):
    """Sprawdza czy user jest na liście zaufanych"""
    usr = changeset["user"]
    if usr in th_usr:
        return True
    else:
        return False

def thrusted_app(changeset):
    """Sprawdza czy aplikacja jest na liście zaufanych"""
    app = changeset["tag"]["created_by"]
    check = [re.compile(a).match(app) for a in th_app ]
    if True in check:
        return True
    else:
        return False


def thrusted(chs):
    """Pobiera dane changesetu i sprawdza listy zaufanych aplikacji i userów"""
    changeset = oapi.ChangesetGet(chs)
    if thrusted_user(changeset) and thrusted_app(changeset):
        return True
    else:
        return False

def create_comment(feat):
    """Tworzy konentarz na podstawie danych z raportu"""
    pass


def post_comment(feat, comment):
    """Wysyła komentarz do OSM"""
    oapi.ChangesetComment(feat[1], comment)
    oapi.flush()

def rep_nostreet():
    """Główna pętla aplikacji"""
    rep = get_addr_rep()
    for feat in rep:
        if not thrusted(feat[1]):
            comm = create_comment(feat)
            post_comment(feat, comm)


rep_nostreet()





