"""Aussprache-Proben für Fachwörter (ElevenLabs, Stimme Christian, eleven_v4). Aufruf: python3 proben.py"""
import json, os, urllib.request, base64
V = {
 'A_pea_wie_geschrieben': 'Palmitoylethanolamid, kurz PEA.',
 'B_pea_bindestriche': 'Palmito-yl-ethanol-amid, kurz Pe-E-A.',
 'C_pea_uel': 'Palmito-ül-ethanol-amid, kurz Pe-E-A.',
 'D_pea_buchstaben': 'Palmitoyl-ethanolamid, kurz P. E. A.',
 'E_ppar': 'PPAR-alpha, gesprochen Pe-Pe-A-Er-Alpha, und Anandamid.',
}
for k, t in V.items():
    ziel = k + '.mp3'
    if os.path.exists(ziel):
        continue
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/NBqeXKdZHweef6y0B67V?output_format=mp3_44100_128',
        data=json.dumps({'text': t, 'model_id': 'eleven_v4'}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(ziel, 'wb').write(r.read()); print(k, len(t), 'Zeichen, berechnet', r.headers.get('character-cost'))
