"""
=========================================
GENESIS CORE

Arquivo:
core/pipeline/pipeline_context.py

Descrição:
Contexto compartilhado da Pipeline
Cognitiva do Genesis Core.

Responsável por transportar o estado
de uma execução cognitiva entre etapas.

O PipelineContext NÃO cria pensamentos.

Ele transporta um Thought criado pelo
ThoughtEngine e mantém o ambiente da
execução cognitiva.

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.models.thought import (
    Thought
)



class PipelineContext:


    """
    Ambiente temporário da Pipeline.

    Thought:
        Estado cognitivo central.

    Context:
        Dados e histórico da execução.

    PipelineStep:
        Manipula o contexto.
    """



    def __init__(
        self,
        thought: Thought | None = None
    ):


        self.thought = thought


        self.result = None


        self.data = {}


        # COMPONENTES

        self.agent = None

        self.persona = None

        self.memory = None

        self.knowledge = None

        self.tools = []



        # EXECUÇÃO

        self.status = "created"

        self.current_step = None


        self.created_at = datetime.now()

        self.started_at = None

        self.finished_at = None



        # CONTROLE

        self.metadata = {}

        self.history = []

        self.errors = []



    # ==================================================
    # THOUGHT
    # ==================================================


    def set_thought(
        self,
        thought: Thought
    ):


        self.thought = thought

        return self



    def get_thought(
        self
    ):


        return self.thought



    def has_thought(
        self
    ):


        return self.thought is not None



    # ==================================================
    # RESULTADO
    # ==================================================


    def set_result(
        self,
        result
    ):


        self.result = result


        if self.thought:

            self.thought.set_result(
                result
            )


        return self



    def get_result(
        self
    ):


        return self.result



    # ==================================================
    # COMPONENTES
    # ==================================================


    def set_agent(
        self,
        agent
    ):


        self.agent = agent

        return self



    def set_persona(
        self,
        persona
    ):


        self.persona = persona

        return self



    def set_memory(
        self,
        memory
    ):


        self.memory = memory

        return self



    def set_knowledge(
        self,
        knowledge
    ):


        self.knowledge = knowledge

        return self



    def add_tool(
        self,
        tool
    ):


        self.tools.append(
            tool
        )


        return self



    # ==================================================
    # CICLO DO CONTEXTO
    # ==================================================


    def start(
        self
    ):


        self.status = "processing"

        self.started_at = datetime.now()


        self.add_history(
            "pipeline_started"
        )


        return self



    def complete(
        self
    ):


        self.status = "completed"

        self.finished_at = datetime.now()


        self.add_history(
            "pipeline_completed"
        )


        return self



    def fail(
        self,
        error=None
    ):


        self.status = "failed"

        self.finished_at = datetime.now()


        if error:

            self.add_error(
                error
            )


        return self



    def is_completed(
        self
    ):


        return self.status == "completed"



    def is_failed(
        self
    ):


        return self.status == "failed"



    # ==================================================
    # ETAPA ATUAL
    # ==================================================


    def update_step(
        self,
        step_name: str
    ):


        self.current_step = step_name


        self.add_history(

            {

                "event":

                    "step_changed",


                "step":

                    step_name,


                "timestamp":

                    datetime.now()
                    .isoformat()

            }

        )


        return self



    # ==================================================
    # DADOS
    # ==================================================


    def set(
        self,
        key,
        value
    ):


        self.data[key] = value


        return self



    def get(
        self,
        key,
        default=None
    ):


        return self.data.get(
            key,
            default
        )



    def contains(
        self,
        key
    ):


        return key in self.data



    # ==================================================
    # METADATA
    # ==================================================


    def set_metadata(
        self,
        key,
        value
    ):


        self.metadata[key] = value


        return self



    def get_metadata(
        self,
        key,
        default=None
    ):


        return self.metadata.get(
            key,
            default
        )



    # ==================================================
    # HISTÓRICO
    # ==================================================


    def add_history(
        self,
        event
    ):


        if isinstance(
            event,
            str
        ):


            event = {


                "event":

                    event,


                "timestamp":

                    datetime.now()
                    .isoformat()

            }



        self.history.append(
            event
        )



        if self.thought:

            self.thought.add_history(
                event
            )


        return self



    # ==================================================
    # ERROS
    # ==================================================


    def add_error(
        self,
        error
    ):


        self.errors.append(
            error
        )


        self.add_history(

            {

                "event":

                    "error",


                "error":

                    str(error),


                "timestamp":

                    datetime.now()
                    .isoformat()

            }

        )


        return self



    def has_errors(
        self
    ):


        return len(
            self.errors
        ) > 0



    # ==================================================
    # MÉTRICAS
    # ==================================================


    def metrics(
        self
    ):


        duration = None


        if self.started_at and self.finished_at:


            duration = (

                self.finished_at
                -
                self.started_at

            ).total_seconds()



        return {


            "status":

                self.status,


            "current_step":

                self.current_step,


            "history":

                len(
                    self.history
                ),


            "errors":

                len(
                    self.errors
                ),


            "duration":

                duration

        }



    # ==================================================
    # LIMPEZA
    # ==================================================


    def clear(
        self
    ):


        self.data.clear()

        self.metadata.clear()

        self.history.clear()

        self.errors.clear()


        self.current_step = None


        self.result = None


        return self



    # ==================================================
    # SERIALIZAÇÃO
    # ==================================================


    def to_dict(
        self
    ):


        return {


            "thought":

                (

                    self.thought.to_dict()

                    if self.thought

                    else None

                ),


            "result":

                self.result,


            "status":

                self.status,


            "current_step":

                self.current_step,


            "data":

                self.data,


            "metadata":

                self.metadata,


            "history":

                self.history,


            "errors":

                self.errors,


            "metrics":

                self.metrics(),


            "created_at":

                self.created_at.isoformat(),


            "started_at":

                (

                    self.started_at.isoformat()

                    if self.started_at

                    else None

                ),


            "finished_at":

                (

                    self.finished_at.isoformat()

                    if self.finished_at

                    else None

                )

        }



    def summary(
        self
    ):


        return self.to_dict()



    # ==================================================
    # REPRESENTAÇÃO
    # ==================================================


    def __repr__(
        self
    ):


        thought = (

            self.thought.id[:8]

            if self.thought

            else "None"

        )


        return (

            f"PipelineContext("
            f"thought={thought}, "
            f"step={self.current_step}, "
            f"status={self.status}, "
            f"errors={len(self.errors)}"
            f")"

        )