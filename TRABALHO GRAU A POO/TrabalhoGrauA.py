
#CODIGO ESTA COMENTADO 

import os

class Pousada:
    def __init__(self): #PARTE DO CODIGO DEDICADA A STR(NOME), STR(C0NTATO), LISTA DE QUARTOS, LISTA DE RESERVAS
        self.__nome=0   #LISTA DE PRODUTOS, 
        self.__contato=0
        self.quartos = []  
        self.reservas = [] 
        self.produtos = []
        #CATEGORIA DOS QUARTOS
        self.tipos_categorias = { 
            'M': 'Master',
            'S': 'Standard',
            'P': 'Premium',
        }
        self.Status_Reservas = { 
            'A': 'Ativa',
            'C': 'Cancelada',
            'I': 'Check-In',
            'O': 'Check-Out',
        }
        self.carregaDados() 

    #FUNÇÃO PARA GERAR ARQUIVOS TXT
    def verificarArquivo(self,nomeArquivo):
        return os.path.isfile(nomeArquivo)

    #PARA ATRIBUIR NOME 
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self):
        raise ValueError('Erro Nome Da Pousada Não Encontrado')
    
    def registarNome(self):
        nome=str(input('Digite o Nome Que Deseja Para A Pousada: '))
        self.__nome=nome
    def getNome(self):
        return self.__nome
    
    #PARA ATRIBUIR CONTATO 
    @property
    def contato(self):
        return self.__contato
    @contato.setter
    def contato(self):
        raise ValueError('Contato Da Pousada Não Encontrado')
    
    def registrarContato(self):
        contato=str(input('Digite o Contato Para a Pousada: '))
        self.__contato=contato
    def getContato(self):
        return self.__contato

    #PARA REGISTRAR OS ATRIBUTOS NA FUNÇÃO

    #PARA ATRIBUIR OS METODOS DA POUSADA
    def carregaDados(self):
        #FUNÇÃO PARA CARREGAR OS DADOS DO ARQUIVO TXT
        nomeArquivo='pousada.txt'
        if self.verificarArquivo(nomeArquivo)==True:
            with open('pousada.txt','r') as ARQpousada:
                nLinhas = int(ARQpousada.readline().strip())
                nLinhas = int(nLinhas)
                for i in range(nLinhas):
                    linha = ARQpousada.readline().strip()
                    a=linha.split(',',2)
                    self.__nome=a[0]
                    self.__contato=a[1]
        else:
            with open('pousada.txt','w') as ARQpousada:
                self.registarNome()
                self.registrarContato()
                ARQpousada.writelines('1')
                dados=(self.nome,',',self.contato)
                dados=str(dados)
                ARQpousada.writelines(dados)

        #FUNÇÃO PARA ARQUIVO TXT DO QUARTO
        with open('quarto.txt','r') as ARQquartos:
            nLinhas=int(sum(1 for _ in ARQquartos))
            ARQquartos.seek(0)
            quartos = []
            for i in range(nLinhas):
                linha = ARQquartos.readline().strip()
                a=linha.split(',',3)
        
                quarto=Quarto(a[0],a[1],a[2],a[3]) #
                quartos.append(quarto)
            self.quartos=quartos

        #FUNÇÃO PARA ARQUIVO TXT DA RESERVA
        with open('reserva.txt','r') as ARQreservas:
            nLinhas=int(sum(1 for _ in ARQreservas))
            ARQreservas.seek(0)
            reservas = []
            for i in range(nLinhas):
                linha = ARQreservas.readline().strip()
                a=linha.split(',',4)
                
                reserva=Reserva(a[0],a[1],a[2],a[3],a[4]) 
                reservas.append(reserva) #
                self.reservas=reservas
        
        #FUNÇÃO PARA ARQUIVO TXT DE PRODUTOS
        with open('produto.txt', 'r') as ARQprodutos:
            nLinhas = int(sum(1 for _ in ARQprodutos))
            ARQprodutos.seek(0)
            produtos = []
            for i in range(nLinhas):
                linha = ARQprodutos.readline().strip()
                a = linha.split(',', 3)
                produto = Produto(a[0].strip(), a[1].strip(), float(a[2].strip()))
                produtos.append(produto)
            self.produtos=produtos
        
        return {
            "quartos": self.quartos,
            "reservas": self.reservas,
            "produtos": self.produtos
        }

    def salvaDados(self):
        #FUNÇÃO QUE FILTRA APENAS RESERVAS ATIVAS
        reservas_validas=[reserva for reserva in self.reservas if reserva.status in ['A', 'I']]
        #TODOS OS QUARTOS
        with open('quarto.txt', 'w') as f:
            for quarto in self.quartos:
                f.write(f"{quarto.numero},{quarto.categoria},{quarto.diaria},{','.join(quarto.consumo)}\n")
        #RESERVAS QUE SÃO VALIDAS
        with open('reserva.txt', 'w') as f:
            for reserva in reservas_validas:
                f.write(f"{reserva.quarto},{reserva.diaInicio},{reserva.diaFim},{reserva.cliente},{reserva.status}\n")
        #PRODUTOS DA POUSADA
        with open('produto.txt', 'w') as f:
            for produto in self.produtos:
                f.write(f"{produto.codigo},{produto.nome},{produto.preco}\n")
        print("Dados Foram Salvos Com Sucesso!")

    def consultaDisponibilidade(self, data, numero_quarto): 
        for quarto in self.quartos:
            if quarto.numero == numero_quarto:
                #VERIFICA A DATA DA RESERVA
                for reserva in self.reservas:
                    if reserva.quarto == quarto.numero and reserva.diaInicio <= data <= reserva.diaFim:
                        print('O Quarto Escolhido Não Esta Disponivel!')
                        return
                print('O Quarto Escolhido Esta Disponivel!')
                print('Informaçoes Sobre o Quarto:')
                print(f"Número: {quarto.numero}")
                print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                print(f"Diária: {quarto.diaria}")
                return
        raise ValueError("Quarto Inválido.")

    def consultaReserva(self, data=None, cliente=None, numero_quarto=None):
        reservas_encontradas = []
        #FINÇÃO PARA VALIDAR AS RESERVAS
        for reserva in self.reservas:
            if reserva.status != 'A':
                continue  
            #FILTRA A RESERVA PELO NOME E DATA
            cliente_ok = (cliente is None or cliente.strip() == '' or reserva.cliente.lower() == cliente.lower())
            data_ok = (data is None or (reserva.diaInicio <= data <= reserva.diaFim))
            quarto_ok = (numero_quarto is None or reserva.quarto == numero_quarto)
            
            if data_ok and cliente_ok and quarto_ok:
                reservas_encontradas.append(reserva)
        
        if reservas_encontradas:
            print("A Reserva Foi Encontrada!:")
            for reserva in reservas_encontradas:
                print(f"Cliente: {reserva.cliente}")
                print(f"Data Inicial: {reserva.diaInicio}")
                print(f"Data Final: {reserva.diaFim}")
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                if quarto:
                    print('Informações do quarto:')
                    print(f"Número: {quarto.numero}")
                    print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                    print(f"Diária: {quarto.diaria}")
                
        else:
            print("Nenhuma Reserva Foi Encontrada Com Esses Dados!.")

    def realizarReserva(self,dataI,dataF,cliente,numero_quarto):
        #VERIFICA DISPONIBILIDADE DO QUARTO
        for reserva in self.reservas:
            if reserva.quarto == numero_quarto and \
            (reserva.diaInicio <= dataF and reserva.diaFim >= dataI):
                print("Este Quarto Já Esta Reservado!.")
                return

        
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and \
            reserva.status in ['A', 'I']:  
                print("O Clinte Já Possui Uma Reserva Ativa!.")
                return

        
        nova_reserva = Reserva(numero_quarto, dataI, dataF, cliente, 'A') 
        self.reservas.append(nova_reserva)
        print("Reserva realizada com sucesso!")

    def cancelaReserva(self, cliente):
        
        reserva_encontrada = False
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'A':
                reserva.status = 'C'  #STATUS C RESERVA ESTA CANCELADA
                reserva_encontrada = True
                print(f"Reserva do Cliente '{cliente}' Foi Cancelada!")
                break
        if not reserva_encontrada:
            print("Não Ha Nenhuma Reserva Ativa No Nome Informado!.")

    def realizaCheckIn(self,cliente):
        
        reserva_encontrada = False
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'A':
                reserva.status = 'I' 
                reserva_encontrada = True
                #FUNÇÃO PRINT DOS DADOS
                print(f"Data Inicial: {reserva.diaInicio}")
                print(f"Data Final: {reserva.diaFim}")
                TotalDias=reserva.diaFim-reserva.diaInicio
                print(F"Quantidade de Dias: {TotalDias}")
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                TotalDiarias=TotalDias*quarto.diaria
                print(F"VALOR Total das Diarias: {TotalDiarias}")
                if quarto:
                    print('Informações do quarto:')
                    print(f"Número: {quarto.numero}")
                    print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                    print(f"Diária: {quarto.diaria}")
                    print('Check-In realizado com sucesso! aproveite sua estadia!')
                return  
        if not reserva_encontrada:
            print("Não Ha Nenhuma Reserva Ativa No Nome Informado!.")

    def realizaCheckOut(self, cliente):
        reserva_encontrada = False
        
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'I':
                reserva_encontrada = True
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                
                if quarto:
                    #CALCULAR RESERVA E VALORES
                    total_dias = reserva.diaFim - reserva.diaInicio
                    total_diarias = total_dias * quarto.diaria
                    total_consumo = quarto.valorTotalConsumo(pousada.produtos)
                    valor_final = total_diarias + total_consumo
                    
                    print(f"Cliente: {reserva.cliente}")
                    print(f"Data Inicial: {reserva.diaInicio}")
                    print(f"Data Final: {reserva.diaFim}")
                    print(f"Quantidade de Dias: {total_dias}")
                    print(f"Valor Total das Diárias: R${total_diarias:.2f}")
                    #CONSUMO DO CLIENTE
                    quarto.listaConsumo(pousada.produtos)
                    print(f"Valor Total dos Consumos: R${total_consumo:.2f}")
                    print(f"Valor Final a ser Pago: R${valor_final:.2f}")
                    
                    reserva.status = 'O'
                    
                    quarto.limpaConsumo()
                    print("Check-out Realizado Com Sucesso!")
        if not reserva_encontrada:
            print("Nenhuma Seserva em Check-in Encontrada Com o Nome Informado!.")

    def registrarConsumo(self, cliente):
        
        reserva_encontrada = None
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'I':
                reserva_encontrada = reserva
                break
        if not reserva_encontrada:
            print("Nenhuma Eeserva em Check-in Encontrada Para o Nome informado!.")
            return
        #APRESENTA OS PRODUTOS DISPONIVEIS NA COPA
        print("Produtos Disponíveis na Copa!:")
        for produto in self.produtos:
            print(f"Código: {produto.codigo}, Nome: {produto.nome}, Preço: R${produto.preco:.2f}")
        
        codigo_produto = input("Digite o Código do Produto Que Deseja!: ")
        codigo_limpo = codigo_produto.strip() 
        
        produto_encontrado = next((p for p in self.produtos if p.codigo == int(codigo_limpo)), None)
        if produto_encontrado:
            quarto = next((q for q in self.quartos if q.numero == reserva_encontrada.quarto), None)
            if quarto:
                
                quarto.adicionaConsumo(codigo_limpo)  
                print(f"Consumo Foi Registrado!: {produto_encontrado.nome} - R${produto_encontrado.preco:.2f}")
            else:
                print("Quarto não Foi Encontrado!.")
        else:
            print("Produto não foi Encontrado!.")

