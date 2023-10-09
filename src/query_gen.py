import openai

def generate_search_query(input_text,openai_api_key):
    """
    GPT-3.5-turboを使用して、ユーザーの入力テキストから検索クエリを生成します。

    :param input_text: str, ユーザーからの入力テキスト
    :return: str, 生成された検索クエリ
    """
    openai.api_key = openai_api_key

    try:
        # GPT-3.5-turbo APIをコールします。
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests keyword. You have to think of a word to search papers. DO NOT ANSWER IN SENTENCE. ANSWER IN WORDs. ONE ANSWER ONLY."},
                {"role": "user", "content": input_text}
            ]
        )

        # レスポンスからコンテンツを抽出し、返します。
        message_content = response['choices'][0]['message']['content']
        return message_content.strip()

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
