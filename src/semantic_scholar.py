import requests

def search_papers(query, offset=0, limit=100, fields=None, api_key=None):
    # APIのエンドポイントURL
    api_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # クエリパラメータを設定
    params = {
        "query": query,
        "offset": offset,
        "limit": limit,
        "fields": fields
    }

    # ヘッダーを設定
    headers = {}
    if api_key:
        headers['x-api-key'] = api_key

    # APIリクエストを送信
    response = requests.get(api_url, params=params, headers=headers)

    # レスポンスをチェック
    if response.status_code == 200:
        # JSON形式で結果をパース
        results = response.json()
        return results
    else:
        print(f"Failed to fetch results with status code {response.status_code}")
        return None
