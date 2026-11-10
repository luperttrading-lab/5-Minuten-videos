"""Aussprache-Proben für Fachwörter (ElevenLabs, Stimme Christian, eleven_v4). Aufruf: python3 proben.py"""
import json, os, urllib.request
V = {
 'f1': 'Sein voller Name ist Dimethylsulfoxid, kurz DMSO.',
 'f2': 'Sein voller Name ist Di-methyl-sulf-oxid, kurz De Em Es O.',
 'f3': 'Sein voller Name ist Dimethül-sulfoxiet, kurz De-Em-Es-O.',
 'f4': 'Sein voller Name ist Dimethyl-sulfoxid, kurz D. M. S. O.',
}
for k, t in V.items():
    if os.path.exists(k + '.mp3'):
        continue
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/NBqeXKdZHweef6y0B67V?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v4'}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(k + '.mp3', 'wb').write(r.read()); print(k, len(t), 'Zeichen, berechnet', r.headers.get('character-cost'))
