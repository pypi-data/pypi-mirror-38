import json
import os
import python_jsonschema_objects as pjs
import websocket


class OCPPConnection():
        def __init__(self, url):
            self.url = url
            self.ws = websocket.create_connection(url)

            self.schemas_dict = {}

            schemas_dir = os.path.join(os.path.dirname(__file__),
                                       'OCPP-2.0_part3_schemas/')
            schemas = os.listdir(schemas_dir)

            for schema in schemas:
                    self.schemas_dict[schema] = json.load(
                            open(os.path.join(schemas_dir, schema),
                                 encoding='utf-8-sig'))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.ws.close()

        def request(self, message, payload):
            """ Send a request message.

            :param message: 
            :param payload: 
            :returns: 
            :rtype: 

            """
            builder = pjs.ObjectBuilder(self.schemas_dict[message +
                                                          'Request_v1p0.json'],
                                        resolved=self.schemas_dict)
            ns = builder.build_classes(standardize_names=False)

            method_name = 'urn_ocpp_cp_2_2018_4_' + message.lower() + 'request'

            method = getattr(ns, method_name)

            t = method().from_json(payload)

            self.ws.send(t.serialize())
            response = self.ws.recv()
            return {'url': self.url, 'data': response}
