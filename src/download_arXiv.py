import requests
import shutil
import os

def download_from_arxiv_id(arxiv_id, save_dir='../pdfs'):
    # save_dirが存在しない場合、ディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # PDFファイルをダウンロード
    response = requests.get(url, stream=True)

    # ダウンロードが成功したかチェック
    if response.status_code == 200:
        # ファイルに書き込む
        with open(os.path.join(save_dir, f"{arxiv_id}.pdf"), 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"Downloaded {arxiv_id}.pdf to {save_dir}")
    else:
        print(f"Failed to download {arxiv_id}.pdf")
