from wuneed.config.user_config import user_config
from wuneed.utils.metrics_manager import metrics_manager
import openai
import json

class ContinuousLearning:
    def __init__(self):
        self.feedback_data = user_config.get('feedback_data', [])
        self.model_version = user_config.get('model_version', '1.0')

    def add_feedback(self, query: str, suggestion: str, is_helpful: bool, user_comment: str):
        self.feedback_data.append({
            'query': query,
            'suggestion': suggestion,
            'is_helpful': is_helpful,
            'user_comment': user_comment
        })
        user_config.set('feedback_data', self.feedback_data)

    def train_model(self):
        if len(self.feedback_data) < 100:
            return "Not enough feedback data for training"

        training_data = [
            {"prompt": f"{item['query']}\n\nSuggestion: {item['suggestion']}",
             "completion": "This suggestion is helpful." if item['is_helpful'] else "This suggestion is not helpful."}
            for item in self.feedback_data
        ]

        response = openai.File.create(
            file=json.dumps(training_data),
            purpose='fine-tune'
        )
        file_id = response.id

        fine_tune_response = openai.FineTune.create(
            training_file=file_id,
            model="davinci"
        )

        self.model_version = fine_tune_response.fine_tuned_model
        user_config.set('model_version', self.model_version)
        metrics_manager.add_metric('model_version', self.model_version)

        return f"Model fine-tuned. New version: {self.model_version}"

continuous_learning = ContinuousLearning()