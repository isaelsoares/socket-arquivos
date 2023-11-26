# socket-arquivos
Compartilhamento de arquivos com python

Para o desenvolvimento do projeto foram necessário quatro depêndencias:

- Socket: Fornece as funcionalidades necessárias para comunição em rede usando sockets.

- Threading: Permite a criação de threads para lidar com várias conexões de clientes.

- Os: Oferece funcionalidades relacionadas ao sistema operacional, no caso desse projeto foi usado a listagem de arquivos de um diretório

- Pickle: Permite serializar e desserializar objetos Python.


## Server.py - documentação

No incío do arquivo server.py teremos duas variáveis globais: **arquivos** e **clientes**. 

A variável **arquivos** armazena os arquivos que estão no mesmo diretório que o server.py, já a variável **clientes** armazena os clientes conectados.

Função **criaServidor()**: Está função é reponsável por criar e incializar o servidor socket para receber conexões de clientes. A função ficou organizada da seguinte forma:

```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind(('localhost', 5000))
        server.listen()
        print('\nServidor iniciou!\n Aguardando conexões...\n') 
    except:
        print('\nOcorreu um erro ao iniciar o servidor!\n')
```

Na primeira linha criamos o socket usando a família de endereços IPv4 **(socket.AF_INET)** e o protocolo TPC **(socket.SOCK_STREAM)**, a escolha do protolo TPC deve-se ao fato de que ele garante que nenhuma parte da mensagem ou arquivo enviado seja perdida pelo caminho.

Ademais, tentamos associar o endereço do servidor a porta 5000 fazendo uso do método **bind()**. Se tudo correr bem, o servidor é iniciado e está pronto para receber conexões, junto a isso criamos um  método listen() para deixar o servidor no modo espera. 

Observação: Foi utilizado a instrução Try para que se o servidor não for iniciado, temos a garantia que a função **criaServidor()** será quebrada.

Depois disso, temos um loop infinito que cuidará da recepção dos clientes.

```
    while True:
        cliente, endereco = server.accept()
        clientes.append(cliente) 
        print(f'{endereco} Conectado') 

        lista_serializada = pickle.dumps(arquivos)
        cliente.send(lista_serializada)

```

Através do método **accept()** aceitaremos os clientes que estiverem tentando se conectar ao servidor, na linha de baixo esse cliente será colocado na lista de clientes e em seguida será imprimido na tela do servidor o endereço do cliente que se conectou. Mais além faremos uso da dependência **Pickle** para achatar a lista de arquivos e enviar em único fluxo para o cliente usando o método **send()**. 

Quando a lista de arquivos é enviada, inicia a etapa da função **TrataArquivo** que se reponsabiliza por receber o nome do arquivo e encaminhar para a função enviarArquivo os parâmetros do cliente que pediu e o que ele pediu.

```
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
```

Inicia-se uma nova thread para lidar com o nome do arquivo enviado pelo cliente, chamando a função **trataArquivo()**. Nessa função teremos um loop onde recebermos  o nome do arquivo usando o método **recv()** e converemos para string usando método **decode()**, se isso der certo esse valor será armazenado na variável **nomeArquivo** e será passado junto ao parâmetro cliente para a função reponsável por enviar os arquivos **enviarArquivos()**. Caso não seja possível ouvir o cliente, significa que ele não está mais online, então o cliente é removido a lista de clientes e o processo é quebrado.

Por fim, temos a função enviarArquivos().

```
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

```

A função enviar arquivo inicia com um For que itera sobre os itens na lista clientes para encontrar o cliente correspondente ao objeto de socket fornecido afim de garantir que o arquivo seja enviado para a pessoa cliente certo, nesse verificação também é analisado se o nome de arquivo solicitado se encontra na pasta.  Se as condições forem dadas como verdadeiras então incia o processo onde tentamos enviar o arquivo para o cliente. 

O whith open serve para abrir a variável **nomeArquivo** (o arquivo será aberto em modo binário), na próxima linha temos um **file.readlines():** que basicamente vai ler o arquivo linha por linha, toda vez que que uma linha for lida o for vai armazenar essa linha a variével data enviar para o cliente, quando o processo acabar será imprimido que o 'Arquivo foi enviado' e o cliente será desconectado. Em caso de erro o cliente é removido da lista de clientes e mensagem de erro é imprimida na tela do servidor.


## Cliente.py - documentação

A parte do cliente, por sí só é menos extensa já que comporta um número menor de operações.

Para o cliente foram usadas apenas duas dependências: **socket** e **pickle**.
 
Para começar temos uma única função que comporta todas as operações do cliente, a função **criaCliente()**:
```
def criaCliente():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 5000))
        print('\nConectado ao servidor!\n')
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')
```

Nesse primeiro trecho, criamos o socket com as mesmas configurações que o servidor, depois disso é utilizado o Try por que estamos tentanto estabilizar uma conexão com o servidor, se tudo correr bem é imprimido uma mensagem na tela confirmando a conexão, caso algo de errado a função é quebrada é imprimido a mensagem de erro.

Depois que cliente conectar tentaremos receber a lista de arquivos enviada pelo servidor, se lista chegar é armazena em **lista_recebida** onde na próxima linha usando o **Pickle** vamos abrir essa lista que veio de forma achatada. Se isso der certo, o código segue, onde vai imprimir a lista dos arquivos para que o cliente possa escolher. Abaixo da lista terá um input onde o usuário vai digitar o nome do arquivo que ele quer, porém se o nome digitado não estiver na lista o loop abaixo entra em ação e enquanto o nome digitado não estiver na lista o loop continua.

Se tudo correr bem, esse nome será enviado para o servidor atrvés do método **send**, usamos o encode para mandar em formato de bits.

```    
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

```

Posteriomente ao código acima teremos um with open composto de loop que vai ficar aguardando e pegando cada pedaço de informação enviado pelo servidor, quando não houver mais dados a serem recebidos o cliente é desconectado.

```
    with open(nomeArquivo, 'wb') as file:
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

```
