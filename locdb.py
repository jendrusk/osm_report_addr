import sqlite3


# tabele do inicjalizacji
tables = [
    {"name": "broken_objects",
     "create": """create table broken_objects (
            osm_user text, 
            osm_changeset bigint,
            created timestamp,
            osm_id bigint, 
            reason text, 
            type text, 
            version int, 
            lat real, 
            lon real,
            trusted_user boolean,
            trusted_app boolean,
            app text,
            damaged_now boolean)"""},
    {"name": "changeset_visits",
     "create": """create table changeset_visits (
            changeset bigint, referer text)"""}
]



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_conn():
    db = sqlite3.connect("locdb")
    db.row_factory = dict_factory
    return db

def insert(rep_val):
    db = get_conn()
    cur = db.cursor()
    sql = """
    insert into broken_objects (osm_user, osm_changeset, created, osm_id, reason, type, version, lat, lon, 
      trusted_user, trusted_app, app, damaged_now)
    values(:user, :changeset, :created, :osm_id, :reason, :type, :version, :lat, :lon, 
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
        sql = """select *, 
            (select count(*) from changeset_visits v where v.changeset = o.osm_changeset) as visits  
            from broken_objects o"""
        cur.execute(sql)
    else:
        sql = """select *, 
            (select count(*) from changeset_visits v where v.changeset = o.osm_changeset) as visits  
            from broken_objects o 
            limit :limit"""
        cur.execute(sql,{"limit": limit})
    res = cur.fetchall()
    db.close()
    return res

def select_changeset(changeset):
    db = get_conn()
    cur = db.cursor()
    sql = "select * from broken_objects where osm_changeset = :changeset"
    cur.execute(sql, {"changeset": changeset})
    res = cur.fetchall()
    db.close()
    return res

def add_visit(chgs_id, referer):
    params = {"chgs_id": chgs_id, "referer": referer}
    sql = "insert into changeset_visits (changeset, referer) values (:chgs_id, :referer)"
    db = get_conn()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    db.close()

def select_visits_grouped(chgs_id):
    params = {"chgs_id": chgs_id}
    sql = "select referer, count(*) as count from changeset_visits where changeset = :chgs_id group by referer"
    db = get_conn()
    cur = db.cursor()
    cur.execute(sql, params)
    res = cur.fetchall()
    db.close()
    return res

def db_init():
    for table in tables:
        if not table_exists(table):
            table_create(table)


def table_create(table):
    db = get_conn()
    cur = db.cursor()
    cur.execute(table["create"])
    db.commit()
    db.close()


def table_exists(table):
    db = get_conn()
    cur = db.cursor()
    cur.execute("select 1 from sqlite_master where type='table' and name=:name", table)
    res = cur.fetchall()
    db.close()
    return len(res) > 0


db_init()
