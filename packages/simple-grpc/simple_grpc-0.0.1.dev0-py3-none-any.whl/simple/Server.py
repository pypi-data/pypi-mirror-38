import concurrent.futures
import socket
import h2.connection
from h2.config import H2Configuration

from .Request import Request

class Application:
    def __init__(self, packageName, **kwargs):
        self.packageName = packageName
        self.services = {}
        
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((kwargs.get('listen_on', '0.0.0.0'), kwargs.get('port', 50051)))
        self.sock.listen(5)
        pass

    def AddService(self, service):
        self.services[".".join([self.packageName, service.name])] = service
        pass

    def handle(self, sock):
        conn = h2.connection.H2Connection(H2Configuration(client_side=False)) 
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())
        while True:
            data = sock.recv(65535)
            if not data:
               break 
            events = conn.receive_data(data)
            request = Request()
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    request.headers = event
                if isinstance(event, h2.events.DataReceived):
                    request.data = event
            if request.Validate():
                self.route(request)
                pass
    
    def route(self, request):
        self.services[request.pathParts[0]].handle(request)
        pass

    def serve(self):
        while True:
            self.handle(self.sock.accept()[0])
        pass
    #def Service(self, recieves=None, returns=None, **kwargs):
    #    '''
    #    Service is a function that 
    #    '''
    #    assert issubclass(returns, Message)
    #    returns = returns()
    #    def wrapper(func):
    #        self.modules[func.__name__] = self._wrap(func, returns, recieves, kwargs)
    #        def func_wrappper(*args, **kwargs):
    #            return func(*args, **kwargs)
    #        return func_wrappper
    #    return wrapper
    
    #def _wrap(self, func, returns: Message, recieves: Message, attrs: dict):
    #    if recieves is None:
    #        name = func.__name__ + "Message"
    #        recieves = MessageBase(name, (Message, ), attrs)
    #        pass
    #    recieves = recieves()
    #    def request(request, context):
    #        print (request)
    #        func(**request)
    #    return grpc.unary_unary_rpc_method_handler(
    #      func,
    #      request_deserializer= recieves.FormGRPC().FromString,
    #      response_serializer=returns.FormGRPC().SerializeToString,
    #    )