from .get_api_key import get_api_keys
from .query_gen import generate_search_query
from .semantic_scholar import search_papers
from .rerank import make_papers_for_sorting, propose_papers, score_with_gpt3, rerank_with_gpt3
from .download_arXiv import download_from_arxiv_id


def download_relevent_papers(input, save_dir):
    #API keys
    api_keys = get_api_keys("./api_keys.json")
    openai_api_key = api_keys["OPENAI_API_KEY"]
    ss_api_key = api_keys["SEMANTIC_SCHOLAR_API_KEY"]

    fields = "title,authors,abstract,externalIds,paperId"
    search_query = generate_search_query(input, openai_api_key)
    results = search_papers(search_query, offset=10, limit=100, fields=fields, api_key=ss_api_key)
    papers = make_papers_for_sorting(results)
    paper_list_data = propose_papers(input,papers,openai_api_key)

    #downlaod PDF from arXiv
    for i, paper in enumerate(paper_list_data):
        # paper['paperId']を使ってオリジナルのデータから追加情報を取得する
        original_paper_info = next(item for item in results['data'] if item["paperId"] == paper['paperId'])

        if 'externalIds' in original_paper_info:
            if 'ArXiv' in original_paper_info['externalIds']:
                try :
                    print(f"   arxiv : {original_paper_info['externalIds']['ArXiv']}")
                    download_from_arxiv_id(arxiv_id = original_paper_info['externalIds']['ArXiv'], save_dir = save_dir)
                except ValueError:
                    print("No ArXIv info.")
        else:
            print("   DOI information not available.")
