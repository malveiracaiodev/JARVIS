"""
=========================================
GENESIS CORE

Arquivo:
core/managers/persona_manager.py

Descrição:
Gerenciador central das Personas.

Responsável por:
- carregar personas dinamicamente
- controlar persona ativa
- fornecer contexto cognitivo
- integrar identidade ao sistema

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from personas.persona_factory import PersonaFactory


class PersonaManager:


    def __init__(
        self,
        logger=None
    ):

        self.logger = logger

        self.factory = PersonaFactory()

        self.personas = {}

        self.active = None

        self.initialized = False



    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(self):


        available = (
            self.factory.available()
        )


        for name in available:


            persona = (
                self.factory.create(name)
            )


            if persona:

                self.personas[name] = persona


                self.log(
                    f"Persona carregada: {persona.name}"
                )



        default = (
            self.factory
            .get_system_identity()
            .get(
                "default_persona",
                "jarvis"
            )
        )


        self.set_persona(
            default
        )


        self.initialized = True


        self.log(
            "Persona Manager ONLINE"
        )



        return True




    def shutdown(self):


        self.active = None

        self.personas.clear()

        self.initialized = False


        self.log(
            "Persona Manager OFFLINE"
        )



    # ==================================================
    # CONTROLE
    # ==================================================


    def set_persona(
        self,
        name
    ):


        name = (
            name.lower()
            .strip()
        )


        persona = (
            self.personas.get(name)
        )


        if not persona:

            raise ValueError(
                f"Persona inexistente: {name}"
            )


        self.active = persona


        self.log(
            f"Persona ativa: {persona.name}"
        )



        return persona




    def get_active(self):

        return self.active




    def current_name(self):


        if not self.active:

            return None


        return self.active.name




    # ==================================================
    # CONTEXTO COGNITIVO
    # ==================================================


    def context(
        self,
        message
    ):


        if not self.active:

            return {}


        return (
            self.active
            .build_context(message)
        )



    # ==================================================
    # CONSULTAS
    # ==================================================


    def list_personas(self):

        return list(
            self.personas.keys()
        )



    def status(self):


        return {


            "online":
                self.initialized,


            "active":
                self.current_name(),


            "available":
                self.list_personas()


        }




    # ==================================================
    # LOG
    # ==================================================


    def log(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )

        else:

            print(
                f"[PERSONA] {message}"
            )