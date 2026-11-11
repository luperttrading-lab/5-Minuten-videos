"""Aussprache-Proben (ElevenLabs, Christian, eleven_v4). f = „L-Theanin“, j = japanische Wörter. Aufruf: python3 proben.py"""
import json, os, urllib.request
V = {
 'f1': 'L-Theanin: ein Stoff aus grünem Tee. Sakato nannte ihn Theanin.',
 'f2': 'El-Te-anihn: ein Stoff aus grünem Tee. Sakato nannte ihn Te-anihn.',
 'f3': 'El Teh-a-nihn: ein Stoff aus grünem Tee. Sakato nannte ihn Teh-a-nihn.',
 'f4': 'L. Theanien: ein Stoff aus grünem Tee. Sakato nannte ihn Theanien.',
 'j1': 'In der Teestadt Uji untersuchte Yajiro Sakato den Schattentee Gyokuro. Auch Matcha wird beschattet. Der Geschmack heißt Umami.',
 'j2': 'In der Teestadt Udschi untersuchte Jadschiro Sakato den Schattentee Gjokuro. Auch Mattscha wird beschattet. Der Geschmack heißt Umami.',
}
for k, t in V.items():
    if os.path.exists(k + '.mp3'):
        continue
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/NBqeXKdZHweef6y0B67V?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v4'}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(k + '.mp3', 'wb').write(r.read()); print(k, len(t), 'Zeichen, berechnet', r.headers.get('character-cost'))
