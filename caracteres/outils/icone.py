"""Dessine le logo de Zìzì (icon-192.png, icon-512.png) à partir des traits de 字 dans traits.json.

Feuille crème posée sur le bleu de l'appli, grille 米字格 en pointillés, 字 à l'encre avec sa clé 宀 en rouge
(comme dans les fiches). Tout le dessin tient dans la zone sûre des icônes « maskable » (cercle de 80 %),
pour qu'Android ne coupe rien, quelle que soit la forme de l'icône sur le téléphone.

Usage, depuis caracteres/ :  python3 outils/icone.py      (Google Chrome ou Chromium requis)
"""
import json, os, shutil, subprocess, tempfile

BLEU, CREME, ENCRE, ROUGE, GRILLE = '#2B4C9B', '#FBF6EC', '#1F2A44', '#D9453B', '#E8A99A'
CLE = 3  # les 3 premiers traits de 字 forment la clé 宀


def svg(taille):
    traits = json.load(open('traits.json', encoding='utf-8'))['字']['strokes']
    c, cote, r = 256, 290, 40          # feuille de 290 px centrée : coins dans la zone sûre (rayon 205)
    x0 = c - cote / 2
    pas = 8
    grille = (f'<g stroke="{GRILLE}" stroke-width="5" stroke-dasharray="14 10" fill="none">'
              f'<path d="M{x0+pas} {c}H{x0+cote-pas}M{c} {x0+pas}V{x0+cote-pas}'
              f'M{x0+pas+34} {x0+pas+34}L{x0+cote-pas-34} {x0+cote-pas-34}'
              f'M{x0+cote-pas-34} {x0+pas+34}L{x0+pas+34} {x0+cote-pas-34}"/></g>')
    # Make Me a Hanzi : boîte de 1024, axe y vers le haut → on retourne et on réduit à la feuille.
    k = (cote - 40) / 1024
    car = ''.join(f'<path d="{d}" fill="{ROUGE if i < CLE else ENCRE}"/>' for i, d in enumerate(traits))
    car = f'<g transform="translate({x0+20} {x0+20+900*k}) scale({k} {-k})">{car}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{taille}" height="{taille}" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" fill="{BLEU}"/>'
            f'<rect x="{x0}" y="{x0+6}" width="{cote}" height="{cote}" rx="{r}" fill="#000" opacity=".18"/>'
            f'<rect x="{x0}" y="{x0}" width="{cote}" height="{cote}" rx="{r}" fill="{CREME}"/>'
            f'{grille}{car}</svg>')


def main():
    chrome = next((shutil.which(n) for n in ('google-chrome', 'chromium', 'chromium-browser') if shutil.which(n)), None)
    if not chrome:
        raise SystemExit('Il faut Google Chrome ou Chromium pour dessiner les PNG.')
    with tempfile.TemporaryDirectory() as tmp:
        for taille in (192, 512):
            page = os.path.join(tmp, f'i{taille}.html')
            open(page, 'w', encoding='utf-8').write(
                f'<!doctype html><style>html,body{{margin:0;overflow:hidden}}svg{{display:block}}</style>{svg(taille)}')
            sortie = os.path.abspath(f'icon-{taille}.png')
            subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
                            '--force-device-scale-factor=1', f'--window-size={taille},{taille}',
                            f'--screenshot={sortie}', 'file://' + page], check=True, capture_output=True)
            print('écrit', sortie)


if __name__ == '__main__':
    main()
