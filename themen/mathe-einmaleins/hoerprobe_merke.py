"""Hörprobe für den Merke-Teil in einer Textfassung: Ton (ElevenLabs, Cache), aufbereitet wie im Video, Bild wie im
Video; geschnitten auf den Merke-Teil. Aufruf: python3 hoerprobe_merke.py <fassung> <ziel.mp4>"""
import sys, os, subprocess, wave
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, '/home/user/5-Minuten-videos/themen/mathe-einmaleins')
os.chdir('/home/user/5-Minuten-videos/themen/mathe-einmaleins')
import regel as G
from PIL import Image

FASSUNGEN = {
    'ziffer': ('Merk dir die drei Schritte: Eine Einerziffer zur anderen Zahl addieren, egal, welche. Eine Null anhängen. '
               'Beide Einerziffern multiplizieren und dazuzählen. Und jetzt du: dreizehn mal vierzehn.',
               [('1', G.CB, ['Eine Einerziffer zur anderen', 'Zahl addieren – egal, welche'], 'Eine Einerziffer'),
                ('2', G.TEAL, ['Eine Null anhängen'], 'Eine Null'),
                ('3', G.CD, ['Beide Einerziffern', 'multiplizieren und dazuzählen'], 'Beide Einerziffern')]),
    'aktuell': (next(x for x in G.SZENEN if x['id'] == 'merke')['text'], list(G.MERKSAETZE)),
    'den': ('Merk dir die drei Schritte: Den Einer zur anderen Zahl dazuzählen, egal, welchen. Eine Null anhängen. '
            'Die beiden Einer malnehmen und dazuzählen. Und jetzt du: dreizehn mal vierzehn.',
            [('1', G.CB, ['Den Einer zur anderen Zahl', 'dazuzählen – egal, welchen'], 'Den Einer'),
             ('2', G.TEAL, ['Eine Null anhängen'], 'Eine Null'),
             ('3', G.CD, ['Die beiden Einer malnehmen', 'und dazuzählen'], 'Die beiden')]),
}
name, ziel = sys.argv[1], sys.argv[2]
text, saetze = FASSUNGEN[name]
m = next(s for s in G.SZENEN if s['id'] == 'merke')
m['text'] = text
G.MERKSAETZE[:] = saetze


def frames(arg):
    k0, k1, pfad = arg
    G.ton_und_zeitplan()                                   # Zeitplan je Prozess (Ton liegt dann im Cache)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-r', '30',
                           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p', pfad],
                          stdin=subprocess.PIPE)
    for k in range(k0, k1):
        ff.stdin.write(G.bild(k / 30).resize((1280, 720), Image.LANCZOS).tobytes())
    ff.stdin.close(); ff.wait()
    return pfad


if __name__ == '__main__':
    voll = ziel.replace('.mp4', '_voll.mp4')
    sys.argv = ['regel.py', voll, '--nur-ton']
    G.main()                                               # erzeugt ..._voll.wav (aufbereitet, entknackst, mit Geräuschen)
    m = next(s for s in G.SZENEN if s['id'] == 'merke')
    t0, t1 = m['start'] - 0.3, m['start'] + m['dauer'] + G.DENKPAUSE   # mit Denkpause und Lösung
    a, b = int(t0 * 30), int(t1 * 30)
    g = [a + (b - a) * i // 4 for i in range(5)]
    with Pool(4) as pool:
        teile = pool.map(frames, [(g[i], g[i + 1], ziel.replace('.mp4', f'_t{i}.mp4')) for i in range(4)])
    liste = ziel.replace('.mp4', '_l.txt')
    open(liste, 'w').writelines(f"file '{q}'\n" for q in teile)
    wav = voll.replace('.mp4', '.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', liste, '-ss', f'{a / 30:.3f}', '-t',
                    f'{(b - a) / 30:.3f}', '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', ziel], check=True)
    for q in teile + [liste]:
        os.remove(q)
    print('fertig', ziel, f'{(b - a) / 30:.1f} s')
