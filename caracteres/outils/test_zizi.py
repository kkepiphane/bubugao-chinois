"""Test de bout en bout de Zìzì dans Chromium : séance complète avec tracé au doigt simulé,
onglets, quêtes, niveaux, les 3 défis, examen blanc HSK, lecture, hors-ligne. Usage, depuis caracteres/ :  python3 outils/test_zizi.py"""
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
        check(await pg.evaluate('S.q && S.q.done.seance === 1 && S.xp > 0'), 'quête « séance » validée et points gagnés')
        await pg.click('[data-act=home]')
        # après la séance du jour : on peut apprendre encore des nouveaux, autant qu'on veut
        n0 = await pg.evaluate('newToday()')
        for tour in range(2):
            await pg.click('[data-act=plus]')
            for _ in range(80):
                st = await pg.evaluate('ui.sess ? (ui.sess.end ? "END" : ui.sess.steps[ui.sess.i].kind + ":" + ui.sess.steps[ui.sess.i].c) : "NO"')
                if st in ('END', 'NO'): break
                k, c = st.split(':')
                if k == 'fiche': await pg.click('[data-act=next]'); continue
                if k in ('trace', 'ecrire'): await pg.wait_for_timeout(300); await draw(pg, c); await pg.wait_for_timeout(1200); await pg.click('[data-act=next]'); continue
                await pg.locator('[data-act=ans]').first.click(); await pg.click('[data-act=next]')
            await pg.click('[data-act=home]')
        n1 = await pg.evaluate('newToday()')
        check(n1 >= n0 + 4, f'« Encore des nouveaux » deux fois de suite : {n0} → {n1} nouveaux aujourd’hui')
        for t in ['mur', 'lire', 'hsk', 'prog', 'home']: await pg.click(f'[data-act=tab][data-k={t}]')
        await pg.click('[data-act=tab][data-k=mur]'); await pg.click('[data-act=mur][data-m=cles]'); await pg.click('[data-act=key] >> nth=0')
        check(await pg.locator('.keycard').count() > 10, 'clés affichées dans Mon mur')
        await pg.click('[data-act=mur][data-m=chars]')
        await pg.click('[data-act=tab][data-k=mur]'); await pg.click('.cell >> nth=0'); await pg.wait_for_timeout(500)
        check(await pg.evaluate('!document.getElementById("sheet").hidden'), 'fiche ouverte depuis le mur')
        await pg.click('[data-act=closesheet] >> nth=0')
        r = await pg.evaluate("""async () => { say(DATA.chars[0].a); await new Promise(r => setTimeout(r, 800)); return curAudio ? (curAudio.error ? 'erreur' : 'mp3') : 'tts'; }""")
        check(r == 'mp3', f'son : {r}')
        await pg.evaluate("DATA.chars.slice(0,40).forEach(x=>{const r=rec(x.c);r.intro=Date.now();SK.forEach(k=>{const s=skState(x.c,k);s.S=3;s.last=Date.now();});});save();ui.tab='lire';render()")
        await pg.click('[data-act=read] >> nth=0'); await pg.click('[data-act=readdone]')
        check(await pg.evaluate('Object.keys(S.read).length') == 1, 'lecture ouverte et marquée lue')
        # le rouleau sur l'accueil : 40 caractères appris = 2 pages terminées, on est à la page 3
        await pg.click('[data-act=tab][data-k=home]')
        check(await pg.locator('.paper .sc.on').count() == 0 and await pg.locator('.pd.done').count() == 2 and await pg.locator('.sc.next').count() == 1, 'rouleau : page en cours et 2 pages terminées')
        await pg.click('[data-act=page][data-p="0"] >> nth=0')
        check(await pg.locator('.paper .sc.on').count() == 20 and await pg.locator('.paper .seal').count() == 1, 'rouleau : page 1 feuilletée, scellée 完成')
        await pg.evaluate('ui.page = null; render()')
        for gid in ['mystere', 'cles', 'eclair']:
            await pg.evaluate(f"startGame('{gid}')")
            for _ in range(200):
                g = await pg.evaluate('ui.game ? {end: ui.game.end, found: ui.game.found, rend: ui.game.roundEnd} : null')
                if not g or g['end']: break
                if gid == 'mystere':
                    if g['found']: await pg.click('[data-act=mysnext]')
                    else: await pg.click(f"[data-act=mys][data-c='{await pg.evaluate('ui.game.c')}']")
                elif gid == 'cles':
                    if g['rend']: await pg.click('[data-act=huntnext]'); continue
                    for c in await pg.evaluate('ui.game.targets.filter(c => !ui.game.hit.includes(c))'):
                        await pg.click(f"[data-act=hunt][data-c='{c}']")
                else:
                    await pg.locator('[data-act=flash]:not([disabled])').first.click(timeout=3000)
                    await pg.wait_for_timeout(950)
                    if await pg.evaluate('ui.game.okN + (ui.game.combo === 0 ? 1 : 0)') >= 6: await pg.evaluate('ui.game.left = 1'); await pg.wait_for_timeout(1300)
            ok = await pg.evaluate(f"!!(ui.game && ui.game.end && S.games['{gid}'].plays === 1)")
            check(ok, f'défi {gid} joué jusqu’au bout (score ' + str(await pg.evaluate('ui.game ? ui.game.score : -1')) + ')')
            await pg.click('[data-act=ghome]')
        # examen blanc HSK
        await pg.click('[data-act=tab][data-k=hsk]'); await pg.click('[data-act=exam]'); await pg.click('[data-act=expy][data-v="1"]'); await pg.click('[data-act=exgo]')
        parts = await pg.evaluate('[...new Set(ui.exam.qs.map(q => q.part))].length')
        for _ in range(20):
            await pg.locator('[data-act=exans]').first.click(); await pg.wait_for_timeout(320)
        check(parts == 4 and await pg.evaluate("ui.exam.stage === 'res' && S.exams.length === 1"), f'examen blanc HSK : 20 questions, 4 parties, note {await pg.evaluate("ui.exam.score")}/100')
        await pg.click('[data-act=exhome]'); await pg.click('[data-act=extrain][data-p="3"]')
        for _ in range(5):
            await pg.locator('[data-act=exans]').first.click(); await pg.click('[data-act=exnext]')
        check(await pg.evaluate("ui.exam.stage === 'res'"), 'entraînement HSK partie 4 terminé')
        await pg.click('[data-act=exhome]')
        # niveau supérieur et progrès
        await pg.evaluate('ui.levelUp = null; S.xp = DATA.rangs[1].xp - 5; addXP(10); ui.tab = "prog"; render()')
        await pg.wait_for_timeout(300)
        check(await pg.evaluate('!document.getElementById("sheet").hidden && document.getElementById("sheet").textContent.includes(DATA.rangs[1].fr)'), 'nouveau titre annoncé')
        await pg.click('[data-act=closesheet] >> nth=0')
        check(await pg.locator('.badge.on').count() >= 3 and await pg.locator('.cal i').count() == 84, 'progrès : médailles et calendrier')
        await pg.wait_for_timeout(1500); await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1000)
        check(await pg.evaluate('!!(typeof DATA !== "undefined" && DATA && DATA.chars.length)'), 'réouverture hors-ligne')
        # installation : aide dans le navigateur, fenêtre de Bùbùgāo, appli Zìzì installée
        UA = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'
        async def ouvrir(url, standalone, referer=None):
            c = await b.new_context(viewport={'width': 390, 'height': 844}, user_agent=UA)
            q = await c.new_page(); q.on('pageerror', lambda e: errs.append(str(e)))
            if standalone:  # appli installée : (display-mode: standalone) vrai
                await q.add_init_script("const mm = window.matchMedia.bind(window); window.matchMedia = m => /display-mode:\\s*standalone/.test(m) ? {matches: true, media: m, addEventListener() {}, removeEventListener() {}} : mm(m);")
            await q.goto(url, referer=referer); await q.wait_for_timeout(4800)
            return c, q
        c2, q = await ouvrir(f'http://127.0.0.1:{PORT}/', False)
        check(await q.locator('text=Installe Zìzì sur ton téléphone').count() == 1, 'navigateur : aide pour installer depuis le menu')
        await q.click('[data-act=installok]')
        check(await q.locator('text=Installe Zìzì sur ton téléphone').count() == 0, 'aide masquée après « déjà installée »')
        await c2.close()
        c2, q = await ouvrir(f'http://127.0.0.1:{PORT}/', True, referer=f'http://127.0.0.1:{PORT}/bubugao-chinois/')
        href = await q.locator('a:has-text("Ouvrir dans Chrome")').get_attribute('href') if await q.locator('a:has-text("Ouvrir dans Chrome")').count() else ''
        check(href.startswith('intent://') and 'package=com.android.chrome' in href, 'fenêtre de Bùbùgāo : bouton « Ouvrir dans Chrome »')
        await c2.close()
        c2, q = await ouvrir(f'http://127.0.0.1:{PORT}/?app=zizi', True)
        check(await q.locator('text=Installe Zìzì').count() == 0, 'appli Zìzì installée : pas de carte d’installation')
        await c2.close()
        check(not errs, f'aucune erreur JavaScript {errs[:3]}')
        await b.close()
    print('\n' + ('TOUT EST BON' if not fails else f'{len(fails)} problème(s)')); sys.exit(1 if fails else 0)

if __name__ == '__main__':
    asyncio.run(main())
