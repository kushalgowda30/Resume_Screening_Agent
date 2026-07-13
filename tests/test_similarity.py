from src.similarity import calculate_similarity

def test_similarity():
    jd = "Python SQL Machine Learning"
    resume = "Python SQL"

    score = calculate_similarity(resume, jd)

    assert score >= 0