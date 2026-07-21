import pytest
from custom_tools import fetch_external_data, process_dataframe_metrics

# Simulação da estrutura do pipeline para fins de testes integrados
class MockToolManager:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, func, description):
        self.tools[name] = {"func": func, "description": description}

    def execute(self, name, params):
        if name in self.tools:
            return self.tools[name]["func"](params)
        raise ValueError(f"Ferramenta {name} não encontrada.")

class CognitivePipelineMock:
    def __init__(self, tool_manager):
        self.tool_manager = tool_manager

    def run(self, prompt: str):
        # Simulação do comportamento do Reasoner/Planner selecionando as novas ferramentas
        executed_tools = []
        if "API externa" in prompt or "dados" in prompt:
            res1 = self.tool_manager.execute("fetch_external_data", {"endpoint": "/api/v1/clients"})
            executed_tools.append("fetch_external_data")
        
        if "métricas" in prompt or "processe" in prompt:
            res2 = self.tool_manager.execute("process_dataframe_metrics", {"dataset": "clients_dataset"})
            executed_tools.append("process_dataframe_metrics")
            
        return {
            "success": True,
            "executed_tools": executed_tools
        }

@pytest.fixture
def configured_pipeline():
    manager = MockToolManager()
    manager.register_tool("fetch_external_data", fetch_external_data, "Busca dados externos.")
    manager.register_tool("process_dataframe_metrics", process_dataframe_metrics, "Processa métricas.")
    return CognitivePipelineMock(manager)

def test_custom_tools_integration(configured_pipeline):
    # Arrange
    prompt = "Busque os dados na API externa de clientes e processe as métricas."
    
    # Act
    result = configured_pipeline.run(prompt)
    
    # Assert
    assert result["success"] is True
    assert "fetch_external_data" in result["executed_tools"]
    assert "process_dataframe_metrics" in result["executed_tools"]