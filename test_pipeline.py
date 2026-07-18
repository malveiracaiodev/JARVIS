"""
=========================================
GENESIS CORE

Arquivo:
test_pipeline.py

Teste completo da Pipeline Cognitiva.

Arquitetura:
Genesis Core Mark IV
Thought Engine
=========================================
"""


from core.managers.tool_manager import (
    ToolManager
)


from core.pipeline.pipeline_initializer import (
    PipelineInitializer
)


from core.models.thought import (
    Thought
)



# ==================================================
# TOOL MANAGER
# ==================================================


print(
    "\n[BOOT] Inicializando ToolManager..."
)


tool_manager = ToolManager()


tool_manager.initialize()



print(
    "[OK] ToolManager iniciado."
)



# ==================================================
# PIPELINE
# ==================================================


print(
    "\n[BOOT] Construindo Thought Engine..."
)



initializer = PipelineInitializer(

    tool_manager=tool_manager

)



pipeline = initializer.build()



print(
    "[OK] Pipeline criada."
)



# ==================================================
# ETAPAS
# ==================================================


print(
    "\nETAPAS CARREGADAS:"
)



for step in pipeline.list_steps():


    print(
        "-",
        step
    )



# ==================================================
# CRIAÇÃO DO THOUGHT
# ==================================================


message = (

    "Jarvis, teste seu sistema cognitivo"

)



print(
    "\nENTRADA:"
)



print(
    message
)



thought = Thought(

    message=message,

    agent="jarvis",

    source="test"

)



print(
    "\nTHOUGHT CRIADO:"
)



print(
    thought
)



# ==================================================
# EXECUÇÃO COGNITIVA
# ==================================================


context = pipeline.process(

    thought

)



# ==================================================
# RESULTADO GERAL
# ==================================================


print(
    "\n=============================="
)



print(
    "RESUMO FINAL"
)



print(
    "=============================="
)



print(
    context.summary()
)



# ==================================================
# THOUGHT FINAL
# ==================================================


print(
    "\n=============================="
)



print(
    "THOUGHT FINAL"
)



print(
    "=============================="
)



print(
    context.thought.to_dict()
)



# ==================================================
# DADOS INTERNOS
# ==================================================


print(
    "\n=============================="
)



print(
    "DADOS INTERNOS"
)



print(
    "=============================="
)



for key, value in context.data.items():


    print(
        "\n----------------------"
    )


    print(
        key.upper()
    )


    print(
        value
    )



# ==================================================
# HISTÓRICO
# ==================================================


print(
    "\n=============================="
)



print(
    "HISTÓRICO DA PIPELINE"
)



print(
    "=============================="
)



for event in context.history:


    print(
        event
    )



# ==================================================
# STATUS FINAL
# ==================================================


print(
    "\n=============================="
)



print(
    "STATUS"
)



print(
    "=============================="
)



print(

    pipeline.status

)