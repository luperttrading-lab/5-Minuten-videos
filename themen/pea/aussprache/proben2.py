"""Zweite Runde Aussprache-Proben nach Nutzernotiz 09.11., 23:52: „pal-mi-toil-e-ta-no-la-miit“, Betonung auf -miid (lang)."""
import json, os, urllib.request
V = {
 'F1': '1957 stellten sie ihn vor: Palmitoil-ethanolamiet, kurz Pe-E-A.',
 'F2': '1957 stellten sie ihn vor: Palmitoil-etanola-miet, kurz Pe-E-A.',
 'F3': '1957 stellten sie ihn vor: Pal-mi-toil-e-ta-no-la-miet, kurz Pe-E-A.',
 'F4': '1957 stellten sie ihn vor: Palmitoyl-ethanolamíd, kurz Pe-E-A.',
}
for k, t in V.items():
    if os.path.exists(k + '.mp3'):
        continue
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/NBqeXKdZHweef6y0B67V?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v4'}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(k + '.mp3', 'wb').write(r.read()); print(k, 'berechnet', r.headers.get('character-cost'))
