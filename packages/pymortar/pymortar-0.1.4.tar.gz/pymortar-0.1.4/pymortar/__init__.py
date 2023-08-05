name = "pymortar"

import logging
import importlib
import traceback
import os
import time
import pickle
import IPython
import grpc
import base64
import uuid
#import result
import pytz
import json
import pandas as pd
from pymortar import hod_pb2
from pymortar import mdal_pb2
from pymortar import mortar_pb2
from pymortar import mortar_pb2_grpc

from pymortar import cache

logging.basicConfig(level=logging.DEBUG)

agg_funcs = {
    "RAW": mdal_pb2.RAW,
    "MEAN": mdal_pb2.MEAN,
    "MIN": mdal_pb2.MIN,
    "MAX": mdal_pb2.MAX,
    "COUNT": mdal_pb2.COUNT,
    "SUM": mdal_pb2.SUM,
}
def parse_agg_func(name):
    return mdal_pb2.AggFunc.Value(name.upper())


class MortarClient:
    def __init__(self, caddr=None, with_cache=True):
        if caddr is None:
            caddr = os.environ.get('MORTAR_API_ADDRESS','localhost:9001')
        self.with_cache = with_cache
        #self.client = plasma.connect("/tmp/plasma", "", 0)
        self.cache = cache.cache()
        self.channel = grpc.insecure_channel(caddr, options=[
                  ('grpc.max_send_message_length', 100 * 1024 * 1024),
                  ('grpc.max_receive_message_length', 100 * 1024 * 1024)
        ])
        self.stub = mortar_pb2_grpc.MortarStub(self.channel)

    def clear_cache(self, modulename):
        self.cache.delete_module_prefix(modulename)


    def qualify(self, required):
        q = [hod_pb2.QueryRequest(query=req) for req in required]
        sites = self.stub.Qualify(mortar_pb2.QualifyRequest(requiredqueries=q))

        #objectid = self.cache.put(list(sites.sites))
        #b64hash = base64.b64encode(objectid.binary())

        return list(sites.sites)

    def fetch(self, sitename, request):
        aggs = {}
        for varname, aggfunclist in request["Aggregation"].items():
            aggs[varname] = mdal_pb2.Aggregation(funcs=[parse_agg_func(func) for func in aggfunclist])
        #print aggs
        vardefs = {}
        for varname, defn in request["Variables"].items():
            vardefs[varname] = mdal_pb2.Variable(
                name = varname,
                definition = defn["Definition"] % sitename,
                units = defn.get("Units",None),
            )
        #print vardefs
        params = mdal_pb2.DataQueryRequest(
            composition = request["Composition"],
            aggregation = aggs,
            variables = vardefs,
            time = mdal_pb2.TimeParams(
                start = request["Time"]["Start"],
                end = request["Time"]["End"],
                window = request["Time"]["Window"],
                aligned = request["Time"]["Aligned"],
            ),
        )
        #print params
        tz = pytz.timezone("US/Pacific")
        resp = self.stub.Fetch(mortar_pb2.FetchRequest(request=params), timeout=120)
        if resp.error != "":
            raise Exception(resp.error)

        #IPython.embed()
        values = [x.value for x in resp.response.values]
        if pd.np.array(values).size > 0:
            t = resp.response.times
            v = pd.np.array(values)
            #if len(resp.response.times) > pd.np.array(values).shape[1]:
            df = pd.DataFrame.from_records(values).T
            df.columns = resp.response.uuids
            df.index = pd.to_datetime(resp.response.times)

            mapping = {}
            for k, v in resp.response.mapping.items():
                mapping[k] = [str(uuid.UUID(bytes=x)) for x in v.uuids]

            result = {
                'df': df,
                'sitename': sitename,
                'context': {x.uuid: dict(x.row) for x in resp.response.context},
                'mapping': mapping,
            }

            return result
        return None

    def RUN(self, qualify, fetch, clean=None, execute=None, aggregate=None):
        if qualify is None or not isinstance(qualify, str):
            raise Exception("QUALIFY must be string path of module")
        qualifyrun = importlib.import_module(qualify)
        logging.info("Imported qualify module {0}".format(qualify))

        if fetch is None or not isinstance(fetch, str):
            raise Exception("FETCH must be string path of module")
        fetchrun = importlib.import_module(fetch)
        logging.info("Imported fetch module {0}".format(fetch))

        if clean is not None:
            cleanrun = importlib.import_module(clean)
            logging.info("Imported clean module {0}".format(clean))
        else:
            logging.info("No clean module")
            cleanrun = None

        if execute is not None:
            executerun = importlib.import_module(execute)
            logging.info("Imported execute module {0}".format(execute))
        else:
            logging.info("No execute module")
            executerun = None

        if aggregate is not None:
            aggregaterun = importlib.import_module(aggregate)
            logging.info("Imported aggregate module {0}".format(aggregate))
        else:
            logging.info("No aggregate module")
            aggregaterun = None

        # qualify to get execution set
        fromcache = self.cache.get(qualify)
        if fromcache:
            logging.info("Pulling execution set from cache")
            sites = fromcache
        else:
            logging.info("Running qualify")
            sites = qualifyrun.run(self)
            self.cache.put(qualify, sites)

        # run fetch on each site in execution set
        res = []
        logging.info("Running on {0} sites".format(len(sites)))
        for site in sites:
            try:
                # get from cache: keyed by site+fetch
                fromcache = self.cache.get(fetch, site)
                if fromcache:
                    siteres = fromcache
                else:
                    siteres = fetchrun.run(self, site)
                    if siteres is None: continue
                    self.cache.put(fetch, siteres, site)

                if cleanrun:
                    siteres = cleanrun.run(self, siteres)
                    if siteres is None: continue
                if executerun:
                    siteres = executerun.run(self, siteres)
                    if siteres is None: continue
                if aggregaterun:
                    res.append(siteres)
                else:
                    yield siteres
            except Exception as e:
                traceback.print_exc()

        if aggregaterun:
            aggregaterun.run(res)
