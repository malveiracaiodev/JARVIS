"""
=========================================
JARVIS CORE

Arquivo:
tools.py

Descrição:
Sistema de ferramentas do JARVIS.

Responsável por:
- Registrar ferramentas
- Executar capacidades
- Gerenciar ações externas

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""



class Tools:



    """
    Gerenciador das capacidades
    externas do JARVIS.
    """



    def __init__(self):


        self.tools = {}



    # ---------------------------------
    # Registrar ferramenta
    # ---------------------------------

    def register(

            self,

            name,

            function

    ):


        self.tools[name] = function



        print(

            "[TOOLS] Registrada:",

            name

        )



    # ---------------------------------
    # Executar ferramenta
    # ---------------------------------

    def execute(

            self,

            name,

            *args,

            **kwargs

    ):


        tool = self.tools.get(
            name
        )



        if not tool:


            return (

                "Ferramenta não encontrada"

            )



        try:


            return tool(

                *args,

                **kwargs

            )


        except Exception as error:


            return (

                f"Erro ao executar: {error}"

            )



    # ---------------------------------
    # Listar ferramentas
    # ---------------------------------

    def available(self):


        return list(

            self.tools.keys()

        )



    # ---------------------------------
    # Remover
    # ---------------------------------

    def remove(

            self,

            name

    ):


        if name in self.tools:


            del self.tools[name]