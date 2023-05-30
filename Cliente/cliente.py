import socket, pickle

def criaCliente():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 5000))
        print('\nConectado ao servidor!\n')
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')
    
    try:
        lista_recebida = client.recv(4096)
        arquivos = pickle.loads(lista_recebida)
    except:
        print('\nOcorreu um erro com a lista de arquivos!\n')
    
    print('Arquivos disponíveis:\n')
    print(arquivos)

    nomeArquivo = str(input('\nNome arquivo> '))

    while nomeArquivo not in arquivos:
        nomeArquivo = str(input('\nO arquivo solicitado não está disponível, digite novamente> '))

    client.send(nomeArquivo.encode())

    with open(nomeArquivo, 'wb') as file: #wb -> escreve o arquivo
        try:
            while True:
                data = client.recv(1000000)
                if not data:
                    break
                file.write(data)
        except:
            print('Ocorreu um erro na leitura do arquivo!')
            client.close()
        
    print(f'\n{nomeArquivo} recebido!\n')

criaCliente()
    