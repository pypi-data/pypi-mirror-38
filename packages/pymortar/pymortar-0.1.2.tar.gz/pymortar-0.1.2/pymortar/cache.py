"""
sqlite3 - based caching layer and for tracking the sequence of things
"""

import sqlite3
import base64
import pyarrow.plasma as plasma

class cache:
    def __init__(self):
        self.client = plasma.connect("/tmp/plasma", "", 0)
        self.conn = sqlite3.connect("mortar.db")
        self.conn.text_factory = str # handles bytes better
        self.c = self.conn.cursor()

        # create tables
        self.c.execute('''CREATE TABLE IF NOT EXISTS cache (
            module TEXT,
            sitename TEXT,
            objectid TEXT,
            inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS objects (
            object BLOB,
            objectid TEXT,
            inserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        self.conn.commit()

    def hashToOID(self, b64hash):
        return plasma.ObjectID(base64.b64decode(b64hash))

    def OIDtoHash(self, objectid):
        return base64.b64encode(objectid.binary())

    def get(self, module, site='all'):
        # get objectid from sqlite
        res = self.c.execute("SELECT objectid, inserted FROM cache WHERE module=? AND sitename=?", (module, site))
        ans = res.fetchone()
        if not ans:
            return None # no cache
        b64hash = ans[0]
        inserted = ans[1]

        # fetch from plasma if exists
        objectid = self.hashToOID(b64hash)
        if self.client.contains(objectid):
            obj = self.client.get(objectid, timeout_ms=10000000) # 10 sec
            return obj

        # else pull from sqlite disk
        res = self.c.execute("SELECT object FROM objects WHERE objectid=?", (b64hash,))
        buf = res.fetchone()
        pb = self.client.create(objectid, len(buf[0]))
        pd.np.copyto(pd.np.frombuffer(pb, dtype='uint8'), pd.np.frombuffer(buf[0],dtype='uint8'))
        self.client.seal(objectid)
        return self.client.get(objectid, timeout_ms=10000000)

    def put(self, module, pyobject, site='all'):
        objectid = self.client.put(pyobject)
        b64hash = self.OIDtoHash(objectid)

        # get bytes buffer
        buf = self.client.get_buffers([objectid])[0].to_pybytes()

        self.c.execute("INSERT INTO cache(module, sitename, objectid) VALUES (?, ?, ?);", (module, site, b64hash))
        self.c.execute("INSERT INTO objects(objectid, object) VALUES (?, ?);", (b64hash, buf))
        self.conn.commit()
