import datetime
import socket

## DOWNLOAD DO CLIENTE

HOST = '0.0.0.0'
PORT = 8888
PACKAGE_SIZE = 1024

HEADER_SIZE = 8
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

print(f'\nVinculado em {HOST}:{PORT}\n')

data, client_addr = sock.recvfrom(PACKAGE_SIZE)
if data == b'CONNECT!':
    sock.sendto(b'CONNECTED!', client_addr)
else:
    print('Server nao se conectou com o cliente!')
    exit(1)

print("### Testando Download do Cliente ###\n")

sock.settimeout(3)

starttime = datetime.datetime.now()
package_id = 1
count_timeout = 0
payload = b'x' * PAYLOAD_SIZE

while True:
    header = bytes('{:0>8}'.format(format(package_id, 'X')), 'utf-8')      #Faz um header com caracteres com um identificador único para cada pacote, em hexadecimal
    package_id += 1
    package = b''.join([header, payload])

    sock.sendto(package, client_addr)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= 20):
        header = bytes('{:0>8}'.format(0), 'utf-8')     #Faz um header com HEADER_SIZE 0's, em hexadecimal
        package = b''.join([header, b'END!'])

        while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
            try:
                sock.sendto(package, client_addr)
                data, client_addr = sock.recvfrom(PACKAGE_SIZE)

                if data == b'OK!':
                    break
            except socket.timeout:
                if count_timeout == 5:
                    break
                else:
                    count_timeout = count_timeout + 1
                    continue
        break

count_timeout = 0
while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
    try:
        sock.sendto(str(package_id).encode(), client_addr)
        data, client_addr = sock.recvfrom(PACKAGE_SIZE)

        if data == b'OK!':
            break
    except socket.timeout:
        if count_timeout == 5:
            break
        else:
            count_timeout = count_timeout + 1
            continue

## UPLOAD DO CLIENTE
print("### Testando Upload do Cliente ###\n")

sock.settimeout(None)

package_counter = 0

while True:
    package, server_socket = sock.recvfrom(PACKAGE_SIZE)
    package_counter = package_counter + 1

    package_id = int(str(package)[2:HEADER_SIZE+2], 16)

    if package_id != 0:
        continue

    sock.sendto(b'OK!', client_addr)

    break

sock.settimeout(3)

while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até perder a conexão com o cliente
    try:
        sock.sendto(str(package_counter).encode(), client_addr)
        data, client_addr = sock.recvfrom(PACKAGE_SIZE)

        if data == b'OK!':
            break
    except socket.timeout:
        continue
    except ConnectionResetError:
        break

sock.close()
