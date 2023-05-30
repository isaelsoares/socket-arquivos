import socket, threading, os, pickle

arquivos = os.listdir(".")
clientes = []

def criaServidor():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4 e TCP
    
    try:
        server.bind(('localhost', 5000))
        server.listen()
        print('\nServidor iniciou!\n Aguardando conexões...\n') 
    except:
        print('\nOcorreu um erro ao iniciar o servidor!\n')

    while True:
        cliente, endereco = server.accept()
        clientes.append(cliente) 
        print(f'{endereco} Conectado') 

        lista_serializada = pickle.dumps(arquivos)
        cliente.send(lista_serializada)

        thread = threading.Thread(target = TrataArquivo, args = [cliente])
        thread.start()

def TrataArquivo(cliente): 
    while True:  
        try:
            nomeArquivo = cliente.recv(2048).decode()
            enviarArquivo(nomeArquivo, cliente)
        except:
            clientes.remove(cliente)
            break

def enviarArquivo(nomeArquivo, cliente):
    for clientItem in clientes:
        if (clientItem == cliente) & (nomeArquivo in arquivos):
            try:
                with open(nomeArquivo, 'rb') as file:
                    for data in file.readlines():
                        cliente.send(data)
                print('Arquivo enviado!')
                cliente.close()
            except:
                clientes.remove(cliente) 
                print('Falha ao enviar o arquivo!')

criaServidor()
