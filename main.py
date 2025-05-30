from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

openai.api_key = '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'
SERP_API_KEY = 'f15ac20a4fb3969424e81105797343c1da16a122003ab6b6ccb395463b9444ef'

@app.route('/')
def home():
    return "API Cek Fakta Online. Gunakan endpoint POST /cek-fakta"

@app.route('/cek-fakta', methods=['POST'])
def cek_fakta():
    klaim = request.json.get('claim')

    params = {
        'q': klaim,
        'api_key': SERP_API_KEY,
        'engine': 'google',
        'hl': 'id',
        'gl': 'id',
        'num': 3
    }

    serp_response = requests.get('https://serpapi.com/search.json', params=params).json()
    hasil_snippet = []

    for result in serp_response.get('organic_results', [])[:3]:
        judul = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        if judul and snippet:
            hasil_snippet.append(f"{judul}\n{snippet}\n{link}")

    sumber_text = '\n\n'.join(hasil_snippet)

    prompt = f"""
Klaim: \"{klaim}\"

Berikut hasil pencarian dari internet:
{sumber_text}

Verifikasi apakah klaim ini BENAR atau SALAH berdasarkan sumber di atas.

✅ Status Klaim: (Benar / Salah / Tidak Diketahui)  
🧠 Penjelasan: (bahasa mudah, max 3 paragraf)  
📚 Sumber: (sebutkan nama artikel & link)
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    jawaban = response['choices'][0]['message']['content']
    return jsonify({"hasil": jawaban})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
