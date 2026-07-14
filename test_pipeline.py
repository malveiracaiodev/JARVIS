from core.pipeline.pipeline_initializer import PipelineInitializer



pipeline = PipelineInitializer().build()



print(
    "ETAPAS:"
)

print(
    pipeline.list_steps()
)



context = pipeline.process(
    "Jarvis, teste seu sistema cognitivo"
)



print(
    "\nRESUMO:"
)

print(
    context.summary()
)