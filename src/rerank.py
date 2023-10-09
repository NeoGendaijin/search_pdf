from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import faiss
import openai
import os

def make_papers_for_sorting(results):
    papers = []
    for i, paper in enumerate(results['data'], start=1):
        # 各論文の情報としてIDも保存しておく
        papers.append({
            'title_abstract': paper['title'] + ". " + str(paper['abstract']),
            'paperId': paper['paperId']
        })
    return papers

# --- クエリとのマッチングとリランキング ---
def propose_papers(query,papers,openai_api_key, filters=None):
    # --- データの前処理とインデックスの作成 ---
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    embedded_papers = model.encode(papers)

    # FAISSインデックスの作成
    index = faiss.IndexFlatL2(embedded_papers.shape[1])
    index.add(embedded_papers)
    embedded_query = model.encode([query])

    _, indices = index.search(embedded_query, 20)
    top_20_papers = [papers[i] for i in indices[0]]

    top_20_papers = rerank_with_gpt3(input,top_20_papers,openai_api_key)

    return top_20_papers[:8] # return top 8


def score_with_gpt3(input,paper,openai_api_key):
    """
    This function takes a paper (as a string) and returns a score using GPT-3.5-turbo.
    """

    prompt = f""" KEY QUESITON
                    \n
                    {input}
                    \n
                    PAPER ABSTRACT
                    \n
                    {paper}
                    \n
                    \n
                    AGAIN, the answer SHOULD ONLY BE a number form 1 to 30.
                    """

    try:
        # OpenAI API call with GPT-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rate the relevance of the key question and the following paper abstract. The answer should be a number from 1 to 30:"},
                {"role": "user", "content": prompt}
            ],
            api_key=openai_api_key  # APIキーをここで使用
        )

        # Extract and return the score from GPT-3.5-turbo's response
        try:
            score = float(response['choices'][0]['message']['content'].strip())
        except ValueError:
            print("Warning: Could not convert GPT-3.5-turbo response to float. Defaulting score to 0.")
            score = 0.0
        return score

    except Exception as e:
        print(f"Error in scoring paper with GPT-3.5-turbo: {e}")
        return None


def rerank_with_gpt3(input,papers,openai_api_key):
    # Score each paper using GPT-3
    scored_papers = [(paper, score_with_gpt3(input,paper,openai_api_key)) for paper in papers]

    # Remove any papers that couldn't be scored
    scored_papers = [(paper, score) for paper, score in scored_papers if score is not None]

    # Sort papers by score
    scored_papers.sort(key=lambda x: x[1], reverse=True)

    # Return the reranked papers
    return [paper for paper, score in scored_papers]
