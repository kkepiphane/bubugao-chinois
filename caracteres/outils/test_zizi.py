"""Test de bout en bout de Zìzì dans Chromium : séance complète avec tracé au doigt simulé,
onglets, lecture, hors-ligne. Usage, depuis caracteres/ :  python3 outils/test_zizi.py"""
import asyncio, functools, http.server, json, os, socketserver, sys, threading
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8798
T = json.load(open(os.path.join(ROOT, 'traits.json'), encoding='utf-8'))

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    socketserver.TCPServer.allow_reuse_address = True
    h = socketserver.TCPServer(('127.0.0.1', PORT), functools.partial(Q, directory=ROOT))
    threading.Thread(target=h.serve_forever, daemon=True).start()

async def draw(pg, c):
    box = await pg.locator('#hw-main svg').first.bounding_box()
    sc = (box['width'] - 28) / 1024
    for med in T[c]['medians']:
        pts = [(box['x'] + 14 + x * sc, box['y'] + 14 + (900 - y) * sc) for x, y in med]
        await pg.mouse.move(*pts[0]); await pg.mouse.down()
        for x, y in pts[1:]: await pg.mouse.move(x, y, steps=4)
        await pg.mouse.up(); await pg.wait_for_timeout(250)

async def main():
    from playwright.async_api import async_playwright
    serve(); fails = []
    def check(ok, msg):
        print('OK   ' if ok else 'ÉCHEC', msg)
        if not ok: fails.append(msg)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(f'http://127.0.0.1:{PORT}/'); await pg.wait_for_timeout(1500)
        check(await pg.evaluate('DATA.chars.length') > 0, 'données chargées')
        check(await pg.evaluate('Object.keys(AUDIO).length') > 0, 'index audio chargé')
        await pg.click('[data-act=daily]'); kinds = []; traces = []
        for _ in range(100):
            st = await pg.evaluate('ui.sess ? (ui.sess.end ? "END" : ui.sess.steps[ui.sess.i].kind + ":" + ui.sess.steps[ui.sess.i].c) : "NO"')
            kinds.append(st.split(':')[0])
            if st in ('END', 'NO'): break
            k, c = st.split(':')
            if k == 'fiche': await pg.wait_for_timeout(200); await pg.click('[data-act=next]'); continue
            if k in ('trace', 'ecrire'):
                await pg.wait_for_timeout(300); await draw(pg, c); await pg.wait_for_timeout(1200)
                traces.append(await pg.evaluate('JSON.stringify(ui.sess.steps[ui.sess.i].res)'))
                await pg.click('[data-act=next]'); continue
            await pg.locator('[data-act=ans]').first.click(); await pg.click('[data-act=next]')
        check(kinds[-1] == 'END', f'séance terminée ({len(kinds) - 1} étapes : {sorted(set(kinds[:-1]))})')
        check(traces and all('"ok":true' in t for t in traces), f'tracé au doigt reconnu ({len(traces)} caractères)')
        await pg.click('[data-act=home]')
        for t in ['mur', 'cles', 'lire', 'home']: await pg.click(f'[data-act=tab][data-k={t}]')
        await pg.click('[data-act=tab][data-k=mur]'); await pg.click('.cell >> nth=0'); await pg.wait_for_timeout(500)
        check(await pg.evaluate('!document.getElementById("sheet").hidden'), 'fiche ouverte depuis le mur')
        await pg.click('[data-act=closesheet] >> nth=0')
        r = await pg.evaluate("""async () => { say(DATA.chars[0].a); await new Promise(r => setTimeout(r, 800)); return curAudio ? (curAudio.error ? 'erreur' : 'mp3') : 'tts'; }""")
        check(r == 'mp3', f'son : {r}')
        await pg.evaluate("DATA.chars.slice(0,40).forEach(x=>{const r=rec(x.c);r.intro=Date.now();SK.forEach(k=>{const s=skState(x.c,k);s.S=3;s.last=Date.now();});});save();ui.tab='lire';render()")
        await pg.click('[data-act=read] >> nth=0'); await pg.click('[data-act=readdone]')
        check(await pg.evaluate('Object.keys(S.read).length') == 1, 'lecture ouverte et marquée lue')
        await pg.wait_for_timeout(1500); await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1000)
        check(await pg.evaluate('!!(typeof DATA !== "undefined" && DATA && DATA.chars.length)'), 'réouverture hors-ligne')
        check(not errs, f'aucune erreur JavaScript {errs[:3]}')
        await b.close()
    print('\n' + ('TOUT EST BON' if not fails else f'{len(fails)} problème(s)')); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    asyncio.run(main())