class Quarto: 
    def __init__(self,numero,categoria,diaria,consumo): 
        self.numero=int(numero)
        self.categoria=str(categoria)
        self.diaria=float(diaria)
        self.consumo = consumo.split(',')
    def __str__(self):
        return f"Quarto({self.numero},{self.categoria},{self.diaria},{self.consumo})"
    def __repr__(self):
        return self.__str__()

    def adicionaConsumo(self, codigo_produto):
        self.consumo.append(codigo_produto)

    def listaConsumo(self, produtos):
        if not self.consumo:
            print("Não há nenhum Consumo Registrado Para Este Quarto!.")
            return
        print("Consumo do Quarto", self.numero, ":")
        for codigo in self.consumo:
            codigo_limpo = codigo.strip('() ') #limpeza de caracteres
            try:
                produto = next((p for p in produtos if p.codigo == int(codigo_limpo)), None)
                if produto:
                    print(f"Produto: {produto.nome}, Preço: R${produto.preco:.2f}")
                else:
                    print(f"Produto com Código {codigo_limpo} Não Encontrado!.")
            except ValueError:
                print(f"Código do Produto é Inválido!: {codigo}.")

    def valorTotalConsumo(self, produtos):
        total = 0.0
        for codigo in self.consumo:
            
            codigo_limpo = codigo.strip('() ')  
            produto = next((p for p in produtos if p.codigo == int(codigo_limpo)), None)
            if produto:
                total += produto.preco
        return total
    
    def limpaConsumo(self):
        
        self.consumo = []

