
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        for i in range(len(self.summaries)):
            for j in range(i+1, len(self.summaries)):
                if cosine_matrix[i][j] >= threshold:
                    similar_pairs.append((i, j))
        return similar_pairs
