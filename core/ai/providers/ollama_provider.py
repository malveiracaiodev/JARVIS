"""
=========================================
GENESIS CORE

Arquivo:
core/ai/providers/ollama_provider.py

Descrição:
Provider oficial de integração com Ollama.

Executa modelos locais através da API
HTTP do Ollama.

Responsável por:

- Comunicação com Ollama
- Geração de respostas
- Chat
- Controle de métricas
- Tratamento de erros

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

import requests


from core.ai.base.base_provider import BaseProvider

from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse



class OllamaProvider(BaseProvider):
    """
    Provider para modelos locais Ollama.
    """



    def __init__(
        self,
        model_name: str = "llama3.2",
        host: str = "http://localhost:11434"
    ) -> None:


        super().__init__(

            provider_name="ollama",

            model_name=model_name,

            version="1.0"

        )


        self.host = host.rstrip("/")



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(self) -> bool:
        """
        Verifica conexão com Ollama.
        """


        try:

            response = requests.get(
                f"{self.host}/api/tags",
                timeout=5
            )


            if response.status_code == 200:

                self.state.initialize()

                self.state.update_metadata(

                    host=self.host,

                    model=self.model_name

                )

                return True



        except Exception as error:

            self.state.last_error = str(error)



        return False



    # =====================================================
    # GENERATE
    # =====================================================


    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:
        """
        Geração simples.
        """


        start = perf_counter()


        try:


            payload = {

                "model":
                    self.model_name,


                "prompt":
                    request.prompt,


                "stream":
                    False,


                "options": {

                    "temperature":
                        request.temperature,

                    "num_predict":
                        request.max_tokens

                }

            }



            response = requests.post(

                f"{self.host}/api/generate",

                json=payload,

                timeout=self.timeout

            )


            response.raise_for_status()


            data = response.json()



            content = data.get(

                "response",

                ""

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

                metadata={

                    "ollama":
                        data

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
        messages: list[dict],
        **kwargs: Any
    ) -> AIResponse:
        """
        Conversação usando histórico.
        """


        start = perf_counter()


        try:


            payload = {

                "model":
                    self.model_name,


                "messages":
                    messages,


                "stream":
                    False

            }



            response = requests.post(

                f"{self.host}/api/chat",

                json=payload,

                timeout=self.timeout

            )


            response.raise_for_status()


            data = response.json()



            content = (

                data

                .get(
                    "message",
                    {}
                )

                .get(
                    "content",
                    ""
                )

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

                metadata={

                    "ollama":
                        data

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
    # EMBEDDINGS
    # =====================================================


    def embeddings(
        self,
        text: str
    ):

        """
        Embeddings via Ollama.

        Necessário modelo compatível.
        """


        payload = {

            "model":
                self.model_name,

            "prompt":
                text

        }


        response = requests.post(

            f"{self.host}/api/embeddings",

            json=payload,

            timeout=self.timeout

        )


        response.raise_for_status()


        return response.json().get(
            "embedding"
        )