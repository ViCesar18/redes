import socket
import time

ip = '0.0.0.0'
port = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))

addr = (ip, port)
package_size = 1024
buffer_size = 8
buffer = []
i = 0

f = open('./recebido/uel.jpg', 'wb')

package_number = 0

Count, countadress = server_socket.recvfrom(package_size)

tillI = Count.decode()
tillI = int(tillI)

loop = True
transmission_start = time.time()
while loop:
    package, addr = server_socket.recvfrom(package_size)

    if package == b'OK!':
        for data in buffer:
            f.write(data)

        buffer = []
    elif package == b'QNTD?':
        server_socket.sendto(str(i).encode(), addr)
        i = 0
    elif package == b'RESET!':
        buffer = []
    elif package == b'END!':
        loop = False
    else:
        buffer.append(package)
        
        i += 1
        package_number += 1
        tillI -= 1  
        print(f"Recebendo pacote numero: {package_number}")

f.close()
server_socket.close()

transmission_end = time.time()
transmission_time = transmission_end - transmission_start

print('\nArquivo enviado com sucesso!')
print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
print(f'Número de Pacotes transmitidos: {package_number}')
print(f'Tamanho dos Pacotes: {package_size}')
print(f'Tamanho do Buffer: {buffer_size}')
print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits