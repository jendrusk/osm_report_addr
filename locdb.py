import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




def get_conn():
    db = sqlite3.connect("locdb")
    db.row_factory = dict_factory
    return db

db = get_conn()
cur = db.cursor()
cur.execute("select 1 from sqlite_master where type='table' and name='broken_objects'")
res = cur.fetchall()

if len(res) == 0:
    cur.execute("""create table broken_objects (
        osm_user text, 
        osm_changeset bigint, 
        osm_id bigint, 
        reason text, 
        type text, 
        version int, 
        lat real, 
        lon real,
        trusted_user boolean,
        trusted_app boolean,
        app text,
        damaged_now boolean)""")
    db.commit()
db.close()


def insert(rep_val):
    db = get_conn()
    cur = db.cursor()
    sql = """
    insert into broken_objects (osm_user, osm_changeset, osm_id, reason, type, version, lat, lon, 
      trusted_user, trusted_app, app, damaged_now)
    values(:user, :changeset, :osm_id, :reason, :type, :version, :lat, :lon, 
      :trusted_user, :trusted_app, :app, :damaged_now)
    """
    for feat in rep_val:
        cur.execute(sql,feat)
    db.commit()
    db.close()

def select_all(limit=0):
    db = get_conn()
    cur = db.cursor()
    if limit == 0:
        sql = "select * from broken_objects"
        cur.execute(sql)
    else:
        sql = "select * from broken_objects limit :limit"
        cur.execute(sql,{"limit": limit})
    res = cur.fetchall()
    db.close()
    return res

def select_changeset(changeset):
    db = get_conn()
    cur = db.cursor()
    sql = "select * from broken_objects where changeset = :changeset"
    cur.execute(sql, {"changeset": changeset})
    res = cur.fetchall()
    db.close()
    return res
