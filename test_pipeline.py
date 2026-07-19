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


from core.cognitive.thought_engine import (
    ThoughtEngine
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
# CONSTRUÇÃO DA PIPELINE
# ==================================================


print(
    "\n[BOOT] Construindo Pipeline Cognitiva..."
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
# THOUGHT ENGINE
# ==================================================


print(
    "\n[BOOT] Inicializando Thought Engine..."
)



engine = ThoughtEngine(

    pipeline=pipeline

)



print(
    "[OK] Thought Engine pronta."
)



# ==================================================
# ENTRADA
# ==================================================


message = (

    "Jarvis, execute um teste do sistema cognitivo"

)



print(
    "\nENTRADA:"
)



print(
    message
)



# ==================================================
# EXECUÇÃO DO CICLO
# ==================================================


thought = engine.think(

    message,

    agent="jarvis",

    source="test_pipeline"

)



# ==================================================
# RESULTADO FINAL
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

    thought.to_dict()

)



# ==================================================
# RESULTADO DA PIPELINE
# ==================================================


print(
    "\n=============================="
)


print(
    "RESULTADO PIPELINE"
)


print(
    "=============================="
)



if thought.result:


    print(
        thought.result
    )


else:


    print(
        "Nenhum resultado."
    )



# ==================================================
# HISTÓRICO
# ==================================================


print(
    "\n=============================="
)


print(
    "HISTÓRICO PIPELINE"
)


print(
    "=============================="
)



for event in pipeline.get_history():


    print(
        event
    )



# ==================================================
# MÉTRICAS ENGINE
# ==================================================


print(
    "\n=============================="
)


print(
    "MÉTRICAS THOUGHT ENGINE"
)


print(
    "=============================="
)



print(

    engine.metrics()

)



# ==================================================
# STATUS PIPELINE
# ==================================================


print(
    "\n=============================="
)


print(
    "STATUS PIPELINE"
)


print(
    "=============================="
)



print(

    pipeline.status()

)



# ==================================================
# STATUS ENGINE
# ==================================================


print(
    "\n=============================="
)


print(
    "STATUS ENGINE"
)


print(
    "=============================="
)



print(

    engine.status()

)



print(
    "\n[FINALIZADO] Teste cognitivo concluído."
)