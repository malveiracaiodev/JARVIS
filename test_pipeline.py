"""
=========================================
GENESIS CORE

Arquivo:
test_pipeline.py

Teste completo da Pipeline Cognitiva.

Arquitetura:
Genesis Core Mark III
=========================================
"""


from core.managers.tool_manager import (
    ToolManager
)


from core.pipeline.pipeline_initializer import (
    PipelineInitializer
)



# ==================================================
# TOOL MANAGER
# ==================================================


print("\n[BOOT] Inicializando ToolManager...")


tool_manager = ToolManager()


tool_manager.initialize()



print(
    "[OK] ToolManager iniciado."
)



# ==================================================
# PIPELINE
# ==================================================


print(
    "\n[BOOT] Construindo Pipeline Cognitiva..."
)


pipeline = PipelineInitializer(
    tool_manager=tool_manager
).build()



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
# PROCESSAMENTO
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



context = pipeline.process(
    message
)



# ==================================================
# RESULTADO GERAL
# ==================================================


print(
    "\nRESUMO:"
)


print(
    context.summary()
)



# ==================================================
# DEBUG COGNITIVO
# ==================================================


print(
    "\nDADOS INTERNOS:"
)


for key, value in context.data.items():


    print(
        "\n======================"
    )


    print(
        key.upper()
    )


    print(
        value
    )