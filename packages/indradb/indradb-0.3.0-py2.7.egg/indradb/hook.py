import os
import sys

import capnp
capnp.remove_import_hook()

def get_schema():
    module_path = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(module_path, "indradb.capnp")
    print("XXX", __file__, os.path.abspath(__file__), module_path, schema_path)
    return capnp, capnp.load(schema_path)
