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
        }
