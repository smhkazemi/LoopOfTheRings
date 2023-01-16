import csv
import hashlib
import random
import socket
import threading


class UnitOfServiceWork:
    def __init__(self, uv, ty):
        self.type = ty
        self.unit_value = uv


class Service:
    def __init__(self, ty, muw=1, uv=1):
        self.minimumUnitOfWork = muw
        self.unit_of_service_work = UnitOfServiceWork(uv, ty)


list_of_services = []
number_of_registered_traders = 0


def init_services(file_name):
    min_value_service = Service("", 1, 99999999)
    with open(file_name) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            list_of_services.append(Service(row[0], row[1], row[2]))
            if row[2] < min_value_service.unit_of_service_work.unit_value:
                min_value_service = list_of_services[-1]
    file_obj.close()
    return min_value_service


def calc_sha256(str):
    return hashlib.sha256(str.encode())


def get_details(data):
    response = data.split(' ')
    return response[1]


def broadcast_message(
        msg=b'getInfo'):  # simulating the system of the user - this function is seperated from the user to use multi-threading
    UDP_IP = "255.255.255.255"
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    for ip in allips:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, 0))
        sock.sendto(msg, (UDP_IP, 5005))
        sock.close()


def handle_message(data, min_value_service):
    data = data.decode()
    if "register" in data:
        amount = get_details(data)
        if amount >= 10 * min_value_service.unit_of_service_work.unit_value:
            broadcast_message(calc_sha256(random.random() * 10000000000))
        else:
            broadcast_message(-1)


def listen_for_new_registration_requests():
    UDP_IP = "255.255.255.255"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
        threading.Thread(target=handle_message, args=(data,)).start()
