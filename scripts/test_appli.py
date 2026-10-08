"""Test de bout en bout de l'appli dans un vrai navigateur (Chromium via Playwright).

Ce qu'il vérifie :
  1. l'appli démarre, charge les chapitres de packs/ et l'index audio
  2. trois séances du jour complètes (tous les types d'exercices), sans erreur JavaScript
  3. la lecture d'un son, l'analyse de tons sur un enregistrement natif
  4. le test HSK blanc
  5. la réouverture hors-ligne (service worker)

Usage :  python3 scripts/test_appli.py        (depuis la racine du dépôt)
Prérequis : pip install playwright  &&  playwright install chromium
"""
import asyncio, functools, http.server, os, socketserver, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8799


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


async def run_session(pg):
    kinds = []
    for _ in range(120):
        st = await pg.evaluate('ui.sess ? (ui.sess.end ? "END" : ui.sess.steps[ui.sess.i].kind) : "NOSESS"')
        kinds.append(st)
        if st in ('END', 'NOSESS'):
            break
        if st in ('learn', 'mission', 'shadow', 'grammar', 'charlearn'):
            await pg.click('[data-act=next]'); continue
        if st == 'conv':
            while not await pg.evaluate('ui.sess.steps[ui.sess.i].cs.done'):
                await pg.click('[data-act=cpick]:not([disabled])')
            await pg.click('[data-act=next]'); continue
        if st == 'prod' and await pg.locator('[data-act=tile]').count():
            n = await pg.locator('[data-act=tile]').count()
            for _ in range(n - 1):
                await pg.locator('[data-act=tile]:not(.used)').first.click()
            await pg.click('[data-act=checktiles]'); await pg.click('[data-act=next]'); continue
        await pg.locator('[data-act=ans]').first.click(); await pg.click('[data-act=next]')
    return kinds


async def main():
    from playwright.async_api import async_playwright
    serve()
    fails = []
    def check(cond, msg):
        print(('OK   ' if cond else 'ÉCHEC'), msg)
        if not cond: fails.append(msg)

    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(f'http://127.0.0.1:{PORT}/'); await pg.wait_for_timeout(2500)
        packs = await pg.evaluate('PACKS.map(p => p.id)')
        check(len(packs) > 1, f'chapitres chargés : {packs}')
        check(await pg.evaluate('Object.keys(AUDIO).length') > 0, 'index audio chargé')
        await pg.fill('#nm', 'Test'); await pg.click('[data-act=skipdiag]')
        for day in range(3):
            await pg.evaluate('S.lastSessionDay = null; save(); ui.sess = null; ui.tab = "home"; render()')
            await pg.click('[data-act=daily]')
            k = await run_session(pg)
            check(k[-1] == 'END', f'séance {day + 1} terminée ({len(k) - 1} étapes, types : {sorted(set(k[:-1]))})')
            await pg.click('[data-act=home]')
        r = await pg.evaluate("""async () => { say('谢谢'); await new Promise(r => setTimeout(r, 900));
            return curAudio ? (curAudio.error ? 'erreur' : 'mp3') : 'voix du téléphone'; }""")
        check(r == 'mp3', f'lecture audio : {r}')
        res = await pg.evaluate("""async () => { const an = async id => { const it = BY[id]; const blob = await (await fetch('audio/' + AUDIO[it.h])).blob();
            const st = {it, kind: 'shadow'}; ui.sess = {kind: 'mini', steps: [st], i: 0, xp: 0, ok: 0, n: 0, end: false};
            await analyzeBlob(st, blob); ui.sess = null; return st.rec.state === 'done' ? st.rec.res.score : -1; };
            await an('zaishuo'); const r = await an('nihao'); render(); return r; }""")
        check(await pg.evaluate('S.pitchRef') > 0, 'hauteur de voix mesurée sur une phrase de 5 syllabes')
        check(res >= 60, f'analyse de tons sur voix native (你好) : score {res}/100')
        await pg.evaluate('startTest()'); k = await run_session(pg)
        check(k[-1] == 'END', 'test HSK blanc terminé')
        await pg.click('[data-act=home]')
        await pg.wait_for_timeout(1500)
        await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1000)
        check(await pg.evaluate('!!document.querySelector(".cta")'), 'réouverture hors-ligne')
        check(not errs, f'aucune erreur JavaScript {errs[:3]}')
        await b.close()
    print('\n' + ('TOUT EST BON' if not fails else f'{len(fails)} problème(s)'))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    asyncio.run(main())
