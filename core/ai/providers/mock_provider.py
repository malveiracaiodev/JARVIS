"""
=========================================
GENESIS CORE

Arquivo:
core/ai/providers/mock_provider.py

Descrição:
Provider simulado do Genesis Core.

Executa respostas locais sem depender de:

- Ollama
- APIs externas
- Internet
- GPU

Utilizado para validar toda a arquitetura
da camada de Inteligência Artificial.

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from __future__ import annotations

from time import perf_counter
from typing import Any


from core.ai.base.base_provider import BaseProvider

from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse



class MockProvider(BaseProvider):
    """
    Provider local de simulação.

    Representa um LLM falso para testes
    do Genesis Core.
    """



    def __init__(self) -> None:


        super().__init__(

            provider_name="mock",

            model_name="Genesis Simulation",

            version="5.0"

        )


        self.state.provider_name = (
            self.provider_name
        )

        self.state.provider_version = (
            self.version
        )

        self.state.current_model = (
            self.model_name
        )



    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        request: AIRequest | str,
        **kwargs: Any
    ) -> AIResponse:


        start = perf_counter()


        try:


            self.validate_input(
                request
            )


            self.state.register_generation()


            if isinstance(
                request,
                AIRequest
            ):

                prompt = request.prompt

            else:

                prompt = request



            input_tokens = len(
                prompt.split()
            )


            content = self._build_response(
                prompt
            )


            output_tokens = len(
                content.split()
            )


            latency = (
                perf_counter()
                -
                start
            )


            self.register_success(
                latency
            )


            return AIResponse(

                success=True,

                content=content,

                provider=self.provider_name,

                model=self.model_name,

                latency=latency,

                prompt_tokens=input_tokens,

                completion_tokens=output_tokens,

                total_tokens=(
                    input_tokens
                    +
                    output_tokens
                ),

                metadata={

                    "simulation": True,

                    "provider_version":
                        self.version

                }

            )



        except Exception as error:


            latency = (
                perf_counter()
                -
                start
            )


            self.state.register_failure(
                str(error)
            )


            return AIResponse(

                success=False,

                content="",

                provider=self.provider_name,

                model=self.model_name,

                latency=latency,

                error=str(error)

            )



    # =====================================================
    # CHAT
    # =====================================================

    def chat(
        self,
        messages: list[dict],
        **kwargs
    ) -> AIResponse:


        self.state.register_chat()


        if not messages:


            return self.generate(
                ""
            )



        last = messages[-1]


        if isinstance(
            last,
            dict
        ):

            prompt = last.get(
                "content",
                ""
            )

        else:

            prompt = str(last)



        return self.generate(
            prompt
        )



    # =====================================================
    # EMBEDDINGS
    # =====================================================

    def embeddings(
        self,
        text: str
    ) -> list[float]:


        """
        Mock simples de embeddings.

        Futuramente será substituído
        por Ollama/OpenAI/etc.
        """


        self.state.register_embedding()


        size = min(
            len(text),
            10
        )


        return [

            float(
                ord(char)
            )

            for char in text[:size]

        ]



    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def validate_input(
        self,
        request
    ):


        if request is None:

            raise ValueError(
                "Request vazio."
            )


        if isinstance(
            request,
            AIRequest
        ):

            if not request.prompt:

                raise ValueError(
                    "Prompt vazio."
                )


        elif isinstance(
            request,
            str
        ):

            if not request.strip():

                raise ValueError(
                    "Prompt vazio."
                )


        else:

            raise TypeError(
                "Formato de request inválido."
            )



    # =====================================================
    # RESPOSTAS SIMULADAS
    # =====================================================

    def _build_response(
        self,
        prompt: str
    ) -> str:


        text = prompt.lower().strip()



        if any(
            item in text

            for item in [

                "oi",

                "olá",

                "ola",

                "bom dia",

                "boa tarde",

                "boa noite"

            ]

        ):


            return (

                "Olá, Senhor. "
                "Genesis Core operacional. "
                "Todos os sistemas principais "
                "estão funcionando."

            )



        if "quem é você" in text:


            return (

                "Sou JARVIS, núcleo de "
                "inteligência artificial do "
                "Genesis Core."

            )



        if "status" in text:


            return (

                "Genesis Core Status:\n\n"

                "- Kernel: ONLINE\n"

                "- Mind: ONLINE\n"

                "- Thought Engine: ONLINE\n"

                "- AIService: ONLINE\n"

                "- Provider: Genesis Mock"

            )



        if "pipeline" in text:


            return (

                "Pipeline cognitiva ativa:\n"

                "Parser → Planner → Reasoner → "
                "Executor → Reflection → Memory"

            )



        if "rafiki" in text:


            return (

                "Persona Rafiki registrada. "
                "Aguardando conexão com "
                "PersonaManager."

            )



        if "memória" in text or "memoria" in text:


            return (

                "Sistema de memória preparado "
                "para integração com a camada "
                "cognitiva."

            )



        if "ia" in text:


            return (

                "Genesis Mock é uma simulação "
                "local de provider IA. "
                "Providers reais como Ollama, "
                "Gemini ou OpenAI podem assumir "
                "esta função."

            )



        if (
            "teste" in text
            or
            "testar" in text
        ):


            return (

                "Teste executado com sucesso. "
                "Provider Mock respondendo "
                "corretamente."

            )



        return (

            "Genesis Mock recebeu sua mensagem:\n\n"

            f'"{prompt}"'

        )