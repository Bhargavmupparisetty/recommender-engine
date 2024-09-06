from collections import Counter
from itertools import combinations

class RecommenderEngine:
    def __init__(self, transactions):
        self.transactions = transactions

    def analyze_frequent_items(self):
        item_counts = Counter()
        for transaction in self.transactions:
            items = transaction.split(',')  # Assuming items are comma-separated
            item_counts.update(items)
        return item_counts.most_common()

    def analyze_item_pairs(self):
        pairs = []
        for transaction in self.transactions:
            items = transaction.split(',')  # Assuming items are comma-separated
            for pair in combinations(sorted(items), 2):
                pairs.append(pair)
        pair_counts = Counter(pairs)
        return pair_counts.most_common()

    def generate_recommendations(self):
        item_counts = self.analyze_frequent_items()
        pair_counts = self.analyze_item_pairs()

        report = "Recommendations based on the analyzed data:\n\n"
        report += "Most Frequent Items:\n"
        for item, count in item_counts:
            report += f"{item}: {count} times\n"

        report += "\nFrequently Bought Together:\n"
        for (item1, item2), count in pair_counts:
            report += f"{item1} and {item2}: {count} times\n"

        return report
