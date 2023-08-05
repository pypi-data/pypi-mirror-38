class IAList:

    @classmethod
    def reconhecimento_padroes(cls):
        return "Associar um conjunto de dados a um rótulo, que representa uma classe determinada. Por exemplo, identificar os objetos presentes em uma imagem ou identificar uma pessoa pela voz."

    @classmethod
    def etapas_reconhecimento_padroes(cls):
        return """
            - Pre-processamento: preparação e filtragem dos dados brutos, tornando-os mais adequados para a classificação
            - Extração de atributos determinação dos atributos numéricos a serem empregados na classificação, bem como a extração dos seus valores do conjunto de dados sendo classificados
            - Classificação: determinação da classe do conjunto de dados a partir da classificação dos vetores de atributos
        """

    @classmethod
    def modalidades_machine_learn(cls):
        return """
            - Aprendizado supervisionado: Envolve o aprendizado de uma “função” a partir de exemplos de entrada e saída, fornecidos por um tutor
            - Aprendizado não-supervisionado: Envolve o aprendizado de padrões dos dados de entrada, agrupando dados semelhantes e separando dados distintos
            - Aprendizado por reforço: Envolve o aprendizado de ações ou comportamentos com base em reforços positivos ou negativos recebidos pelo agente
        """,

    @classmethod
    def classificação_linear_nao_linear(cls):
        return """
            Classificadores lineares separam o espaço de atributos através de superfícies de separação lineares (retas, planos ou hiperplanos, dependendo da dimensionalidade do espaço de atributos), enquanto classificadores não lineares podem criar superfícies de separação mais genéricas.
            Exemplos de classificadores lineares: Perceptron, Adaline
            Exemplos de classificadores não lineares: Multilayer Perceptron, SVM, árvores de decisão, kNN
        """,

    @classmethod
    def machine_learning(cls):
        return """"MachineLearning ou aprendizado de máquina é o campo de estudo de programas de computadores que melhoram seu desempenho de acordo com sua experiência (Tom Mitchell,
            - Do ponto de vista da IA, seu foco é permitir que agentes artificiais melhorem os resultados de sua medida de desempenho de acordo
            com dados “inputados” por operadores humanos ou capturados ao
            longo da sua interação com o ambiente, sem a necessidade de
            programá-lo explicitamente para aqueles resultados.
             Aprendizado indutivo: aprender uma regra geral a partir de
            exemplos
        """
    
    @classmethod
    def hiperparameters(cls):
        return """
            O que são os hiperparâmetros de taxa de aprendizado e
            o batch size no
            aprendizado da rede MLP?
            -
            Taxa de aprendizado: número positivo que indica a magnitude das atualizações dos pesos a
            cada iteração do algoritmo de aprendizado (backpropagation). Não deve ser nem  muito
            pequeno a ponto de atrasar a converg
            ência do algoritmo, e nem muito grande ao ponto de
            tornar o aprendizado instável
            -
            Batch size: número de entradas (deve ser pelo menos uma) usadas para calcular a correção
            dos pesos na rede neural. Quanto menor esse número, mais oscilações poderão ser ver
            ificadas
            na curva de aprendizado; quanto maior for esse número, menos eficiente será o algoritmo de
            treinamento, podendo demorar mais para convergir.
        """

    @classmethod
    def camada_entrada_saida(cls):
        return """
            O que são a camada de entrada e de saída de uma rede neural. Qual é o seu 
            significado nas redes MLP e Perceptron?
            A camada de saída corresponde aos atributos sendo usados como entrada da rede neural. 
            Assim, o número de elementos dessa camada corresponde ao numero de atributos sendo 
            classificado. Já a camada de saída corresponde aos neurônios cuja ativação indica o resultado 
            da 
            classificação. Assim, o número de neurônios na camada de saída corresponde ao número de 
            classes que que podemos classificar os dados de entrada.
            Isso vale tanto para a MP quanto 
            para a rede Perceptron.
        """
    
    @classmethod
    def mlp_architeture(cls):
        return """
            Quais são os hiper parâmetros da rede MLP relacionadas à sua arquitetura?
            Qual é o seu significado?
            A rede Perceptron possui esses hiperparâmetros?
            Os hiperparâmetros que definem a arquitetura de uma MLP (Multilayer Perceptron) são:
            a)Número de camadas ocultas: número de camadas de neurônios entre a camada de entrada e a camada de saída
            b)Número de neurônios em cada camada oculta:
            c) Função de ativação:
            função que processa o potencial de ação a, também chamado de entrada líquida da rede, para produzir
            Costumam ser usadas as seguintes funções numa MLP: logística ou sigmoide, tanhegnte
            hiperbólica e linear retificada
        """
    
    @classmethod
    def overflit(cls):
        return """
            O problema de overfitting ocorre quando um classificador se torna muito 
            especializado em classificar as amostras de treinamento, de forma a
            adaptar inclusive ao ruído das mesmas, resultando numa perda de 
            desempenho (aumento de erro) ao classificar as amostras de teste. Para 
            evitar o problema de overfitting em MLPs, devese ter a preocupação em 
            não exagerar no número de neurônios da cama
            da oculta, empregando a validação cruzada para chegar em um valor equilibrado de neurônios cujo 
            treinamento seja realizado em tempo aceitável, apresentando bons 
            resultados tato nas amostras de treinamento quanto nas amostras de teste.
        """

    @classmethod
    def all(cls):
        return {
            "1. Reconhecimento de padrões?": cls.reconhecimento_padroes(),
            "2. Etapas reconhecimento de padrões": (
                cls.etapas_reconhecimento_padroes()
            ),
            "3. Modalidades de aprendizagem em machine learning": (
                cls.modalidades_machine_learn()
            ),
            """
                4. Classificadores lineares e não-lineares? Pesquise e
                dê um exemplo de cada. O kNN encontra-se em que categoria?
            """: cls.classificação_linear_nao_linear(),
            "Machine Learning": cls.machine_learning()
            "Oferflitting": cls.overflit(),
            "Arquitetura MLP": cls.mlp_architeture(),
            "Camada entrada e saida": cls.camada_entrada_saida(),
            "Hiperparametros": cls.hiperparameters()
        }
