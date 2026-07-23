"""
=========================================
GENESIS CORE

Arquivo:
core/ai/providers/ollama_provider.py

Descrição:
Provider oficial Ollama.

Integra modelos locais através
da API HTTP do Ollama.

Responsabilidades:

- Comunicação HTTP
- Geração
- Chat
- Embeddings
- Métricas
- Diagnóstico

Não controla:

- Persona
- Memória
- Identidade

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


from core.ai.exceptions import (
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderGenerationError,
    EmbeddingError
)





class OllamaProvider(BaseProvider):


    def __init__(
        self,
        model_name: str = "llama3.2",
        host: str = "http://localhost:11434"
    ):


        super().__init__(

            provider_name="ollama",

            model_name=model_name,

            version="5.0"

        )


        self.host = host.rstrip("/")


        self.timeout = 120





    # =====================================================
    # INIT
    # =====================================================


    def initialize(self) -> bool:


        try:


            response = requests.get(

                f"{self.host}/api/tags",

                timeout=5

            )


            response.raise_for_status()



            self.state.initialize(

                provider_name=self.provider_name,

                provider_version=self.version,

                model=self.model_name

            )


            self.state.metadata.update({

                "host": self.host

            })


            return True



        except requests.Timeout as error:


            raise ProviderTimeoutError(

                str(error)

            )



        except requests.RequestException as error:


            raise ProviderConnectionError(

                f"Ollama offline: {error}"

            )







    # =====================================================
    # GENERATE
    # =====================================================


    def generate(
        self,
        request: AIRequest,
        **kwargs:Any
    ) -> AIResponse:


        start = perf_counter()



        try:


            self.validate_request(
                request
            )



            payload = {


                "model":

                    request.model
                    or
                    self.model_name,


                "prompt":

                    request.prompt,


                "stream":

                    False,


                "options":

                {

                    "temperature":

                        request.temperature,


                    "top_p":

                        request.top_p,


                    "num_predict":

                        request.max_tokens

                }

            }





            if request.system_prompt:


                payload["system"] = request.system_prompt





            elif request.context:


                payload["system"] = (

                    f"Você é {request.context.persona}. "

                    "Responda como assistente do Genesis Core."

                )





            response = requests.post(

                f"{self.host}/api/generate",

                json=payload,

                timeout=self.timeout

            )



            response.raise_for_status()



            data=response.json()



            content=data.get(

                "response",

                ""

            )



            if not content.strip():


                raise ProviderGenerationError(

                    "Ollama retornou resposta vazia."

                )



            latency=(

                perf_counter()

                -
                start

            )



            self.register_success(

                latency

            )



            return AIResponse(

                request_id=request.request_id,


                success=True,


                content=content,


                provider=self.provider_name,


                model=payload["model"],


                persona=request.persona,


                latency=latency,


                metadata={

                    "ollama":data

                }

            )




        except requests.Timeout:


            self.register_failure(
                "timeout"
            )


            raise ProviderTimeoutError(

                "Ollama excedeu tempo limite."

            )



        except requests.RequestException as error:


            self.register_failure(

                str(error)

            )


            raise ProviderConnectionError(

                str(error)

            )



        except Exception as error:


            self.register_failure(

                str(error)

            )


            raise ProviderGenerationError(

                str(error)

            )







    # =====================================================
    # CHAT
    # =====================================================


    def chat(
        self,
        messages:list[dict],
        **kwargs
    ) -> AIResponse:



        start=perf_counter()



        try:


            payload={


                "model":

                    kwargs.get(

                        "model",

                        self.model_name

                    ),


                "messages":

                    messages,


                "stream":

                    False

            }



            response=requests.post(

                f"{self.host}/api/chat",

                json=payload,

                timeout=self.timeout

            )


            response.raise_for_status()



            data=response.json()



            content=(

                data.get(

                    "message",

                    {}

                )
                .get(

                    "content",

                    ""

                )

            )



            if not content.strip():

                raise ProviderGenerationError(

                    "Resposta vazia."

                )



            latency=(

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

                model=payload["model"],

                latency=latency,

                metadata={

                    "ollama":data

                }

            )




        except Exception as error:


            self.register_failure(

                str(error)

            )


            raise ProviderGenerationError(

                str(error)

            )






    # =====================================================
    # EMBEDDINGS
    # =====================================================


    def embeddings(
        self,
        text:str
    ):


        try:


            response=requests.post(

                f"{self.host}/api/embeddings",

                json={

                    "model":

                        self.model_name,

                    "prompt":

                        text

                },

                timeout=self.timeout

            )



            response.raise_for_status()



            data=response.json()



            self.state.register_embedding()



            return data.get(

                "embedding",

                []

            )



        except Exception as error:


            raise EmbeddingError(

                str(error)

            )