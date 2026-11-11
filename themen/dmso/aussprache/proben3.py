"""Runde 3 nach Nutzernotiz 11.11. („De-MSO, anders als am Anfang“): Satzanfang mit DMSO klingt wie „Der MSO“."""
import json, os, urllib.request
V = {
 'h1': 'De-Em-Es-O: ein Stoff aus der Papierfabrik, der Zellen beim Einfrieren schützt.',
 'h2': 'De, Em, Es, O: ein Stoff aus der Papierfabrik, der Zellen beim Einfrieren schützt.',
 'h3': 'D M S O: ein Stoff aus der Papierfabrik, der Zellen beim Einfrieren schützt.',
 'z1': 'De-Em-Es-O hat eine erstaunliche Reise hinter sich.',
 'z2': 'De, Em, Es, O hat eine erstaunliche Reise hinter sich.',
 'z3': 'D M S O hat eine erstaunliche Reise hinter sich.',
}
for k, t in V.items():
    if os.path.exists(k + '.mp3'):
        continue
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/NBqeXKdZHweef6y0B67V?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v4'}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(k + '.mp3', 'wb').write(r.read()); print(k, 'berechnet', r.headers.get('character-cost'))
