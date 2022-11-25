import cv2
import pickle
import struct
import socket


class ImgClient:
    def __init__(self, host, port, protcol='ipv4', type='tcp'):
        self.protcol = socket.AF_INET if protcol=='ipv4' else socket.AF_INET6
        self.socket_type = socket.SOCK_STREAM if type=='tcp' else socket.SOCK_DGRAM
        self.host = host
        self.port = port
        self.pack_format = ">L"
        self.connect()
        
    def connect(self):
        self.client_socket = socket.socket(self.protcol, self.socket_type)
        self.client_socket.connect((self.host, self.port))
        connection = self.client_socket.makefile('wb')
        print('acceptting request .......')
        
    def send(self, image):
        result, encode = cv2.imencode('.jpg', image, (cv2.IMWRITE_JPEG_QUALITY, 30))
        data = pickle.dumps(encode, 0)
            # size = len(data)
        self.client_socket.sendall(struct.pack(self.pack_format, len(data)) + data)
        print('send success')
        #except:
        #    self.client_socket.shutdown(socket.SHUT_RDWR)
        #    self.client_socket.close()
        #    sys.exit(1)





class ImgServer:
    def __init__(self, host, port, protcol='ipv4', type='tcp'):
        self.protcol = socket.AF_INET if protcol=='ipv4' else socket.AF_INET6
        self.socket_type = socket.SOCK_STREAM if type=='tcp' else socket.SOCK_DGRAM
        self.host = host
        self.port = port
        self.pack_format = ">L"
        #self.accept()

    def accept(self):
        # 1. socket
        self.server_socket = socket.socket(self.protcol, self.socket_type)
        # 2. bind
        self.server_socket.bind((self.host, self.port))
        # 3. listen
        self.server_socket.listen(10)
        print('Server started')

    def img_unpack(self, data, payload_size):
        # unpack
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(self.pack_format, packed_msg_size)[0]
        print("Done Recv data: {}, msg size: {}".format(len(data), msg_size))
        return data, msg_size
        
    def byte2img(self, frame_data):
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)

    def recieve(self):
        data = b""
        conn, addr = self.server_socket.accept()
        payload_size = struct.calcsize(self.pack_format)
        print("payload_size: {}".format(payload_size))
        while True:
            while len(data) < payload_size:
                #print("Recv: {}".format(len(data)))
                data += conn.recv(4096)
                      
            data, msg_size = self.img_unpack(data, payload_size)
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            # byte 2 img
            frame = cv2.cvtColor(self.byte2img(frame_data), cv2.COLOR_BGR2RGB)
            return frame
            

