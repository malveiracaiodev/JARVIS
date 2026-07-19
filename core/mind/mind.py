"""
=========================================
GENESIS CORE

Arquivo:
core/mind/mind.py

Descrição:
Centro cognitivo principal do Genesis Core.

Responsável por:

- Receber entradas do usuário
- Criar Thoughts
- Acionar Thought Engine
- Coordenar Pipeline Cognitiva
- Gerenciar estado mental

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.base.module import Module

from core.models.thought import Thought



class Mind(Module):
    """
    Controlador cognitivo principal.

    O Mind não raciocina.

    Ele cria Thoughts e entrega
    para a Thought Engine.
    """



    def __init__(
        self,
        tool_manager=None,
        logger=None,
        event_bus=None,
        config=None,
        identity=None,
        service_manager=None,
        runtime=None,
        engine=None,
        pipeline=None,
    ):


        super().__init__(
            "mind"
        )



        # ==================================================
        # DEPENDÊNCIAS
        # ==================================================

        self.tool_manager = tool_manager

        self.logger = logger

        self.event_bus = event_bus

        self.config = config

        self.identity = identity

        self.service_manager = service_manager


        self.runtime = runtime or engine


        self.pipeline = pipeline



        # ==================================================
        # ESTADO
        # ==================================================

        self.last_thought = None

        self.history = []



    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(
        self
    ):


        self.log(
            "Mind iniciando."
        )


        self.status = "ONLINE"



        if self.event_bus:

            self.event_bus.emit(

                "mind.started",

                {
                    "time":
                    datetime.now().isoformat()
                }

            )


        self.log(
            "Mind ONLINE."
        )



    def shutdown(
        self
    ):


        self.log(
            "Mind OFFLINE."
        )


        self.status = "OFFLINE"



    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================


    def think(
        self,
        text
    ):


        try:


            if not self.pipeline:

                return (
                    "Pipeline cognitiva indisponível."
                )



            #
            # Criação do Thought
            #

            thought = Thought(

                message=text,

                metadata={

                    "identity":
                        self.identity,

                    "history_size":
                        len(self.history),

                    "created_by":
                        "mind",

                    "received_at":
                        datetime.now().isoformat()

                }

            )



            self.last_thought = thought



            thought.processing()



            thought.add_history(
                "thought_created"
            )



            #
            # Execução da Thought Engine
            #

            if hasattr(
                self.pipeline,
                "process"
            ):


                result = self.pipeline.process(
                    thought
                )


            elif hasattr(
                self.pipeline,
                "run"
            ):


                result = self.pipeline.run(
                    thought
                )


            elif hasattr(
                self.pipeline,
                "execute"
            ):


                result = self.pipeline.execute(
                    thought
                )


            else:


                raise RuntimeError(

                    "Pipeline sem método de execução."

                )



            #
            # Guarda resultado
            #

            thought.set_result(
                result
            )



            if not thought.is_finished():

                thought.completed()



            thought.add_history(
                "thought_finished"
            )



            self.history.append(

                {

                    "thought_id":
                        thought.id,

                    "input":
                        text,

                    "status":
                        thought.status,

                    "confidence":
                        thought.confidence,

                    "execution_time":
                        thought.execution_time,

                    "time":
                        datetime.now().isoformat()

                }

            )



            return result



        except Exception as error:



            if self.last_thought:


                try:

                    self.last_thought.failed()

                    self.last_thought.set_metadata(

                        "exception",

                        str(error)

                    )


                except Exception:

                    pass



            if self.logger:

                self.logger.error(

                    f"Erro cognitivo: {error}"

                )



            return (

                f"[FALHA COGNITIVA]: {error}"

            )



    # ==================================================
    # STATUS
    # ==================================================


    def get_brain_status(
        self
    ):


        return {


            "name":
                "Genesis Mind",


            "status":
                self.status,


            "pipeline":
                self.pipeline is not None,


            "thoughts":
                len(self.history),


            "last_thought":

                (

                    self.last_thought.id

                    if self.last_thought

                    else None

                )

        }



    # ==================================================
    # APRENDIZADO
    # ==================================================


    def learn(
        self,
        data
    ):


        self.log(
            "Novo conhecimento recebido."
        )


        return True



    # ==================================================
    # RESET
    # ==================================================


    def reset(
        self
    ):


        self.last_thought = None

        self.history.clear()


        return True



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
                "[MIND]",
                message
            )