"""
=========================================
GENESIS CORE

Arquivo:
core/ai/providers/mock_provider.py

Descrição:
Provider simulado oficial do Genesis Core.

Valida:

AIManager
    ↓
AIRequest
    ↓
Provider
    ↓
AIResponse


Não representa inteligência real.

Utilizado para testes arquiteturais.

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
    Provider artificial para testes.
    """



    def __init__(self):

        super().__init__(

            provider_name="mock",

            model_name="Genesis-Mock-LLM",

            version="5.2"

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



            content = self._simulate_generation(
                request
            )



            latency = (
                perf_counter()
                -
                start
            )



            prompt_tokens = len(
                request.prompt.split()
            )


            completion_tokens = len(
                content.split()
            )



            self.register_success(

                latency,

                prompt_tokens,

                completion_tokens

            )



            persona = self._get_persona(
                request
            )



            return AIResponse(

                request_id=request.request_id,


                success=True,


                content=content,


                provider=self.provider_name,


                model=self.model_name,


                persona=persona,


                latency=latency,


                prompt_tokens=prompt_tokens,


                completion_tokens=completion_tokens,


                total_tokens=(

                    prompt_tokens
                    +
                    completion_tokens

                ),



                metadata={

                    "simulation": True,

                    "provider_version":
                        self.version,

                    "architecture":
                        "Genesis Core Mark V"

                }

            )



        except Exception as error:


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
        messages:list[dict],
        **kwargs
    ) -> AIResponse:



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
        text:str
    ) -> list[float]:


        self.state.register_embedding()



        return [

            float(ord(char))

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

            "MockProvider recebeu uma requisição inválida."

        )





    # =====================================================
    # PERSONA
    # =====================================================


    def _get_persona(
        self,
        request:AIRequest
    ) -> str:


        if request.context:


            return request.context.persona



        return "jarvis"





    # =====================================================
    # SIMULAÇÃO COGNITIVA
    # =====================================================


    def _simulate_generation(
        self,
        request:AIRequest
    ) -> str:


        prompt = (

            request.prompt

            .strip()

            .lower()

        )



        persona = self._get_persona(
            request
        )



        persona_name = persona.capitalize()



        if not prompt:


            return (

                "Não recebi nenhuma mensagem "
                "para processar."

            )





        if (
            "quem é você" in prompt
            or
            "quem és tu" in prompt
        ):


            return (

                f"Olá, Caio. "

                f"Eu sou {persona_name}, "

                "uma inteligência simulada "

                "integrada ao Genesis Core. "

                "Estou operando através do "

                "Mock Provider para validar "

                "a arquitetura cognitiva."

            )





        if (
            "olá" in prompt
            or
            "oi" in prompt
        ):


            return (

                f"Olá, Caio. "

                f"{persona_name} online. "

                "Sistemas cognitivos preparados."

            )





        if "status" in prompt:


            return (

                "Genesis Core Status:\n\n"

                "✓ Kernel ONLINE\n"

                "✓ AIService ONLINE\n"

                "✓ AIManager ONLINE\n"

                "✓ Mock Provider ONLINE\n"

                "✓ Thought Engine ONLINE"

            )





        if "teste" in prompt:


            return (

                "Teste concluído com sucesso.\n\n"

                "Fluxo validado:\n"

                "AIManager → AIRequest → "

                "Provider → AIResponse"

            )





        if (
            "ia" in prompt
            or
            "inteligência artificial" in prompt
        ):


            return (

                "Inteligência artificial é uma "

                "área da computação dedicada a "

                "criar sistemas capazes de executar "

                "tarefas que normalmente exigiriam "

                "capacidades humanas como "

                "aprendizado, análise e raciocínio."

            )





        return (

            f"{persona_name} recebeu sua mensagem:\n\n"

            f"{request.prompt}"

        )