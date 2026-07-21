"""
=========================================
GENESIS CORE

Arquivo:
personas/persona_factory.py

Descrição:

Fábrica dinâmica responsável pela criação
de Personas do Genesis Core.

Responsabilidades:

- Ler identity.json.
- Resolver módulos dinamicamente.
- Criar personalidades.
- Separar configuração de implementação.
- Permitir expansão por plugins.

Arquitetura:

Identity JSON
      |
      ▼
 Persona Factory
      |
      ▼
 Dynamic Loader
      |
 ┌────┴────┐
 ▼         ▼
Jarvis   Rafiki


Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


import json
import os
import importlib



from personas.persona import Persona





class PersonaFactory:


    """
    Criador dinâmico de Personas.

    A Factory não conhece nenhuma Persona
    específica.

    Ela apenas interpreta a identidade
    declarada no JSON.
    """



    def __init__(
        self,
        identity_path=None
    ):


        self.identity_path = (

            identity_path

            or

            "data/personas/identity.json"

        )


        self.identity = {}


        self.load()






    # ==================================================
    # CARREGAMENTO IDENTITY
    # ==================================================


    def load(self):


        if not os.path.exists(
            self.identity_path
        ):


            self.identity = {}

            return



        try:


            with open(
                self.identity_path,
                "r",
                encoding="utf-8"
            ) as file:


                self.identity = json.load(
                    file
                )



        except Exception as error:


            print(
                "[PERSONA FACTORY] Erro:",
                error
            )


            self.identity = {}








    # ==================================================
    # CRIAÇÃO PRINCIPAL
    # ==================================================


    def create(
        self,
        name
    ):


        name = name.lower()



        personas = self.identity.get(

            "personas",

            {}

        )



        config = personas.get(

            name

        )



        if not config:


            return self.create_default(
                name
            )



        module_path = config.get(

            "module"

        )



        if module_path:


            instance = self.load_module(

                module_path,

                config

            )


            if instance:

                return instance



        return self.create_from_identity(

            name

        )








    # ==================================================
    # CARREGAMENTO DINÂMICO
    # ==================================================


    def load_module(
        self,
        module_path,
        config
    ):


        try:


            module_name, class_name = (

                module_path.rsplit(
                    ".",
                    1
                )

            )



            module = importlib.import_module(

                module_name

            )



            persona_class = getattr(

                module,

                class_name

            )



            return persona_class()



        except Exception as error:


            print(

                "[PERSONA FACTORY] Falha carregando",

                module_path,

                error

            )


            return None







    # ==================================================
    # PERSONA CONFIGURÁVEL
    # ==================================================


    def create_from_identity(
        self,
        name
    ):


        personas = self.identity.get(

            "personas",

            {}

        )



        config = personas.get(

            name,

            {}

        )



        personality = config.get(

            "personality",

            {}

        )



        return Persona(


            name=config.get(

                "name",

                name.upper()

            ),



            role=config.get(

                "role",

                "Agente Genesis"

            ),



            description=config.get(

                "description",

                ""

            ),



            tone=personality.get(

                "tone",

                "neutro"

            ),



            traits=[


                personality.get(

                    "style",

                    ""

                ),



                personality.get(

                    "humor",

                    ""

                )

            ],



            capabilities=config.get(

                "capabilities",

                []

            )

        )








    # ==================================================
    # PADRÃO
    # ==================================================


    def create_default(
        self,
        name
    ):


        return Persona(


            name=name.upper(),


            role="Agente Genesis",


            description=(

                "Personalidade padrão do sistema."

            ),



            tone="neutro",



            traits=[

                "assistente"

            ]

        )








    # ==================================================
    # LISTAGEM
    # ==================================================


    def available(
        self
    ):


        return list(

            self.identity.get(

                "personas",

                {}

            ).keys()

        )








    # ==================================================
    # IDENTIDADE COMPLETA
    # ==================================================


    def get_system_identity(
        self
    ):


        return self.identity.copy()