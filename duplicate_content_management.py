from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from error_handling import ErrorHandling

error_log = ErrorHandling('duplicate_errors.log')
class DuplicateContentManager:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.summaries = []
        self.vectors = None

    def add_summary(self, summary):
        self.summaries.append(summary)
        self.update_vectors()

    def update_vectors(self):
        self.vectors = self.tfidf_vectorizer.fit_transform(self.summaries)

    def find_similar(self, threshold=0.8):
        similar_pairs = []
        cosine_matrix = cosine_similarity(self.vectors)
        for pair in similar_pairs:
            i, j = pair
            if cosine_matrix[i][j] >= 0.8:
                error_log.log_error(f"Summary {i} and {j}", "Over 80% similarity found")

        return similar_pairs