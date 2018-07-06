#! /usr/bin/env python

import psycopg2
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import *


def get_nostreet_rep():
    query = "select * from rep_addr_nostreet()"
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            dbres = cur.fetchall()
    return dbres

def get_rep_addr_street_n_place():
    query = "select * from rep_addr_street_n_place()"
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            dbres = cur.fetchall()
    return dbres

def post_comment(rep, comment):
    chgs = set([x[1] for x in rep])
    for ch in chgs:
        if unthrusted(ch):
            oapi.ChangesetComment(ch, comment)
    oapi.flush()


def post_notes(rep, note):
    notes_ids = []
    for row in rep:
        note_data = {"lat": row[3], "lon": row[4], "text": note}
        note_resp = oapi.NoteCreate(note_data)
        notes_ids.append(note_resp['id'])
        oapi.flush()
    return notes_ids

def create_users_html(users):
    resp = []
    for user in users:
        resp.append(R'<a href="http://osm.org/user/{user}">  {user}</a>'.format(user=user))
    return "<br />\n".join(resp)

def create_notes_html(notes):
    resp = []
    for note in notes:
        resp.append(R'<a href="http://osm.org/note/{note}">  {note}</a>'.format(note=note))
    return "<br />\n".join(resp)

def create_changesets_html(chns):
    resp = []
    for chn in chns:
        resp.append(R'<a href="http://osm.org/changeset/{chn}">  {chn}</a>'.format(chn=chn))
    return "<br />\n".join(resp)


def unthrusted(changeset):
    """Funkcja sprawdzająca czy changeset pochodzi z edytora (true) czy innej aplikacji (false), np streetComplete"""
    #trzeba dopisać - w kodzie już wpięte
    return True

def create_mail_content(rep,notes):
    items_count = len(rep)
    changesets = set([x[1] for x in rep])
    changesets_count = len(changesets)
    users = set([x[0] for x in rep])

    resp = ""
    resp += "Raport niepełnych adresów <br /><br />\n"
    resp += "W dniu wczorajszym utworzono {items_count} niepełnych adresów " \
            "w ramach {changesets_count} zestawów zmian <br /><br />\n".format(items_count=items_count,changesets_count=changesets_count)
    resp+= "Użytkownicy:<br /> \n"
    resp += create_users_html(users) + "<br /> \n"
    # resp += "Utworzone notatki:<br /> \n"
    # resp += create_notes_html(notes) + "<br /> \n"
    resp += "Zakomentowane zestawy zmian:<br /> \n"
    resp += create_changesets_html(changesets) + "<br /> \n"
    resp += "<br /><br />\n"
    resp += "Pozdrawiam i cierpliwości życzę :)"

    a=1
    return resp

def send_mail(mail_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = mail_from
    text = "Ta wiadomość nie posiada alternatywnej wersji tekstowej"
    html = mail_content

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('localhost')


    for mail_rec in mail_to:
        msg['To'] = mail_rec
        s.sendmail(mail_from, mail_to, msg.as_string())
    s.quit()

def rep_nostreet():
    rep = get_nostreet_rep()
    rep += get_rep_addr_street_n_place()
    # notes = post_notes(rep, nostreet_note_txt)
    post_comment(rep, nostreet_chngeset_comment)
    mail_content = create_mail_content(rep=rep, notes=[])
    send_mail(mail_content=mail_content)


# rep_nostreet()

post_comment(rep_test,nostreet_chngeset_comment)




