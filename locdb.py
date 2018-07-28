import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
def get_cursor():
    db = sqlite3.connect("locdb")
    db.row_factory = dict_factory
    return db.cursor()

cur = get_cursor()
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
        trusted boolean,
        damaged_now boolean)""")
    db.commit()


def insert(rep_val):
    cur = db.cursor()
    sql = """
    insert into broken_objects (osm_user, osm_changeset, osm_id, reason, type, version, lat, lon, trusted, damaged_now)
    values(:user, :changeset, :osm_id, :reason, :type, :version, :lat, :lon, :trusted, :damaged_now)
    """
    for feat in rep_val:
        cur.execute(sql,feat)
    db.commit()

def select_all(limit=0):
    cur = get_cursor()
    if limit == 0:
        sql = "select * from broken_objects"
        cur.execute(sql)
    else:
        sql = "select * from broken_objects limit :limit"
        cur.execute(sql,{"limit": limit})
    return cur.fetchall()
