import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List

class DataVisualizer:
    def __init__(self):
        sns.set_style("whitegrid")

    def plot_metrics(self, metrics: Dict[str, Any]):
        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(metrics.keys()), y=list(metrics.values()))
        plt.title("Wuneed Metrics")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("wuneed_metrics.png")
        plt.close()

    def plot_command_usage(self, usage: Dict[str, int]):
        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(usage.keys()), y=list(usage.values()))
        plt.title("Command Usage")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("command_usage.png")
        plt.close()

    def plot_feedback_distribution(self, feedback: List[Dict[str, Any]]):
        helpful = sum(1 for item in feedback if item['is_helpful'])
        not_helpful = len(feedback) - helpful
        plt.figure(figsize=(8, 8))
        plt.pie([helpful, not_helpful], labels=['Helpful', 'Not Helpful'], autopct='%1.1f%%')
        plt.title("Feedback Distribution")
        plt.savefig("feedback_distribution.png")
        plt.close()

data_visualizer = DataVisualizer()