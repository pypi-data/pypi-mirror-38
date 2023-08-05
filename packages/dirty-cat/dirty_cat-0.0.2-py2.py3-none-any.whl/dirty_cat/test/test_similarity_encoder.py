import numpy as np

from dirty_cat import similarity_encoder, string_distances


def test_similarity_encoder():
    X = np.array(['aa', 'aaa', 'aaab']).reshape(-1, 1)
    X_test = np.array([['Aa', 'aAa', 'aaa', 'aaab', ' aaa  c']]).reshape(-1, 1)

    similarities = [
        'levenshtein-ratio',
        'jaro-winkler',
        'jaro',
        'ngram'
        ]

    for similarity in similarities:
        model = similarity_encoder.SimilarityEncoder(
            similarity=similarity, handle_unknown='ignore')

        encoder = model.fit(X).transform(X_test)

        if similarity == 'levenshtein-ratio':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = string_distances.levenshtein_ratio(x_t, x)
            assert np.array_equal(encoder, ans)

        if similarity == 'jaro-winkler':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = string_distances.jaro_winkler(x_t, x)
            assert np.array_equal(encoder, ans)

        if similarity == 'jaro':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = string_distances.jaro(x_t, x)
            assert np.array_equal(encoder, ans)

        if similarity == 'ngram':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = string_distances.ngram_similarity(x_t, x, 3)
            assert np.array_equal(encoder, ans)
