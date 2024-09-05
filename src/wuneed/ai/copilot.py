import openai
from wuneed.config.manager import config_manager
from wuneed.ai.rag.retriever import rag_retriever
from wuneed.utils.cache import smart_cache
from wuneed.utils.advanced_cache import advanced_cache
from typing import List, Dict, Any
from wuneed.utils.snippet_manager import snippet_manager
from wuneed.utils.template_manager import template_manager
from wuneed.utils.metrics_manager import metrics_manager

class AICopilot:
    def __init__(self):
        self.api_key = config_manager.get_active_profile().get('openai_api_key')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in the active profile")
        openai.api_key = self.api_key
        self.feedback_data = []

    def suggest_command(self, user_input: str, plugins: List[str] = [], extensions: List[str] = []) -> str:
        metrics_manager.start_timer("suggest_command")
        
        cache_key = f"suggest_command:{user_input}:{','.join(sorted(plugins))}:{','.join(sorted(extensions))}"
        cached_result = advanced_cache.get(cache_key)
        if cached_result:
            metrics_manager.add_metric("cache_hit", True)
            metrics_manager.end_timer("suggest_command")
            return cached_result

        metrics_manager.add_metric("cache_hit", False)
        
        metrics_manager.start_timer("rag_retrieval")
        retrieval_result = rag_retriever.retrieve(user_input, plugins=plugins, extensions=extensions)
        metrics_manager.end_timer("rag_retrieval")
        
        context_str = "\n".join([c["text"] for c in retrieval_result["processed_context"]])

        # Include snippets and templates in the context
        snippets = snippet_manager.list_snippets()
        templates = template_manager.list_templates()
        context_str += f"\nAvailable snippets: {', '.join(snippets.keys())}"
        context_str += f"\nAvailable templates: {', '.join(templates.keys())}"

        metrics_manager.start_timer("openai_api_call")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful CLI assistant. You can use snippets and templates in your suggestions."},
                {"role": "user", "content": f"Context:\n{context_str}\n\nSuggest a wuneed command for: {user_input}"}
            ]
        )
        metrics_manager.end_timer("openai_api_call")
        
        suggestion = response.choices[0].message["content"].strip()

        # Check if the suggestion uses a template and apply it if necessary
        for template_name in templates.keys():
            if template_name in suggestion:
                suggestion = template_manager.apply_template(template_name, {})  # You might want to parse parameters from the suggestion

        advanced_cache.set(cache_key, suggestion)
        
        metrics_manager.end_timer("suggest_command")
        return suggestion

    def explain_command(self, command: str, plugins: List[str] = []) -> str:
        cached_result = smart_cache.get(f"explain_command:{command}")
        if cached_result:
            return cached_result

        retrieval_result = rag_retriever.retrieve(command, plugins=plugins)
        context_str = "\n".join([c["text"] for c in retrieval_result["processed_context"]])

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful CLI assistant."},
                {"role": "user", "content": f"Context:\n{context_str}\n\nExplain the wuneed command: {command}"}
            ]
        )
        explanation = response.choices[0].message["content"].strip()
        smart_cache.set(f"explain_command:{command}", explanation)
        return explanation

    def generate_code(self, prompt: str) -> str:
        context = rag_retriever.retrieve(prompt)
        full_prompt = f"Context: {context}\n\nTask: {prompt}\n\nGenerate code:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=full_prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def analyze_code(self, code: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Analyze the following code and provide suggestions for improvement:\n\n{code}",
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def generate_test_cases(self, code: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate test cases for the following code:\n\n{code}",
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def provide_feedback(self, query: str, suggestion: str, is_helpful: bool, user_comment: str = ""):
        self.feedback_data.append({
            "query": query,
            "suggestion": suggestion,
            "is_helpful": is_helpful,
            "user_comment": user_comment
        })

    def train_on_feedback(self):
        # This is a placeholder for actual training logic
        # In a real implementation, you would use the feedback_data to fine-tune the model
        print(f"Training on {len(self.feedback_data)} feedback items")
        self.feedback_data = []

    def analyze_security(self, code: str, plugins: List[str] = []) -> List[Dict[str, str]]:
        retrieval_result = rag_retriever.retrieve(code, plugins=plugins)
        security_issues = []
        for plugin_result in retrieval_result["plugin_results"].values():
            for item in plugin_result:
                if "security_issues" in item:
                    security_issues.extend(item["security_issues"])
        
        if not security_issues:
            return [{"type": "info", "description": "No security issues detected."}]
        
        return security_issues

ai_copilot = AICopilot()