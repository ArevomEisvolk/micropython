import ujson
import ure
import usocket
from urllib.parse import parse_qs, urlparse
import gc

gc.enable()

class Request:
    def __init__(self, method = "", headers = {}, path = "", query_params = (), body = None):
        self.method = method
        self.headers = headers
        self.path = path
        self.query_params = query_params
        self.body = body

class Response:
    def __init__(self, body, status_code = 200, content_type = "text/html"):
        self.body = body
        self.status_code = status_code
        self.content_type = content_type


def garbage_collector(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        gc.collect()
        return f(*args, **kwargs)
    return new_func


class MostMinimalWebFramework:

    route_table = []

    def __init__(self, static_folder="") -> None:
        self.static_folder = static_folder

    @garbage_collector
    def route(self, path: str):
        def decorator(func):
            def __inner():
                return func()

            self.route_table.append((ure.compile(path + "$"), func))
            return __inner

        return decorator

    @garbage_collector
    def get_route_function(self, searched_path: str):
        return next(r for r in self.route_table if r[0].match(searched_path))[1]

    @garbage_collector 
    def request_parser(self, request_str: str) -> Request:
        request_lines = request_str.split("\r\n")
        method, url, _ = request_lines[0].split(" ")  # first line has method and url
        headers = {}
        for i, line in enumerate(request_lines[1:], 1):
            if line == "":  # under empty line, whole data is body
                try:
                    body = ujson.loads("".join(request_lines[i + 1 :]))
                except:
                    body = "".join(request_lines[i + 1 :])
                break

            j = line.find(":")  # left part of : will key, right part will be value
            headers[line[:j].upper()] = line[j + 2 :]

        url = urlparse(url)
        
        return Request(method, headers, url.path, parse_qs(url.query), body)
    
    @garbage_collector 
    def build_response(self, r: Response) -> str:
        html = (
            f"""HTTP/1.1 {r.status_code}\r\nContent-Type: {r.content_type}; charset=utf-8
            \r\nContent-Length: {len(r.body)}\r\nConnection: close\r\n\r\n"""
        )
        return html + r.body if isinstance(r.body, str) else ujson.dumps(r.body)

    @garbage_collector 
    def send_static_file(self, filepath : str):
        with open(self.static_folder + filepath, "r") as static_file:
            return Response(static_file.read(), content_type=self.guess_mimetype(filepath))
    
    @garbage_collector
    def send_static_img(self, filepath):
        with open(self.static_folder + filepath, "rb") as static_file:
            mimetype = self.guess_mimetype(filepath)
            return Response(static_file.read().decode("latin-1"), content_type=mimetype)

    @garbage_collector 
    def guess_mimetype(self, file : str):
        mimetypes = {"js" : "text/javascript", "css" : "text/css", "html" : "text/html", "svg" : "image/svg+xml", "ico" : "image/x-icon", "json" : "application/json"}
        return mimetypes[file.split(".")[-1]]
    
    @micropython.native
    def run(self, address: str, port: int):
        print(f"Server is running on http://{address}:{port}")
        serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
        try:
            serversocket.bind((address, port))
            serversocket.listen(5)
            while True:
                clientsocket, _ = serversocket.accept()
                request = clientsocket.recv(1024).decode()
                gc.collect()
                try:
                    parsed_req = self.request_parser(request)
                    response = self.get_route_function(parsed_req.path)(parsed_req)
                    gc.collect()
                except Exception as e:
                    print(e)
                    gc.collect()
                    response = Response({"msg": f"500 - server error - {e}"}, 500)
                finally:
                    print(response.status_code, parsed_req.method, parsed_req.path)
                    clientsocket.sendall(self.build_response(response).encode())
                    clientsocket.close()
                    gc.collect()

        finally:
            serversocket.close()


