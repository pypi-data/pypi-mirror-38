# -*- coding: utf-8 -*-

"""Generate simple Golang HTTP handlers for all gRPC methods defined in the .proto file.

Usage:
    $ python -m grpc_pytools.gohttp -h

Example:
    $ python -m grpc_pytools.gohttp --proto-ast-file=/path/to/xx_ast.json --http-server=localhost:50051
"""

import argparse
import sys

from . import helpers


HEADER = '''package http

import (
	"encoding/json"
	nethttp "net/http"
)

type Handler func(w http.ResponseWriter, r *http.Request)

func HandleJSON(handler Handler) {
	h := func(w http.ResponseWriter, r *http.Request) {
		decoder := json.NewDecoder(req.Body)
		result = handler(w, r)
		w.Header().Set("Content-Type", "application/octet-stream")
		return result
	}
	return h
}

'''


HANDLER = '''func (s *Server) {method_name}(w http.ResponseWriter, r *http.Request) {
}
'''
RESOURCE = '''@api.route(uri='/{underscored_service_name}/{underscored_method_name}', methods=['POST'])
class {method_name}(GRPCResource):
    name = '{underscored_service_name}.{underscored_method_name}'
    req_schema = schemas.{req_name}Schema()
    resp_schema = schemas.{resp_name}Schema()

    def create(self, request):
        return {underscored_service_name}.{underscored_method_name}(request.data)
'''


class Generator(object):

    writer = sys.stdout

    def __init__(self, proto_ast_file, pb2_module_name, http_server):
        self.proto_ast, self.ast_maps = helpers.load_proto_ast(proto_ast_file)
        self.pb2_path, self.pb2_name = helpers.split_module_name(
            pb2_module_name)
        self.http_server = http_server

    def write_module_header(self, services):
        service_definitions = '\n'.join([
            "{service_name} = services.{service_class_name}('{target}')".format(
                service_name=helpers.underscore(service['name']),
                service_class_name=service['name'],
                target=self.http_server
            )
            for service in services
        ])
        self.writer.write(HEADER.format(
            service_definitions=service_definitions
        ))

    def write_rpc_resources(self, service):
        for method in service['methods']:
            req_name = helpers.get_camel_case_full_name(
                self.ast_maps['messages'][method['input_type']]
            )
            resp_name = helpers.get_camel_case_full_name(
                self.ast_maps['messages'][method['output_type']]
            )
            self.writer.write('\n\n' + RESOURCE.format(
                underscored_service_name=helpers.underscore(service['name']),
                underscored_method_name=helpers.underscore(method['name']),
                method_name=method['name'],
                req_name=req_name,
                resp_name=resp_name
            ))

    def generate(self):
        services = self.proto_ast['services']
        self.write_module_header(services)
        for service in services:
            self.write_rpc_resources(service)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proto-ast-file', required=True,
                        help='The path of the AST-like JSON file.')
    parser.add_argument('--pb2-module-name', required=True,
                        help='The name of the generated `xx_pb2.py` '
                             'module with the full Python path.')
    parser.add_argument('--http-server', required=True,
                        help='The host and port of gRPC server (in '
                             'the form of "host:port").')
    args = parser.parse_args()
    generator = Generator(args.proto_ast_file,
                          args.pb2_module_name,
                          args.http_server)
    generator.generate()


if __name__ == '__main__':
    main()
