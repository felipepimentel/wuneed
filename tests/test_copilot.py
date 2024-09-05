import pytest
from unittest.mock import patch, MagicMock
from wuneed.ai.copilot import AICopilot

@pytest.fixture
def mock_openai():
    with patch('wuneed.ai.copilot.openai') as mock:
        yield mock

@pytest.fixture
def mock_config_manager():
    with patch('wuneed.ai.copilot.config_manager') as mock:
        mock.get_active_profile.return_value = {'openai_api_key': 'test_key'}
        yield mock

def test_suggest_command(mock_openai, mock_config_manager):
    mock_openai.Completion.create.return_value.choices[0].text = ' Suggested command'
    copilot = AICopilot()
    result = copilot.suggest_command("Test input")
    assert result == "Suggested command"
    mock_openai.Completion.create.assert_called_once()

def test_explain_command(mock_openai, mock_config_manager):
    mock_openai.Completion.create.return_value.choices[0].text = ' Command explanation'
    copilot = AICopilot()
    result = copilot.explain_command("test command")
    assert result == "Command explanation"
    mock_openai.Completion.create.assert_called_once()

def test_generate_code(mock_openai, mock_config_manager):
    mock_openai.Completion.create.return_value.choices[0].text = ' Generated code'
    copilot = AICopilot()
    with patch('wuneed.ai.copilot.rag_retriever') as mock_retriever:
        mock_retriever.retrieve.return_value = "Context"
        result = copilot.generate_code("Generate a function")
        assert result == "Generated code"
        mock_openai.Completion.create.assert_called_once()