class Reserva:   #FUNÇÃO INT(diaInicio),INT9diaFim), STRING(cliente), QUARTO(Quarto)
    def __init__(self,quarto,diaInicio,diaFim,cliente,status):
        self.quarto=int(quarto)
        self.diaInicio=int(diaInicio)
        self.diaFim=int(diaFim)
        self.cliente=str(cliente)
        self.status=str(status)
    def __str__(self):
        return f"Reserva({self.quarto},{self.diaInicio},{self.diaFim},{self.cliente},{self.status})"
    def __repr__(self):
        return self.__str__()

class Produto: #FUNÇÃO INT(código), STR(nome), FLOAT(preco)
    def __init__(self,codigo,nome,preco):
        self.codigo=int(codigo)
        self.nome=str(nome)
        self.preco=float(preco)
    def __str__(self):
        return f"Produto({self.codigo},{self.nome},{self.preco})"
    def __repr__(self):
        return self.__str__()

#FUNÇÃO QUE ABRE O MENU
pousada=Pousada()
sair=False
print('Seja bem-vindo ao sistema da pousada',pousada.getNome(),'!')
while sair!=True:
    print('----- MENU -----')
    print('1 -> Consultar Disponibilidade')
    print('2 -> Consultar Reserva')
    print('3 -> Realizar Reserva')
    print('4 -> Cancelar Reserva')
    print('5 -> Realizar Check-in')
    print('6 -> Realizar Check-out')
    print('7 -> Registrar Consumo')
    print('8 -> Salvar')
    print('0 -> Sair')
    resposta=int(input('Selecione a Opção Que Deseja Executar!: '))

    if resposta == 0:
        print("---------------------------")
        sair=True
        pousada.salvaDados()
        print('Encerramento Do Sistema!...')
        print("---------------------------")

    elif resposta == 1:
        print("---------------------------")
        data=int(input('Digite a Data que Deseja Consultar!: '))
        numero_quarto=int(input('Digite o Número do Quarto que Deseja Consultar!: '))
        print("---------------------------")
        pousada.consultaDisponibilidade(data,numero_quarto)
        print("---------------------------")

    elif resposta == 2:
        print("---------------------------")
        data_input = input('Digite a Data que Deseja Consultar!: ')
        cliente = input('Digite o Nome do Cliente!: ')
        numero_quarto_input = input('Digite o Número do Quarto! ')
        data = int(data_input) if data_input else None
        numero_quarto = int(numero_quarto_input) if numero_quarto_input else None
        print("---------------------------")
        pousada.consultaReserva(data, cliente, numero_quarto)
        print("---------------------------")
        
    elif resposta == 3:
        print("---------------------------")
        dataI=int(input('Digite a Data Inicial da Reserva!: '))
        dataF=int(input('Digite a Data do Fim da Reserva!: '))
        cliente=str(input('Digite seu nome Para Reservar!: '))
        numero_quarto=int(input('Digite o Número do Quarto que Deseja Fazer a Reserva!: '))
        print("---------------------------")
        pousada.realizarReserva(dataI,dataF,cliente,numero_quarto)
        print("---------------------------")

    elif resposta == 4:
        print("---------------------------")
        cliente=str(input('Digite o Nome em que a Reserva foi Registrada Para Fazer o Cancelamento!: '))
        print("---------------------------")
        pousada.cancelaReserva(cliente)
        print("---------------------------")

    elif resposta == 5:
        print("---------------------------")
        cliente=str(input('Digite o Nome do Cliente que a Reserva Pertence!: '))
        print("---------------------------")
        pousada.realizaCheckIn(cliente)
        print("---------------------------")

    elif resposta == 6:
        print("---------------------------")
        cliente=str(input('Digite o Nome de Quem é a Reserva!: '))
        print("---------------------------")
        pousada.realizaCheckOut(cliente)
        print("---------------------------")

    elif resposta == 7:
        print("---------------------------")
        cliente=str(input('Digite o Nome de Quem é a Reserva!: '))
        print("---------------------------")
        pousada.registrarConsumo(cliente)
        print("---------------------------")

    elif resposta == 8:
        pousada.salvaDados()

