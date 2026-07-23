"""
=========================================
GENESIS CORE

Arquivo:
personas/persona_factory.py

Descrição:

Factory dinâmica de Personas.

Responsável por:

- Carregar identity.json
- Resolver classes dinamicamente
- Injetar configuração
- Criar personas customizadas
- Suportar plugins futuros

Arquitetura:

Identity
   |
   ↓
PersonaFactory
   |
   ↓
Dynamic Loader
   |
   ├── Jarvis
   ├── Rafiki
   └── Custom Personas


Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from __future__ import annotations


import json
import os
import importlib



from personas.persona import Persona





class PersonaFactory:


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
    # LOAD IDENTITY
    # ==================================================


    def load(self):


        if not os.path.exists(
            self.identity_path
        ):

            print(
                "[PERSONA FACTORY] Identity não encontrado."
            )

            return



        try:


            with open(
                self.identity_path,
                "r",
                encoding="utf-8"
            ) as file:


                self.identity = json.load(file)



        except Exception as error:


            print(

                "[PERSONA FACTORY] Erro:",
                error

            )

            self.identity = {}





    # ==================================================
    # CREATE
    # ==================================================


    def create(
        self,
        name=None
    ):


        if not name:


            name = self.identity.get(

                "default_persona",

                "jarvis"

            )



        name = name.lower().strip()



        config = (

            self.identity

            .get(
                "personas",
                {}
            )

            .get(
                name
            )

        )



        if not config:


            return self.create_default(
                name
            )



        module = config.get(
            "module"
        )



        if module:


            instance = self.load_module(

                module,

                config

            )


            if instance:


                return instance



        return self.create_from_identity(

            name

        )





    # ==================================================
    # DYNAMIC LOADER
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



            persona = persona_class()



            self.apply_config(

                persona,

                config

            )



            return persona



        except Exception as error:


            print(

                "[PERSONA FACTORY] Falha:",
                module_path,
                error

            )


            return None





    # ==================================================
    # INJETAR CONFIGURAÇÃO
    # ==================================================


    def apply_config(
        self,
        persona,
        config
    ):


        personality = config.get(

            "personality",

            {}

        )


        persona.name = config.get(

            "name",

            persona.name

        )


        persona.role = config.get(

            "role",

            persona.role

        )


        persona.description = config.get(

            "description",

            persona.description

        )


        persona.tone = personality.get(

            "tone",

            persona.tone

        )


        persona.traits = [


            personality.get(

                "style",

                ""

            ),


            personality.get(

                "humor",

                ""

            )

        ]



        persona.capabilities = config.get(

            "capabilities",

            persona.capabilities

        )


        persona.system_prompt = config.get(

            "system_prompt",

            getattr(
                persona,
                "system_prompt",
                ""
            )

        )


        persona.metadata = config.get(

            "metadata",

            {

                "version": "1.0",

                "type": "persona"

            }

        )


        return persona





    # ==================================================
    # GENERIC PERSONA
    # ==================================================


    def create_from_identity(
        self,
        name
    ):


        config = (

            self.identity

            .get(
                "personas",
                {}
            )

            .get(
                name,
                {}
            )

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

            ),


            system_prompt=config.get(

                "system_prompt",

                ""

            ),


            metadata=config.get(

                "metadata",

                {}

            )

        )





    # ==================================================
    # DEFAULT
    # ==================================================


    def create_default(
        self,
        name
    ):


        return Persona(


            name=name.upper(),


            role="Agente Genesis",


            description="Persona padrão do sistema.",


            tone="neutro",


            traits=[

                "assistente"

            ]

        )





    # ==================================================
    # LIST
    # ==================================================


    def available(self):


        return list(

            self.identity

            .get(
                "personas",
                {}
            )

            .keys()

        )





    # ==================================================
    # SYSTEM IDENTITY
    # ==================================================


    def get_system_identity(
        self
    ):


        return self.identity.copy()