import datetime
import socket

## DOWNLOAD DO CLIENTE

HOST = '0.0.0.0'
PORT = 8888
PACKAGE_SIZE = 4096

package = b'x' * PACKAGE_SIZE * 4

print("\n### Testando Download do Cliente ###\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(0)
print(f'Escutando em {HOST}:{PORT}')

client_sock, client_addr = sock.accept()

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} conectado')

while True:
    client_sock.send(package)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= 20):
        client_sock.close()
        break

endtime = datetime.datetime.now()
print(endtime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

## UPLOAD DO CLIENTE
print("### Testando Upload do Cliente ###\n")

sock.listen(0)
print(f'Escutando em {HOST}:{PORT}')

client_sock, client_addr = sock.accept()

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} conectado')

while True:
    data = client_sock.recv(PACKAGE_SIZE)
    if data:
        del data
        continue

    client_sock.close()

    endtime = datetime.datetime.now()
    print(endtime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

    break

sock.close()
