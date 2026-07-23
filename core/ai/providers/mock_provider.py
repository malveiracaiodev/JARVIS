"""
=========================================
GENESIS CORE

Arquivo:
core/ai/providers/mock_provider.py

Descrição:
Provider simulado do Genesis Core.

Modelo artificial local utilizado para
validar a arquitetura de IA sem depender
de modelos externos.

Responsabilidades:

- Simular geração de texto
- Validar pipeline IA
- Testar requests/responses
- Gerar métricas

Não possui:

- Persona
- Identidade
- Memória
- Personalidade

Essas responsabilidades pertencem
ao Genesis.

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
    Simulação de modelo IA.

    Atua como um LLM local falso.
    """



    def __init__(self):

        super().__init__(

            provider_name="mock",

            model_name="Genesis-Mock-LLM",

            version="5.1"

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


            request = self._normalize_request(
                request
            )


            self.validate_request(
                request
            )


            self.state.register_generation()



            prompt = request.prompt



            input_tokens = len(
                prompt.split()
            )



            content = self._simulate_generation(
                request
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

                latency,

                input_tokens,

                output_tokens

            )



            return AIResponse(

                request_id=request.request_id,

                success=True,

                content=content,

                provider=self.provider_name,

                model=self.model_name,

                latency=latency,

                persona=request.persona,

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


            self.register_failure(
                str(error)
            )



            return AIResponse.failure(

                error=str(error),

                provider=self.provider_name,

                model=self.model_name

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
                AIRequest(
                    prompt=""
                )
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

            AIRequest(
                prompt=prompt
            )

        )





    # =====================================================
    # EMBEDDINGS
    # =====================================================


    def embeddings(
        self,
        text: str
    ) -> list[float]:


        self.state.register_embedding()



        return [

            float(
                ord(char)
            )

            for char in text[:10]

        ]





    # =====================================================
    # NORMALIZAÇÃO
    # =====================================================


    def _normalize_request(
        self,
        request
    ) -> AIRequest:


        if isinstance(
            request,
            AIRequest
        ):

            return request



        if isinstance(
            request,
            str
        ):

            return AIRequest(

                prompt=request

            )



        raise TypeError(

            "MockProvider recebeu formato inválido."

        )





    # =====================================================
    # SIMULAÇÃO DO MODELO
    # =====================================================


    def _simulate_generation(
        self,
        request: AIRequest
    ) -> str:


        prompt = (
            request.prompt
            .lower()
            .strip()
        )



        if not prompt:


            return (

                "Não recebi nenhum conteúdo "
                "para processar."

            )



        if "status" in prompt:


            return (

                "Status do processamento:\n\n"

                "- Provider: ONLINE\n"

                "- Modelo: Genesis-Mock-LLM\n"

                "- Processamento: concluído"

            )



        if "teste" in prompt:


            return (

                "Teste concluído com sucesso. "
                "O modelo simulado respondeu "
                "corretamente."

            )



        if "quem é você" in prompt:


            return (

                "Sou um modelo de simulação "
                "integrado ao Genesis Core."

            )



        return (

            "Resposta simulada do modelo:\n\n"

            f"{request.prompt}"

        )