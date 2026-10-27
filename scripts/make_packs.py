# Génère les chapitres (packs) de Bùbùgāo.
# Item : "id | caractères | pinyin (mots séparés par espace, syllabes par -) | tons | tons prononcés (ou vide) | français"
import json, os, re

OUT_PUB = '../packs'
OUT_QUEUE = '../a-publier'

def items(spec, st=0):
    out = []
    for line in spec.strip().splitlines():
        f = [x.strip() for x in line.split('|')]
        it = {'id': f[0], 'h': f[1], 'p': f[2], 't': [int(x) for x in f[3].split()], 'fr': f[5], 'st': st}
        if f[4]: it['s'] = [int(x) for x in f[4].split()]
        if len(f) > 6 and f[6]: it['m'] = f[6]
        out.append(it)
    return out

def pair(a, b):
    def one(x):
        h, p, t, fr = x
        return {'h': h, 'p': p, 't': t, 'fr': fr}
    return [one(a), one(b)]

def chars(spec):
    out = []
    for line in spec.strip().splitlines():
        c, p, m, r, rm = [x.strip() for x in line.split('|')]
        out.append({'c': c, 'p': p, 'm': m, 'r': r, 'rm': rm})
    return out

def ex(h, p, fr): return {'h': h, 'p': p, 'fr': fr}
def o(h, p, fr, ok=False, n=None, fix=None):
    d = {'h': h, 'p': p, 'fr': fr}
    if ok: d['ok'] = 1; d['n'] = n
    else: d['fix'] = fix
    return d
def node(h, p, fr, opts=None, end=False, coach=None):
    d = {'h': h, 'p': p, 'fr': fr}
    if end: d['end'] = 1
    else: d['o'] = opts
    if coach: d['coach'] = coach
    return d
def conv(id, title, who, whoFr, intro, nodes, st=0):
    return {'id': id, 'st': st, 'title': title, 'who': who, 'whoFr': whoFr, 'intro': intro, 'start': 'a', 'nodes': nodes}

PACKS = []

# ---------------- HSK 1 · 1 ----------------
PACKS.append(dict(id='hsk1-01', file='hsk1-01-presenter.json', branch='hsk', level=1, publish=True,
 title='HSK 1 · 1 — Se présenter',
 desc='Dire qui tu es, demander le nom de quelqu’un, d’où il vient. 15 mots de la liste officielle HSK 1.',
 grammar={'title': 'Être : 是, et la négation 不',
  'explain': 'Pour dire « je suis… », on met 是 (shì) entre la personne et ce qu’elle est. Pour dire « ne… pas », on met 不 (bù) juste avant le verbe. Le verbe ne change jamais : 我是, 你是, 他是.',
  'examples': [ex('我是老师。', 'Wǒ shì lǎoshī.', 'Je suis enseignante.'), ex('我不是老师。', 'Wǒ bú shì lǎoshī.', 'Je ne suis pas enseignante.'), ex('他是中国人。', 'Tā shì Zhōngguó rén.', 'Il est chinois.'), ex('她不是中国人。', 'Tā bú shì Zhōngguó rén.', 'Elle n’est pas chinoise.')],
  'tip': '不 se prononce bú devant un 4e ton : 不是 bú shì.'},
 items=items('''
k01_wo | 我 | wo | 3 | | Je, moi
k01_ni | 你 | ni | 3 | | Tu, toi
k01_ta | 他 | ta | 1 | | Il, lui
k01_ta2 | 她 | ta | 1 | | Elle
k01_women | 我们 | wo-men | 3 0 | | Nous
k01_shi | 是 | shi | 4 | | Être, c’est
k01_bu | 不 | bu | 4 | | Ne… pas, non
k01_jiao | 叫 | jiao | 4 | | S’appeler
k01_mingzi | 名字 | ming-zi | 2 0 | | Nom, prénom
k01_ren | 人 | ren | 2 | | Personne
k01_zhongguo | 中国 | Zhong-guo | 1 2 | | Chine
k01_renshi | 认识 | ren-shi | 4 0 | | Connaître (quelqu’un)
k01_gaoxing | 高兴 | gao-xing | 1 4 | | Content, heureux
k01_shenme | 什么 | shen-me | 2 0 | | Quoi, quel
k01_shei | 谁 | shei | 2 | | Qui
k01_s_mingzi | 你叫什么名字 | ni jiao shen-me ming-zi | 3 4 2 0 2 0 | | Comment tu t’appelles ? | Demande son prénom à un collègue que tu ne connais pas bien : 你叫什么名字？
k01_s_duoge | 我是多哥人 | wo shi Duo-ge ren | 3 4 1 1 2 | | Je suis Togolaise | Quand un collègue chinois te parle, présente-toi : 我是多哥人。
k01_s_gaoxing | 认识你很高兴 | ren-shi ni hen gao-xing | 4 0 3 3 1 4 | 4 0 2 3 1 4 | Enchantée
'''),
 pairs=[pair(('人', 'ren', 2, 'personne'), ('认', 'ren', 4, 'reconnaître'))],
 chars=chars('''
我 | wǒ | je | 戈 | hallebarde
你 | nǐ | tu | 亻 | personne
他 | tā | il | 亻 | personne
她 | tā | elle | 女 | femme
是 | shì | être | 日 | soleil
不 | bù | ne… pas | 一 | un
人 | rén | personne | 人 | personne
国 | guó | pays | 囗 | enclos
'''),
 convs=[conv('hsk1-presenter', 'Une nouvelle collègue', '新同事', 'Nouvelle collègue', 'Une nouvelle employée chinoise arrive dans ton atelier.', {
  'a': node('你好！你叫什么名字？', 'Nǐ hǎo! Nǐ jiào shénme míngzi?', 'Bonjour ! Comment tu t’appelles ?', [
     o('我叫{name}。你呢？', 'Wǒ jiào {name}. Nǐ ne?', 'Je m’appelle {name}. Et toi ?', True, 'b'),
     o('我是中国人。', 'Wǒ shì Zhōngguó rén.', 'Je suis chinoise.', fix='Elle demande ton nom : réponds « 我叫… ». Et tu n’es pas chinoise !')]),
  'b': node('我叫王丽。你是哪国人？', 'Wǒ jiào Wáng Lì. Nǐ shì nǎ guó rén?', 'Je m’appelle Wang Li. Tu viens de quel pays ?', [
     o('我是多哥人。', 'Wǒ shì Duōgē rén.', 'Je suis Togolaise.', True, 'end'),
     o('我不是。', 'Wǒ bú shì.', 'Je ne suis pas.', fix='哪国人 = de quel pays. Réponds « 我是多哥人 ».')]),
  'end': node('认识你很高兴！', 'Rènshi nǐ hěn gāoxìng!', 'Enchantée !', end=True)})],
 bonus=[{'h': '幸会', 'p': 'xìnghuì', 'fr': 'Ravie de vous rencontrer (poli)', 'note': 'Version très polie de 认识你很高兴, pour un patron ou un client.'}]))

# ---------------- HSK 1 · 2 ----------------
PACKS.append(dict(id='hsk1-02', file='hsk1-02-nombres.json', branch='hsk', level=1, publish=True,
 title='HSK 1 · 2 — Les nombres',
 desc='Compter de 1 à 99, demander combien, dire son âge. 15 mots HSK 1.',
 grammar={'title': '几 ou 多少 : « combien ? »',
  'explain': 'Les nombres chinois se construisent comme des briques : 十一 = 10+1 = 11, 二十 = 2×10 = 20, 二十三 = 23. Pour demander « combien », 几 (jǐ) sert pour un petit nombre (moins de 10) et doit être suivi d’un classificateur comme 个. 多少 (duōshao) sert pour un nombre grand ou inconnu.',
  'examples': [ex('你有几个朋友？', 'Nǐ yǒu jǐ ge péngyou?', 'Tu as combien d’amis ?'), ex('多少钱？', 'Duōshao qián?', 'Combien ça coûte ?'), ex('三十五', 'sānshíwǔ', '35 (3×10+5)'), ex('你女儿几岁？', 'Nǐ nǚ’ér jǐ suì?', 'Ta fille a quel âge ?')],
  'tip': 'Après 几, mets toujours un classificateur (个, 岁, 点…). Après 多少, ce n’est pas obligatoire.'},
 items=items('''
k02_yi | 一 | yi | 1 | | Un (1)
k02_er | 二 | er | 4 | | Deux (2)
k02_san | 三 | san | 1 | | Trois (3)
k02_si | 四 | si | 4 | | Quatre (4)
k02_wu | 五 | wu | 3 | | Cinq (5)
k02_liu | 六 | liu | 4 | | Six (6)
k02_qi | 七 | qi | 1 | | Sept (7)
k02_ba | 八 | ba | 1 | | Huit (8)
k02_jiu | 九 | jiu | 3 | | Neuf (9)
k02_shi | 十 | shi | 2 | | Dix (10)
k02_ji | 几 | ji | 3 | | Combien (petit nombre)
k02_duoshao | 多少 | duo-shao | 1 0 | | Combien
k02_ge | 个 | ge | 4 | | Classificateur courant (un, une)
k02_sui | 岁 | sui | 4 | | An (âge)
k02_nian | 年 | nian | 2 | | Année
k02_s_jisui | 你几岁 | ni ji sui | 3 3 4 | 2 3 4 | Tu as quel âge ? (à un enfant)
k02_s_ershisan | 我二十三岁 | wo er-shi-san sui | 3 4 2 1 4 | | J’ai vingt-trois ans | Dis ton âge à une collègue en chinois : 我…岁。
'''),
 pairs=[pair(('八', 'ba', 1, 'huit'), ('爸', 'ba', 4, 'papa')), pair(('七', 'qi', 1, 'sept'), ('起', 'qi', 3, 'se lever'))],
 chars=chars('''
一 | yī | un | 一 | un
二 | èr | deux | 二 | deux
三 | sān | trois | 一 | un
十 | shí | dix | 十 | dix
个 | gè | unité | 人 | personne
岁 | suì | an (âge) | 山 | montagne
年 | nián | année | 干 | sec, tige
多 | duō | beaucoup | 夕 | soir
'''),
 convs=[conv('hsk1-nombres', 'Combien sur la ligne ?', '组长', 'Chef d’équipe', 'Ton chef d’équipe fait le point avant le début du poste.', {
  'a': node('这里有几个人？', 'Zhèlǐ yǒu jǐ ge rén?', 'Il y a combien de personnes ici ?', [
     o('有八个人。', 'Yǒu bā ge rén.', 'Il y a huit personnes.', True, 'b'),
     o('八岁。', 'Bā suì.', 'Huit ans.', fix='岁 sert pour l’âge. Pour compter des personnes : « 八个人 ».')]),
  'b': node('好。你今年多少岁？', 'Hǎo. Nǐ jīnnián duōshao suì?', 'Bien. Tu as quel âge cette année ?', [
     o('我二十三岁。', 'Wǒ èrshísān suì.', 'J’ai vingt-trois ans.', True, 'end'),
     o('二十三个。', 'Èrshísān ge.', 'Vingt-trois (objets).', fix='Pour l’âge, on utilise 岁 : « 我二十三岁 ».')]),
  'end': node('我也二十三岁！', 'Wǒ yě èrshísān suì!', 'Moi aussi, j’ai vingt-trois ans !', end=True)})]))

# ---------------- HSK 1 · 3 ----------------
PACKS.append(dict(id='hsk1-03', file='hsk1-03-famille.json', branch='hsk', level=1, publish=True,
 title='HSK 1 · 3 — Famille et entourage',
 desc='Parler de ta famille, de tes amis, des gens autour de toi. 15 mots HSK 1.',
 grammar={'title': '有 / 没有, et 的 pour « de »',
  'explain': '有 (yǒu) veut dire « avoir » ou « il y a ». Sa négation est toujours 没有 (méiyǒu), jamais 不有. 的 (de) relie celui qui possède et ce qui est possédé, dans cet ordre : 我的妈妈 = « ma mère » (mot à mot « moi-de mère »).',
  'examples': [ex('我有一个朋友。', 'Wǒ yǒu yí ge péngyou.', 'J’ai un ami.'), ex('我没有电脑。', 'Wǒ méiyǒu diànnǎo.', 'Je n’ai pas d’ordinateur.'), ex('这是我的老师。', 'Zhè shì wǒ de lǎoshī.', 'C’est mon professeur.'), ex('妈妈的家', 'māma de jiā', 'la maison de maman')],
  'tip': 'Pour la famille proche, on peut enlever 的 : 我妈妈, 我家.'},
 items=items('''
k03_baba | 爸爸 | ba-ba | 4 0 | | Papa
k03_mama | 妈妈 | ma-ma | 1 0 | | Maman
k03_erzi | 儿子 | er-zi | 2 0 | | Fils
k03_nver | 女儿 | nv-er | 3 2 | | Fille (enfant)
k03_pengyou | 朋友 | peng-you | 2 0 | | Ami, amie
k03_tongxue | 同学 | tong-xue | 2 2 | | Camarade de classe
k03_laoshi | 老师 | lao-shi | 3 1 | | Professeur
k03_xuesheng | 学生 | xue-sheng | 2 0 | | Élève, étudiant
k03_yisheng | 医生 | yi-sheng | 1 1 | | Médecin
k03_xiansheng | 先生 | xian-sheng | 1 0 | | Monsieur
k03_xiaojie | 小姐 | xiao-jie | 3 3 | 2 3 | Mademoiselle
k03_jia | 家 | jia | 1 | | Maison, famille
k03_you | 有 | you | 3 | | Avoir, il y a
k03_meiyou | 没有 | mei-you | 2 3 | | Ne pas avoir
k03_de | 的 | de | 0 | | De (possession)
k03_s_pengyou | 这是我的朋友 | zhe shi wo de peng-you | 4 4 3 0 2 0 | | C’est mon amie | Présente une amie ou un proche à un collègue chinois : 这是我的…
k03_s_erzi | 我有一个儿子 | wo you yi ge er-zi | 3 3 2 0 2 0 | 2 3 2 0 2 0 | J’ai un fils
'''),
 pairs=[pair(('有', 'you', 3, 'avoir'), ('又', 'you', 4, 'encore, de nouveau'))],
 chars=chars('''
爸 | bà | papa | 父 | père
妈 | mā | maman | 女 | femme
子 | zǐ | enfant | 子 | enfant
女 | nǚ | femme | 女 | femme
朋 | péng | ami | 月 | lune
友 | yǒu | ami | 又 | main
家 | jiā | maison | 宀 | toit
有 | yǒu | avoir | 月 | lune
'''),
 convs=[conv('hsk1-famille', 'Les photos de famille', '同事', 'Collègue', 'À la pause, une collègue regarde les photos sur ton téléphone.', {
  'a': node('这是谁？', 'Zhè shì shéi?', 'C’est qui ?', [
     o('这是我的妈妈。', 'Zhè shì wǒ de māma.', 'C’est ma maman.', True, 'b'),
     o('这是我的。', 'Zhè shì wǒ de.', 'C’est à moi.', fix='Elle demande qui c’est : précise « 我的妈妈 » (ma maman), « 我的朋友 »…')]),
  'b': node('你妈妈很漂亮！你有儿子吗？', 'Nǐ māma hěn piàoliang! Nǐ yǒu érzi ma?', 'Ta maman est très belle ! Tu as un fils ?', [
     o('没有，我没有儿子。', 'Méiyǒu, wǒ méiyǒu érzi.', 'Non, je n’ai pas de fils.', True, 'end'),
     o('有，我有一个儿子。', 'Yǒu, wǒ yǒu yí ge érzi.', 'Oui, j’ai un fils.', True, 'end'),
     o('我不有儿子。', 'Wǒ bù yǒu érzi.', '(erreur de grammaire)', fix='有 ne se nie jamais avec 不 : on dit « 没有 ».')]),
  'end': node('你的家很好！', 'Nǐ de jiā hěn hǎo!', 'Tu as une belle famille !', end=True)})]))

# ---------------- HSK 1 · 4 ----------------
PACKS.append(dict(id='hsk1-04', file='hsk1-04-temps.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 4 — L’heure et la date',
 desc='Dire l’heure, la date, les moments de la journée. 13 mots HSK 1.',
 grammar={'title': 'La date et l’heure : du plus grand au plus petit',
  'explain': 'En chinois, on part toujours du plus grand vers le plus petit : année, mois, jour, moment, heure. 十月二号 = « le 2 octobre » (mot à mot « 10e mois, 2e jour »). Et le moment se place avant le verbe : 我明天去, pas 我去明天.',
  'examples': [ex('今天十月二号。', 'Jīntiān shí yuè èr hào.', 'Aujourd’hui, c’est le 2 octobre.'), ex('星期一上午九点', 'xīngqīyī shàngwǔ jiǔ diǎn', 'lundi à 9 h du matin'), ex('我明天下午去。', 'Wǒ míngtiān xiàwǔ qù.', 'J’y vais demain après-midi.'), ex('你什么时候去？', 'Nǐ shénme shíhou qù?', 'Tu y vas quand ?')],
  'tip': 'Les jours de la semaine sont des nombres : 星期一 = lundi, 星期二 = mardi… 星期六 = samedi. Seul dimanche est spécial : 星期天.'},
 items=items('''
k04_jintian | 今天 | jin-tian | 1 1 | | Aujourd’hui
k04_mingtian | 明天 | ming-tian | 2 1 | | Demain
k04_zuotian | 昨天 | zuo-tian | 2 1 | | Hier
k04_xianzai | 现在 | xian-zai | 4 4 | | Maintenant
k04_dian | 点 | dian | 3 | | Heure (8 点 = 8 h)
k04_fenzhong | 分钟 | fen-zhong | 1 1 | | Minute
k04_shangwu | 上午 | shang-wu | 4 3 | | Le matin
k04_zhongwu | 中午 | zhong-wu | 1 3 | | Midi
k04_xiawu | 下午 | xia-wu | 4 3 | | L’après-midi
k04_xingqi | 星期 | xing-qi | 1 1 | | Semaine
k04_yue | 月 | yue | 4 | | Mois
k04_hao | 号 | hao | 4 | | Jour du mois (date)
k04_shihou | 时候 | shi-hou | 2 0 | | Moment
k04_s_jidian | 现在几点 | xian-zai ji dian | 4 4 3 3 | 4 4 2 3 | Quelle heure est-il ? | Demande l’heure à un collègue chinois : 现在几点？
k04_s_jihao | 今天几月几号 | jin-tian ji yue ji hao | 1 1 3 4 3 4 | | On est quel jour aujourd’hui ?
k04_s_shenmeshihou | 你什么时候下班 | ni shen-me shi-hou xia-ban | 3 2 0 2 0 4 1 | | Tu finis quand ? | Demande à un collègue : 你什么时候下班？
'''),
 pairs=[pair(('天', 'tian', 1, 'jour, ciel'), ('甜', 'tian', 2, 'sucré'))],
 chars=chars('''
今 | jīn | maintenant | 人 | personne
明 | míng | clair, demain | 日 | soleil
天 | tiān | jour, ciel | 大 | grand
午 | wǔ | midi | 十 | dix
上 | shàng | dessus | 一 | un
下 | xià | dessous | 一 | un
月 | yuè | mois, lune | 月 | lune
星 | xīng | étoile | 日 | soleil
'''),
 convs=[conv('hsk1-temps', 'Quelle heure, quel jour ?', '同事', 'Collègue', 'Ton téléphone n’a plus de batterie. Tu demandes à une collègue.', {
  'a': node('现在几点？', 'Xiànzài jǐ diǎn?', 'Il est quelle heure ?', [
     o('现在十点。', 'Xiànzài shí diǎn.', 'Il est dix heures.', True, 'b'),
     o('现在星期一。', 'Xiànzài xīngqīyī.', 'C’est lundi.', fix='几点 = quelle heure : réponds « 十点 ».')], coach='Ta collègue te retourne la question pour vérifier que tu sais lire l’heure.'),
  'b': node('今天几号？', 'Jīntiān jǐ hào?', 'On est le combien aujourd’hui ?', [
     o('今天十月二号。', 'Jīntiān shí yuè èr hào.', 'Nous sommes le 2 octobre.', True, 'end'),
     o('今天下午。', 'Jīntiān xiàwǔ.', 'Cet après-midi.', fix='几号 = quel jour du mois : « 十月二号 » (2 octobre).')]),
  'end': node('谢谢！明天见！', 'Xièxie! Míngtiān jiàn!', 'Merci ! À demain !', end=True)})]))

# ---------------- HSK 1 · 5 ----------------
PACKS.append(dict(id='hsk1-05', file='hsk1-05-manger.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 5 — Manger et boire',
 desc='Commander au restaurant, dire ce que tu aimes et ce que tu veux. 14 mots HSK 1.',
 grammar={'title': '想 et 喜欢 + verbe',
  'explain': '想 (xiǎng) = « vouloir, avoir envie » maintenant. 喜欢 (xǐhuan) = « aimer » en général. Les deux se placent devant un autre verbe : 我想喝水 (j’ai envie de boire de l’eau), 我喜欢吃苹果 (j’aime manger des pommes).',
  'examples': [ex('我想喝水。', 'Wǒ xiǎng hē shuǐ.', 'Je veux boire de l’eau.'), ex('我喜欢吃米饭。', 'Wǒ xǐhuan chī mǐfàn.', 'J’aime manger du riz.'), ex('你想去饭店吗？', 'Nǐ xiǎng qù fàndiàn ma?', 'Tu veux aller au restaurant ?'), ex('我不喜欢喝茶。', 'Wǒ bù xǐhuan hē chá.', 'Je n’aime pas boire du thé.')],
  'tip': '吃 = manger (le solide), 喝 = boire (le liquide). On dit 喝茶, jamais 吃茶.'},
 items=items('''
k05_chi | 吃 | chi | 1 | | Manger
k05_he | 喝 | he | 1 | | Boire
k05_mifan | 米饭 | mi-fan | 3 4 | | Riz (cuit)
k05_cai | 菜 | cai | 4 | | Plat, légume
k05_cha | 茶 | cha | 2 | | Thé
k05_shui | 水 | shui | 3 | | Eau
k05_shuiguo | 水果 | shui-guo | 3 3 | 2 3 | Fruit
k05_pingguo | 苹果 | ping-guo | 2 3 | | Pomme
k05_beizi | 杯子 | bei-zi | 1 0 | | Verre, tasse
k05_fandian | 饭店 | fan-dian | 4 4 | | Restaurant
k05_xihuan | 喜欢 | xi-huan | 3 0 | | Aimer (bien)
k05_xiang | 想 | xiang | 3 | | Vouloir, penser
k05_ai | 爱 | ai | 4 | | Aimer (fort)
k05_qing | 请 | qing | 3 | | S’il vous plaît, inviter
k05_s_xiangchi | 你想吃什么 | ni xiang chi shen-me | 3 3 1 2 0 | 2 3 1 2 0 | Tu veux manger quoi ? | À la pause repas, demande à un collègue : 你想吃什么？
k05_s_hecha | 我喜欢喝茶 | wo xi-huan he cha | 3 3 0 1 2 | 2 3 0 1 2 | J’aime boire du thé
'''),
 pairs=[pair(('吃', 'chi', 1, 'manger'), ('迟', 'chi', 2, 'en retard'))],
 chars=chars('''
吃 | chī | manger | 口 | bouche
喝 | hē | boire | 口 | bouche
米 | mǐ | riz | 米 | riz
饭 | fàn | repas | 饣 | nourriture
茶 | chá | thé | 艹 | herbe
水 | shuǐ | eau | 水 | eau
果 | guǒ | fruit | 木 | arbre
想 | xiǎng | vouloir, penser | 心 | cœur
'''),
 convs=[conv('hsk1-restaurant', 'Au restaurant chinois', '服务员', 'Serveur', 'Tu déjeunes dans un petit restaurant chinois près de l’usine.', {
  'a': node('你好！你想吃什么？', 'Nǐ hǎo! Nǐ xiǎng chī shénme?', 'Bonjour ! Qu’est-ce que tu veux manger ?', [
     o('我想吃米饭和菜。', 'Wǒ xiǎng chī mǐfàn hé cài.', 'Je voudrais du riz et un plat.', True, 'b'),
     o('我想睡觉。', 'Wǒ xiǎng shuìjiào.', 'Je veux dormir.', fix='吃 = manger. Réponds « 我想吃… ».')]),
  'b': node('你想喝什么？', 'Nǐ xiǎng hē shénme?', 'Et à boire ?', [
     o('请给我一杯茶。', 'Qǐng gěi wǒ yì bēi chá.', 'Un thé, s’il vous plaît.', True, 'end'),
     o('我喜欢喝水。', 'Wǒ xǐhuan hē shuǐ.', 'J’aime l’eau.', True, 'end'),
     o('我想吃茶。', 'Wǒ xiǎng chī chá.', '(erreur)', fix='Le thé se boit : 喝茶, pas 吃茶.')]),
  'end': node('好的，请等一下。', 'Hǎo de, qǐng děng yíxià.', 'Très bien, un instant.', end=True)})]))

# ---------------- HSK 1 · 6 ----------------
PACKS.append(dict(id='hsk1-06', file='hsk1-06-acheter.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 6 — Acheter',
 desc='Faire des achats, demander le prix, dire que c’est trop. 12 mots HSK 1.',
 grammar={'title': '太 … 了 : « trop » et les exclamations',
  'explain': '太 (tài) + adjectif + 了 (le) veut dire « trop… » : 太多了 = c’est trop. La même forme sert aussi à s’enthousiasmer : 太好了 ! = génial !',
  'examples': [ex('太多了！', 'Tài duō le!', 'C’est trop !'), ex('这个太小了。', 'Zhège tài xiǎo le.', 'Celui-ci est trop petit.'), ex('太漂亮了！', 'Tài piàoliang le!', 'Trop beau !'), ex('这个多少钱？', 'Zhège duōshao qián?', 'Combien coûte celui-ci ?')],
  'tip': 'À l’oral, on dit 块 (kuài) pour le yuan : 十块 = 10 yuans.'},
 items=items('''
k06_mai | 买 | mai | 3 | | Acheter
k06_qian | 钱 | qian | 2 | | Argent
k06_kuai | 块 | kuai | 4 | | Yuan (à l’oral), morceau
k06_dongxi | 东西 | dong-xi | 1 0 | | Chose, affaires
k06_shangdian | 商店 | shang-dian | 1 4 | | Magasin
k06_yifu | 衣服 | yi-fu | 1 0 | | Vêtement
k06_duo | 多 | duo | 1 | | Beaucoup
k06_shao | 少 | shao | 3 | | Peu
k06_tai | 太 | tai | 4 | | Trop
k06_yidianr | 一点儿 | yi-dian-r | 4 3 0 | | Un peu
k06_xie | 些 | xie | 1 | | Quelques
k06_piaoliang | 漂亮 | piao-liang | 4 0 | | Joli, beau
k06_s_duoshaoqian | 这个多少钱 | zhe-ge duo-shao qian | 4 0 1 0 2 | | Combien coûte celui-ci ? | Dans un magasin chinois, demande un prix : 这个多少钱？
k06_s_taiduole | 太多了 | tai duo le | 4 1 0 | | C’est trop
k06_s_maidongxi | 我想买一些东西 | wo xiang mai yi-xie dong-xi | 3 3 3 4 1 1 0 | 2 2 3 4 1 1 0 | Je voudrais acheter quelques affaires
'''),
 pairs=[pair(('少', 'shao', 3, 'peu'), ('烧', 'shao', 1, 'brûler'))],
 chars=chars('''
钱 | qián | argent | 钅 | métal
块 | kuài | morceau, yuan | 土 | terre
店 | diàn | boutique | 广 | abri
衣 | yī | vêtement | 衣 | vêtement
服 | fú | vêtement | 月 | lune
少 | shǎo | peu | 小 | petit
太 | tài | trop | 大 | grand
东 | dōng | est | 一 | un
'''),
 convs=[conv('hsk1-acheter', 'Une robe au magasin', '店员', 'Vendeuse', 'Tu cherches une tenue dans un magasin tenu par une commerçante chinoise.', {
  'a': node('你想买什么？', 'Nǐ xiǎng mǎi shénme?', 'Tu veux acheter quoi ?', [
     o('我想买衣服。', 'Wǒ xiǎng mǎi yīfu.', 'Je voudrais acheter des vêtements.', True, 'b'),
     o('我想卖衣服。', 'Wǒ xiǎng mài yīfu.', 'Je veux vendre des vêtements.', fix='卖 mài = vendre, 买 mǎi = acheter. Seul le ton change !')]),
  'b': node('这个很漂亮，一百块。', 'Zhège hěn piàoliang, yìbǎi kuài.', 'Celle-ci est très jolie, cent yuans.', [
     o('太多了！少一点儿，可以吗？', 'Tài duō le! Shǎo yìdiǎnr, kěyǐ ma?', 'C’est trop ! Un peu moins, c’est possible ?', True, 'c'),
     o('好，我买。', 'Hǎo, wǒ mǎi.', 'D’accord, je la prends.', True, 'end')]),
  'c': node('好吧，八十块。', 'Hǎo ba, bāshí kuài.', 'Bon, quatre-vingts yuans.', [
     o('好，谢谢！', 'Hǎo, xièxie!', 'D’accord, merci !', True, 'end')]),
  'end': node('谢谢，再见！', 'Xièxie, zàijiàn!', 'Merci, au revoir !', end=True)})]))

# ---------------- HSK 1 · 7 ----------------
PACKS.append(dict(id='hsk1-07', file='hsk1-07-lieux.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 7 — Où ? Les lieux',
 desc='Dire où tu habites, où se trouve quelque chose, devant, derrière. 14 mots HSK 1.',
 grammar={'title': '在 : être à (un endroit)',
  'explain': '在 (zài) + lieu = « être à ». 我在家 = je suis à la maison. Pour demander où, remplace le lieu par 哪儿 (nǎr) : 你在哪儿 ? Le chinois ne change pas l’ordre des mots pour poser une question.',
  'examples': [ex('我在家。', 'Wǒ zài jiā.', 'Je suis à la maison.'), ex('学校在哪儿？', 'Xuéxiào zài nǎr?', 'Où est l’école ?'), ex('医院在学校后面。', 'Yīyuàn zài xuéxiào hòumiàn.', 'L’hôpital est derrière l’école.'), ex('我住在北京。', 'Wǒ zhù zài Běijīng.', 'J’habite à Pékin.')],
  'tip': '这 (zhè) = ce…ci, près de toi. 那 (nà) = ce…là, plus loin.'},
 items=items('''
k07_zai | 在 | zai | 4 | | Être à, se trouver
k07_na | 哪 | na | 3 | | Quel, lequel
k07_nar | 哪儿 | na-r | 3 0 | | Où
k07_zhe | 这 | zhe | 4 | | Ce, ceci
k07_na2 | 那 | na | 4 | | Ce…là, cela
k07_li | 里 | li | 3 | | Dedans
k07_shang | 上 | shang | 4 | | Sur, dessus
k07_xia | 下 | xia | 4 | | Sous, dessous
k07_qianmian | 前面 | qian-mian | 2 4 | | Devant
k07_houmian | 后面 | hou-mian | 4 4 | | Derrière
k07_zhu | 住 | zhu | 4 | | Habiter
k07_xuexiao | 学校 | xue-xiao | 2 4 | | École
k07_yiyuan | 医院 | yi-yuan | 1 4 | | Hôpital
k07_beijing | 北京 | Bei-jing | 3 1 | | Pékin
k07_s_zhuzai | 你住在哪儿 | ni zhu zai na-r | 3 4 4 3 0 | | Tu habites où ? | Demande à un collègue chinois où il habite : 你住在哪儿？
k07_s_yiyuan | 医院在学校后面 | yi-yuan zai xue-xiao hou-mian | 1 4 4 2 4 4 4 | | L’hôpital est derrière l’école
'''),
 pairs=[pair(('住', 'zhu', 4, 'habiter'), ('猪', 'zhu', 1, 'cochon'))],
 chars=chars('''
在 | zài | être à | 土 | terre
哪 | nǎ | quel | 口 | bouche
这 | zhè | ce, ceci | 辶 | marche
那 | nà | cela | 阝 | ville
住 | zhù | habiter | 亻 | personne
校 | xiào | école | 木 | arbre
医 | yī | médecine | 匚 | coffre
院 | yuàn | cour, institution | 阝 | ville
'''),
 convs=[conv('hsk1-lieux', 'Où habites-tu ?', '同事', 'Collègue', 'Un collègue veut organiser un covoiturage.', {
  'a': node('你住在哪儿？', 'Nǐ zhù zài nǎr?', 'Tu habites où ?', [
     o('我住在学校后面。', 'Wǒ zhù zài xuéxiào hòumiàn.', 'J’habite derrière l’école.', True, 'b'),
     o('我在工作。', 'Wǒ zài gōngzuò.', 'Je suis en train de travailler.', fix='住在哪儿 = tu habites où. Réponds « 我住在… ».')]),
  'b': node('医院在哪儿？', 'Yīyuàn zài nǎr?', 'Et l’hôpital, il est où ?', [
     o('医院在商店前面。', 'Yīyuàn zài shāngdiàn qiánmiàn.', 'L’hôpital est devant le magasin.', True, 'end'),
     o('我去医院。', 'Wǒ qù yīyuàn.', 'Je vais à l’hôpital.', fix='Il demande où se trouve l’hôpital : « 医院在… ».')]),
  'end': node('好，谢谢你！', 'Hǎo, xièxie nǐ!', 'Bien, merci !', end=True)})]))

# ---------------- HSK 1 · 8 ----------------
PACKS.append(dict(id='hsk1-08', file='hsk1-08-deplacements.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 8 — Se déplacer et téléphoner',
 desc='Aller, venir, rentrer, prendre un taxi, passer un appel. 13 mots HSK 1.',
 grammar={'title': '去, 来, 回 et 坐 (prendre un transport)',
  'explain': '去 (qù) = aller là-bas, 来 (lái) = venir ici, 回 (huí) = rentrer. Pour dire comment on se déplace, on met 坐 + transport avant le verbe : 坐出租车去 = y aller en taxi.',
  'examples': [ex('我去医院。', 'Wǒ qù yīyuàn.', 'Je vais à l’hôpital.'), ex('你来我家吗？', 'Nǐ lái wǒ jiā ma?', 'Tu viens chez moi ?'), ex('我坐出租车回家。', 'Wǒ zuò chūzūchē huí jiā.', 'Je rentre en taxi.'), ex('他坐飞机去北京。', 'Tā zuò fēijī qù Běijīng.', 'Il va à Pékin en avion.')],
  'tip': '会 (huì) = savoir faire (appris), 能 (néng) = pouvoir (avoir la possibilité).'},
 items=items('''
k08_qu | 去 | qu | 4 | | Aller
k08_lai | 来 | lai | 2 | | Venir
k08_hui | 回 | hui | 2 | | Revenir, rentrer
k08_zuo | 坐 | zuo | 4 | | S’asseoir, prendre (un transport)
k08_chuzuche | 出租车 | chu-zu-che | 1 1 1 | | Taxi
k08_feiji | 飞机 | fei-ji | 1 1 | | Avion
k08_kai | 开 | kai | 1 | | Ouvrir, conduire
k08_dadianhua | 打电话 | da dian-hua | 3 4 4 | | Téléphoner
k08_wei | 喂 | wei | 4 | | Allô
k08_zaijian | 再见 | zai-jian | 4 4 | | Au revoir
k08_neng | 能 | neng | 2 | | Pouvoir
k08_hui2 | 会 | hui | 4 | | Savoir (faire)
k08_zenme | 怎么 | zen-me | 3 0 | | Comment
k08_s_chuzuche | 我坐出租车去医院 | wo zuo chu-zu-che qu yi-yuan | 3 4 1 1 1 4 1 4 | | Je vais à l’hôpital en taxi
k08_s_zenme | 你怎么回家 | ni zen-me hui jia | 3 3 0 2 1 | 2 3 0 2 1 | Tu rentres comment ? | Après le poste, demande à un collègue : 你怎么回家？
'''),
 pairs=[pair(('坐', 'zuo', 4, 's’asseoir'), ('左', 'zuo', 3, 'gauche'))],
 chars=chars('''
去 | qù | aller | 土 | terre
来 | lái | venir | 木 | arbre
回 | huí | revenir | 囗 | enclos
坐 | zuò | s’asseoir | 土 | terre
车 | chē | voiture | 车 | voiture
机 | jī | machine | 木 | arbre
电 | diàn | électricité | 田 | champ
话 | huà | parole | 讠 | parole
'''),
 convs=[conv('hsk1-telephone', 'Un appel d’une amie', '朋友', 'Amie', 'Ton téléphone sonne : c’est une amie chinoise.', {
  'a': node('喂，你好！你在哪儿？', 'Wèi, nǐ hǎo! Nǐ zài nǎr?', 'Allô, bonjour ! Tu es où ?', [
     o('我在家。你呢？', 'Wǒ zài jiā. Nǐ ne?', 'Je suis à la maison. Et toi ?', True, 'b'),
     o('我很好。', 'Wǒ hěn hǎo.', 'Je vais bien.', fix='你在哪儿 = où es-tu ? Réponds « 我在家 ».')]),
  'b': node('我在学校。你明天来学校吗？', 'Wǒ zài xuéxiào. Nǐ míngtiān lái xuéxiào ma?', 'Je suis à l’école. Tu viens à l’école demain ?', [
     o('来，我坐出租车来。', 'Lái, wǒ zuò chūzūchē lái.', 'Oui, je viens en taxi.', True, 'end'),
     o('不来，明天我工作。', 'Bù lái, míngtiān wǒ gōngzuò.', 'Non, demain je travaille.', True, 'end'),
     o('我坐飞机。', 'Wǒ zuò fēijī.', 'Je prends l’avion.', fix='Elle demande si tu viens : réponds 来 (oui) ou 不来 (non).')]),
  'end': node('好的，再见！', 'Hǎo de, zàijiàn!', 'D’accord, au revoir !', end=True)})]))

# ---------------- HSK 1 · 9 ----------------
PACKS.append(dict(id='hsk1-09', file='hsk1-09-activites.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 9 — Ce qu’on fait',
 desc='Regarder, écouter, lire, écrire, travailler, étudier le chinois. 18 mots HSK 1.',
 grammar={'title': '了 : l’action est faite',
  'explain': '了 (le) après un verbe indique que l’action est terminée : 我吃了 = j’ai mangé. Pour dire qu’on ne l’a pas fait, on utilise 没 devant le verbe, sans 了 : 我没吃.',
  'examples': [ex('我吃了。', 'Wǒ chī le.', 'J’ai mangé.'), ex('我买了一本书。', 'Wǒ mǎi le yì běn shū.', 'J’ai acheté un livre.'), ex('你看了吗？', 'Nǐ kàn le ma?', 'Tu l’as vu ?'), ex('我没看。', 'Wǒ méi kàn.', 'Je ne l’ai pas vu.')],
  'tip': '在 + verbe = « en train de » : 我在学习汉语 = je suis en train d’apprendre le chinois.'},
 items=items('''
k09_kan | 看 | kan | 4 | | Regarder, lire
k09_kanjian | 看见 | kan-jian | 4 4 | | Voir
k09_ting | 听 | ting | 1 | | Écouter
k09_shuo | 说 | shuo | 1 | | Parler, dire
k09_du | 读 | du | 2 | | Lire (à voix haute)
k09_xie | 写 | xie | 3 | | Écrire
k09_zi | 字 | zi | 4 | | Caractère
k09_shu | 书 | shu | 1 | | Livre
k09_ben | 本 | ben | 3 | | Classificateur des livres
k09_xuexi | 学习 | xue-xi | 2 2 | | Étudier
k09_hanyu | 汉语 | Han-yu | 4 3 | | Langue chinoise
k09_gongzuo | 工作 | gong-zuo | 1 4 | | Travailler, travail
k09_zuo | 做 | zuo | 4 | | Faire
k09_shuijiao | 睡觉 | shui-jiao | 4 4 | | Dormir
k09_diannao | 电脑 | dian-nao | 4 3 | | Ordinateur
k09_dianshi | 电视 | dian-shi | 4 4 | | Télévision
k09_dianying | 电影 | dian-ying | 4 3 | | Film
k09_le | 了 | le | 0 | | Action terminée
k09_s_xuexi | 我在学习汉语 | wo zai xue-xi Han-yu | 3 4 2 2 4 3 | | J’apprends le chinois | Dis à un collègue chinois que tu apprends sa langue : 我在学习汉语。
k09_s_dianying | 我看了一个电影 | wo kan le yi ge dian-ying | 3 4 0 2 0 4 3 | | J’ai regardé un film
'''),
 pairs=[pair(('书', 'shu', 1, 'livre'), ('树', 'shu', 4, 'arbre'))],
 chars=chars('''
看 | kàn | regarder | 目 | œil
听 | tīng | écouter | 口 | bouche
说 | shuō | parler | 讠 | parole
读 | dú | lire | 讠 | parole
写 | xiě | écrire | 冖 | couvercle
字 | zì | caractère | 子 | enfant
学 | xué | étudier | 子 | enfant
做 | zuò | faire | 亻 | personne
'''),
 convs=[conv('hsk1-activites', 'Ton week-end', '同事', 'Collègue', 'Lundi matin, un collègue te demande ce que tu as fait.', {
  'a': node('昨天你做什么了？', 'Zuótiān nǐ zuò shénme le?', 'Qu’est-ce que tu as fait hier ?', [
     o('我看了一个电影。', 'Wǒ kàn le yí ge diànyǐng.', 'J’ai regardé un film.', True, 'b'),
     o('我明天看电影。', 'Wǒ míngtiān kàn diànyǐng.', 'Demain je regarde un film.', fix='Il parle d’hier (昨天) : utilise 了 : « 我看了一个电影 ».')]),
  'b': node('你会说汉语吗？', 'Nǐ huì shuō Hànyǔ ma?', 'Tu parles chinois ?', [
     o('会一点儿，我在学习。', 'Huì yìdiǎnr, wǒ zài xuéxí.', 'Un peu, je suis en train d’apprendre.', True, 'end'),
     o('我在睡觉。', 'Wǒ zài shuìjiào.', 'Je suis en train de dormir.', fix='Il demande si tu parles chinois : « 会一点儿 » (un peu).')]),
  'end': node('你说得很好！', 'Nǐ shuō de hěn hǎo!', 'Tu le parles très bien !', end=True)})]))

# ---------------- HSK 1 · 10 ----------------
PACKS.append(dict(id='hsk1-10', file='hsk1-10-meteo-politesse.json', branch='hsk', level=1, publish=False,
 title='HSK 1 · 10 — Météo, humeur et politesse',
 desc='Le temps qu’il fait, décrire, remercier, s’excuser, poser des questions. 19 mots HSK 1 : le HSK 1 est complet !',
 grammar={'title': '很 + adjectif, et les questions avec 吗 / 呢',
  'explain': 'Devant un adjectif, on met presque toujours 很 (hěn) : 我很好. On n’utilise pas 是 avec un adjectif. Pour poser une question oui/non, on ajoute 吗 (ma) à la fin. Pour renvoyer la question (« et toi ? »), on ajoute 呢 (ne).',
  'examples': [ex('天气很好。', 'Tiānqì hěn hǎo.', 'Il fait beau.'), ex('你好吗？', 'Nǐ hǎo ma?', 'Tu vas bien ?'), ex('我很好，你呢？', 'Wǒ hěn hǎo, nǐ ne?', 'Je vais bien, et toi ?'), ex('我们都很高兴。', 'Wǒmen dōu hěn gāoxìng.', 'Nous sommes tous contents.')],
  'tip': 'Avec 很, ne mets pas 是 : 我很高兴, jamais 我是高兴.'},
 items=items('''
k10_tianqi | 天气 | tian-qi | 1 4 | | Temps (météo)
k10_leng | 冷 | leng | 3 | | Froid
k10_re | 热 | re | 4 | | Chaud
k10_xiayu | 下雨 | xia-yu | 4 3 | | Pleuvoir
k10_da | 大 | da | 4 | | Grand
k10_xiao | 小 | xiao | 3 | | Petit
k10_hen | 很 | hen | 3 | | Très
k10_hao | 好 | hao | 3 | | Bien, bon
k10_zenmeyang | 怎么样 | zen-me-yang | 3 0 4 | | Comment ça ? Ça va ?
k10_gou | 狗 | gou | 3 | | Chien
k10_mao | 猫 | mao | 1 | | Chat
k10_dou | 都 | dou | 1 | | Tous
k10_he | 和 | he | 2 | | Et (entre deux noms)
k10_ma | 吗 | ma | 0 | | Particule de question
k10_ne | 呢 | ne | 0 | | Et… ? (renvoyer la question)
k10_bukeqi | 不客气 | bu ke-qi | 2 4 0 | | De rien
k10_meiguanxi | 没关系 | mei guan-xi | 2 1 0 | | Ce n’est pas grave
k10_yizi | 椅子 | yi-zi | 3 0 | | Chaise
k10_zhuozi | 桌子 | zhuo-zi | 1 0 | | Table
k10_s_tianqi | 今天天气怎么样 | jin-tian tian-qi zen-me-yang | 1 1 1 4 3 0 4 | | Quel temps fait-il aujourd’hui ? | Le matin, lance la conversation : 今天天气怎么样？
k10_s_nine | 我很好，你呢 | wo hen hao ni ne | 3 3 3 3 0 | 2 2 3 3 0 | Je vais bien, et toi ?
'''),
 pairs=[pair(('猫', 'mao', 1, 'chat'), ('毛', 'mao', 2, 'poil'))],
 chars=chars('''
冷 | lěng | froid | 冫 | glace
热 | rè | chaud | 灬 | feu
雨 | yǔ | pluie | 雨 | pluie
大 | dà | grand | 大 | grand
小 | xiǎo | petit | 小 | petit
好 | hǎo | bien | 女 | femme
狗 | gǒu | chien | 犭 | animal
猫 | māo | chat | 犭 | animal
'''),
 convs=[conv('hsk1-meteo', 'Il fait chaud !', '同事', 'Collègue', 'Il fait très chaud dans l’atelier. Une collègue engage la conversation.', {
  'a': node('今天天气怎么样？', 'Jīntiān tiānqì zěnmeyàng?', 'Quel temps fait-il aujourd’hui ?', [
     o('今天很热。', 'Jīntiān hěn rè.', 'Il fait très chaud.', True, 'b'),
     o('今天星期五。', 'Jīntiān xīngqīwǔ.', 'Aujourd’hui c’est vendredi.', fix='天气 = le temps qu’il fait : « 很热 » (chaud), « 很冷 » (froid).')]),
  'b': node('北京很冷，下雨了。你喜欢下雨吗？', 'Běijīng hěn lěng, xià yǔ le. Nǐ xǐhuan xià yǔ ma?', 'À Pékin il fait froid, il pleut. Tu aimes la pluie ?', [
     o('不喜欢。你呢？', 'Bù xǐhuan. Nǐ ne?', 'Non. Et toi ?', True, 'end'),
     o('喜欢！', 'Xǐhuan!', 'Oui, j’aime !', True, 'end'),
     o('我是下雨。', 'Wǒ shì xià yǔ.', '(phrase incorrecte)', fix='Réponds avec 喜欢 (j’aime) ou 不喜欢 (je n’aime pas).')]),
  'end': node('哈哈，好的！', 'Hāhā, hǎo de!', 'Haha, d’accord !', end=True)})],
 bonus=[{'h': '恭喜', 'p': 'gōngxǐ', 'fr': 'Félicitations !', 'note': 'Tu as terminé le vocabulaire du HSK 1. 恭喜！'}]))

# ---------------- HSK 2 · 1 ----------------
PACKS.append(dict(id='hsk2-01', file='hsk2-01-famille.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 1 — Frères, sœurs et présentations',
 desc='Parler de tes frères et sœurs, de ton mari ou de ta femme, et te présenter poliment. 16 mots HSK 2.',
 grammar={'title': '也 : « aussi »',
  'explain': '也 (yě) veut dire « aussi ». Il se place toujours juste avant le verbe (ou avant 很 + adjectif), jamais au début ni à la fin de la phrase. Pour dire « moi aussi », on dit 我也是 (mot à mot « moi aussi suis »).',
  'examples': [ex('我也是多哥人。', 'Wǒ yě shì Duōgē rén.', 'Je suis Togolaise aussi.'), ex('她也有一个哥哥。', 'Tā yě yǒu yí ge gēge.', 'Elle aussi a un grand frère.'), ex('我们也很高兴。', 'Wǒmen yě hěn gāoxìng.', 'Nous aussi, nous sommes contents.'), ex('——我很忙。——我也是。', '— Wǒ hěn máng. — Wǒ yě shì.', '— Je suis très occupée. — Moi aussi.')],
  'tip': 'Ne dis jamais 也我 : la personne vient d’abord, puis 也, puis le verbe. 我也去 = moi aussi j’y vais.'},
 items=items('''
h201_gege | 哥哥 | ge-ge | 1 0 | | Grand frère
h201_jiejie | 姐姐 | jie-jie | 3 0 | | Grande sœur
h201_didi | 弟弟 | di-di | 4 0 | | Petit frère
h201_meimei | 妹妹 | mei-mei | 4 0 | | Petite sœur
h201_zhangfu | 丈夫 | zhang-fu | 4 0 | | Mari
h201_qizi | 妻子 | qi-zi | 1 0 | | Épouse
h201_haizi | 孩子 | hai-zi | 2 0 | | Enfant
h201_nanren | 男人 | nan-ren | 2 2 | | Homme
h201_nvren | 女人 | nv-ren | 3 2 | | Femme
h201_nin | 您 | nin | 2 | | Vous (poli, à une seule personne)
h201_xing | 姓 | xing | 4 | | Avoir pour nom de famille
h201_jieshao | 介绍 | jie-shao | 4 4 | | Présenter
h201_dajia | 大家 | da-jia | 4 1 | | Tout le monde
h201_ye | 也 | ye | 3 | | Aussi
h201_shengri | 生日 | sheng-ri | 1 4 | | Anniversaire
h201_kuaile | 快乐 | kuai-le | 4 4 | | Joyeux, heureux
h201_s_guixing | 您贵姓 | nin gui xing | 2 4 4 | | Quel est votre nom de famille ? (poli) | Demande poliment son nom de famille à un chef chinois que tu ne connais pas : 您贵姓？
h201_s_jieshao | 我来介绍一下 | wo lai jie-shao yi-xia | 3 2 4 4 2 4 | | Je vous présente…
h201_s_shengri | 生日快乐 | sheng-ri kuai-le | 1 4 4 4 | | Joyeux anniversaire ! | Le jour de l’anniversaire d’une collègue, dis-lui : 生日快乐！
h201_s_yeshi | 我也是 | wo ye shi | 3 3 4 | 2 3 4 | Moi aussi
'''),
 pairs=[pair(('妹', 'mei', 4, 'petite sœur'), ('没', 'mei', 2, 'ne… pas (avoir)')), pair(('姐', 'jie', 3, 'grande sœur'), ('介', 'jie', 4, 'présenter'))],
 chars=chars('''
哥 | gē | grand frère | 口 | bouche
姐 | jiě | grande sœur | 女 | femme
弟 | dì | petit frère | 弓 | arc
妹 | mèi | petite sœur | 女 | femme
孩 | hái | enfant | 子 | enfant
男 | nán | homme | 田 | champ
您 | nín | vous (poli) | 心 | cœur
姓 | xìng | nom de famille | 女 | femme
'''),
 convs=[conv('hsk2-famille', 'Le nouveau chef d’équipe', '新组长', 'Nouveau chef d’équipe', 'Un nouveau chef d’équipe chinois arrive. Il veut connaître tout le monde.', {
  'a': node('大家好！我姓李。你叫什么名字？', 'Dàjiā hǎo! Wǒ xìng Lǐ. Nǐ jiào shénme míngzi?', 'Bonjour à tous ! Je m’appelle Li (nom de famille). Comment tu t’appelles ?', [
     o('您好，李组长！我叫{name}。', 'Nín hǎo, Lǐ zǔzhǎng! Wǒ jiào {name}.', 'Bonjour, chef Li ! Je m’appelle {name}.', True, 'b'),
     o('我姓多哥。', 'Wǒ xìng Duōgē.', 'Mon nom de famille est Togo.', fix='姓 = le nom de famille, et 多哥 c’est ton pays ! Réponds « 我叫{name} ».')]),
  'b': node('你有孩子吗？', 'Nǐ yǒu háizi ma?', 'Tu as des enfants ?', [
     o('有，我有一个儿子。', 'Yǒu, wǒ yǒu yí ge érzi.', 'Oui, j’ai un fils.', True, 'c'),
     o('没有，我没有孩子。', 'Méiyǒu, wǒ méiyǒu háizi.', 'Non, je n’ai pas d’enfant.', True, 'c'),
     o('我是孩子。', 'Wǒ shì háizi.', 'Je suis une enfant.', fix='Il demande si tu AS des enfants : réponds avec 有 ou 没有.')]),
  'c': node('我也有一个孩子。你有哥哥姐姐吗？', 'Wǒ yě yǒu yí ge háizi. Nǐ yǒu gēge jiějie ma?', 'Moi aussi, j’ai un enfant. Tu as des grands frères ou des grandes sœurs ?', [
     o('我有一个哥哥，也有一个妹妹。', 'Wǒ yǒu yí ge gēge, yě yǒu yí ge mèimei.', 'J’ai un grand frère, et aussi une petite sœur.', True, 'end'),
     o('我有一个哥哥，我有也一个妹妹。', 'Wǒ yǒu yí ge gēge, wǒ yǒu yě yí ge mèimei.', '(erreur de place)', fix='也 se met juste AVANT le verbe : « 我也有一个妹妹 ».')]),
  'end': node('认识大家很高兴！', 'Rènshi dàjiā hěn gāoxìng!', 'Ravi de vous connaître tous !', end=True)})],
 bonus=[{'h': '兄弟姐妹', 'p': 'xiōngdì jiěmèi', 'fr': 'Frères et sœurs', 'note': 'Pour demander : 你有兄弟姐妹吗？ (Tu as des frères et sœurs ?)'}]))

# ---------------- HSK 2 · 2 ----------------
PACKS.append(dict(id='hsk2-02', file='hsk2-02-sante.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 2 — Ma journée et ma santé',
 desc='Dire quand tu te lèves, si tu es fatiguée ou malade, et expliquer pourquoi. 15 mots HSK 2.',
 grammar={'title': '因为… 所以… : « parce que… donc… »',
  'explain': 'En chinois, on aime dire la cause d’abord : 因为 (yīnwèi) = parce que, puis la conséquence avec 所以 (suǒyǐ) = donc. On peut garder les deux mots dans la même phrase, ce qui est impossible en français.',
  'examples': [ex('因为我生病了，所以没去上班。', 'Yīnwèi wǒ shēngbìng le, suǒyǐ méi qù shàngbān.', 'Comme j’étais malade, je ne suis pas allée travailler.'), ex('因为很忙，所以我很累。', 'Yīnwèi hěn máng, suǒyǐ wǒ hěn lèi.', 'J’ai beaucoup de travail, donc je suis très fatiguée.'), ex('我今天很累，因为我早上五点起床。', 'Wǒ jīntiān hěn lèi, yīnwèi wǒ zǎoshang wǔ diǎn qǐchuáng.', 'Je suis fatiguée aujourd’hui, parce que je me suis levée à 5 h.')],
  'tip': 'Tu peux aussi n’utiliser qu’un seul des deux : « 因为… » tout seul, ou « …，所以… » tout seul.'},
 items=items('''
h202_qichuang | 起床 | qi-chuang | 3 2 | | Se lever (du lit)
h202_zaoshang | 早上 | zao-shang | 3 0 | | Le matin (tôt)
h202_wanshang | 晚上 | wan-shang | 3 0 | | Le soir
h202_xiaoshi | 小时 | xiao-shi | 3 2 | | Heure (durée)
h202_shijian | 时间 | shi-jian | 2 1 | | Temps, moment libre
h202_mang | 忙 | mang | 2 | | Occupé
h202_lei | 累 | lei | 4 | | Fatigué
h202_shenti | 身体 | shen-ti | 1 3 | | Corps, santé
h202_yanjing | 眼睛 | yan-jing | 3 0 | | Yeux
h202_shengbing | 生病 | sheng-bing | 1 4 | | Tomber malade
h202_yao | 药 | yao | 4 | | Médicament
h202_juede | 觉得 | jue-de | 2 0 | | Trouver, se sentir
h202_yijing | 已经 | yi-jing | 3 1 | | Déjà
h202_yinwei | 因为 | yin-wei | 1 4 | | Parce que
h202_suoyi | 所以 | suo-yi | 3 3 | 2 3 | Donc, c’est pourquoi
h202_s_lei | 我觉得很累 | wo jue-de hen lei | 3 2 0 3 4 | | Je me sens très fatiguée
h202_s_bingle | 我生病了 | wo sheng-bing le | 3 1 4 0 | | Je suis malade | Si un jour tu es malade, préviens ton chef par message : 我生病了，今天不能上班。
h202_s_shijian | 你有时间吗 | ni you shi-jian ma | 3 3 2 1 0 | 2 3 2 1 0 | Tu as un moment ? | Avant de poser une question à un collègue chinois, demande-lui d’abord : 你有时间吗？
'''),
 pairs=[pair(('时', 'shi', 2, 'moment'), ('是', 'shi', 4, 'être')), pair(('眼', 'yan', 3, 'œil'), ('颜', 'yan', 2, 'couleur'))],
 chars=chars('''
床 | chuáng | lit | 广 | abri
早 | zǎo | tôt | 日 | soleil
晚 | wǎn | soir, tard | 日 | soleil
忙 | máng | occupé | 忄 | cœur
累 | lèi | fatigué | 糸 | soie
体 | tǐ | corps | 亻 | personne
眼 | yǎn | œil | 目 | œil
药 | yào | médicament | 艹 | herbe
'''),
 convs=[conv('hsk2-sante', 'Pas en forme aujourd’hui', '组长', 'Chef d’équipe', 'Ce matin, ton chef d’équipe voit que tu n’as pas l’air bien.', {
  'a': node('你怎么了？身体不好吗？', 'Nǐ zěnme le? Shēntǐ bù hǎo ma?', 'Qu’est-ce qui ne va pas ? Tu ne te sens pas bien ?', [
     o('我生病了，觉得很累。', 'Wǒ shēngbìng le, juéde hěn lèi.', 'Je suis malade, je me sens très fatiguée.', True, 'b'),
     o('我很忙。', 'Wǒ hěn máng.', 'Je suis très occupée.', fix='Il demande si tu te sens mal. Si tu es malade, dis « 我生病了 ».')]),
  'b': node('你吃药了吗？', 'Nǐ chī yào le ma?', 'Tu as pris un médicament ?', [
     o('已经吃了。', 'Yǐjīng chī le.', 'Oui, déjà.', True, 'c'),
     o('还没有。', 'Hái méiyǒu.', 'Pas encore.', True, 'c'),
     o('我吃饭了。', 'Wǒ chī fàn le.', 'J’ai mangé.', fix='药 (yào) = médicament, 饭 (fàn) = repas. Réponds « 已经吃了 » (déjà pris).')]),
  'c': node('因为你生病了，所以今天下午休息吧。', 'Yīnwèi nǐ shēngbìng le, suǒyǐ jīntiān xiàwǔ xiūxi ba.', 'Comme tu es malade, repose-toi cet après-midi.', [
     o('谢谢组长！', 'Xièxie zǔzhǎng!', 'Merci, chef !', True, 'end'),
     o('不客气！', 'Bú kèqi!', 'De rien !', fix='C’est toi qui remercies : « 谢谢组长！ ». 不客气 = de rien.')]),
  'end': node('不客气，明天见！', 'Bú kèqi, míngtiān jiàn!', 'De rien, à demain !', end=True)})],
 bonus=[{'h': '多喝水', 'p': 'duō hē shuǐ', 'fr': 'Bois beaucoup d’eau', 'note': 'Le conseil que les Chinois donnent pour presque tous les petits problèmes de santé !'}]))

# ---------------- HSK 2 · 3 ----------------
PACKS.append(dict(id='hsk2-03', file='hsk2-03-comparer.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 3 — Prix, couleurs et comparaisons',
 desc='Vendre et acheter, dire les couleurs, les grands prix, et comparer deux choses. 16 mots HSK 2.',
 grammar={'title': '比 : comparer deux choses',
  'explain': 'Pour dire « A est plus … que B », on dit : A 比 (bǐ) B + adjectif. 这双比那双贵 = celle-ci est plus chère que celle-là. L’adjectif ne change pas et se met tout à la fin.',
  'examples': [ex('这双鞋比那双贵。', 'Zhè shuāng xié bǐ nà shuāng guì.', 'Cette paire est plus chère que celle-là.'), ex('今天比昨天热。', 'Jīntiān bǐ zuótiān rè.', 'Aujourd’hui il fait plus chaud qu’hier.'), ex('他比我忙。', 'Tā bǐ wǒ máng.', 'Il est plus occupé que moi.'), ex('黑的比白的便宜多了。', 'Hēi de bǐ bái de piányi duō le.', 'Le noir est beaucoup moins cher que le blanc.')],
  'tip': 'Avec 比, ne mets jamais 很 : 他比我忙, pas 他比我很忙. Pour « beaucoup plus », ajoute 多了 à la fin.'},
 items=items('''
h203_mai | 卖 | mai | 4 | | Vendre
h203_gui | 贵 | gui | 4 | | Cher
h203_pianyi | 便宜 | pian-yi | 2 0 | | Pas cher, bon marché
h203_yuan | 元 | yuan | 2 | | Yuan (monnaie, à l’écrit)
h203_bai | 百 | bai | 3 | | Cent
h203_qian | 千 | qian | 1 | | Mille
h203_jian | 件 | jian | 4 | | Classificateur des vêtements et des affaires
h203_zhang | 张 | zhang | 1 | | Classificateur des choses plates (papier, billet)
h203_gongjin | 公斤 | gong-jin | 1 1 | | Kilo
h203_yanse | 颜色 | yan-se | 2 4 | | Couleur
h203_bai2 | 白 | bai | 2 | | Blanc
h203_hei | 黑 | hei | 1 | | Noir
h203_hong | 红 | hong | 2 | | Rouge
h203_xin | 新 | xin | 1 | | Neuf, nouveau
h203_chuan | 穿 | chuan | 1 | | Porter (vêtements, chaussures)
h203_bi | 比 | bi | 3 | | Plus… que (comparer)
h203_s_bi | 这件比那件便宜 | zhe jian bi na jian pian-yi | 4 4 3 4 4 2 0 | | Celui-ci est moins cher que celui-là
h203_s_heise | 有没有黑色的 | you mei you hei-se de | 3 2 3 1 4 0 | | Vous l’avez en noir ? | Dans une boutique, demande une autre couleur : 有没有黑色的？ (ou 红色的, 白色的)
h203_s_hao | 我穿三十八号 | wo chuan san-shi-ba hao | 3 1 1 2 1 4 | | Je chausse du 38 | Au magasin de chaussures, donne ta pointure en chinois : 我穿…号。
'''),
 pairs=[pair(('买', 'mai', 3, 'acheter'), ('卖', 'mai', 4, 'vendre')), pair(('白', 'bai', 2, 'blanc'), ('百', 'bai', 3, 'cent'))],
 chars=chars('''
卖 | mài | vendre | 十 | dix
贵 | guì | cher | 贝 | coquillage
元 | yuán | yuan | 儿 | jambes
件 | jiàn | pièce, article | 亻 | personne
张 | zhāng | feuille | 弓 | arc
颜 | yán | couleur, visage | 页 | tête
黑 | hēi | noir | 黑 | noir
新 | xīn | nouveau | 斤 | hache
'''),
 convs=[conv('hsk2-comparer', 'Des chaussures pour toi', '店员', 'Vendeuse', 'Pour une fois, c’est toi qui achètes des chaussures, dans un magasin tenu par une Chinoise.', {
  'a': node('你好，你想买什么？', 'Nǐ hǎo, nǐ xiǎng mǎi shénme?', 'Bonjour, qu’est-ce que tu veux acheter ?', [
     o('我想买一双鞋。', 'Wǒ xiǎng mǎi yì shuāng xié.', 'Je voudrais acheter une paire de chaussures.', True, 'b'),
     o('我想卖一双鞋。', 'Wǒ xiǎng mài yì shuāng xié.', 'Je voudrais vendre une paire de chaussures.', fix='卖 (mài, 4e ton) = vendre. Acheter, c’est 买 (mǎi, 3e ton) : « 我想买一双鞋 ».')]),
  'b': node('你穿多少号？', 'Nǐ chuān duōshao hào?', 'Tu fais quelle pointure ?', [
     o('我穿三十八号。', 'Wǒ chuān sānshíbā hào.', 'Je chausse du 38.', True, 'c'),
     o('我三十八岁。', 'Wǒ sānshíbā suì.', 'J’ai 38 ans.', fix='号 = la pointure (ou la taille). 岁, c’est l’âge ! « 我穿三十八号 ».')]),
  'c': node('这双白的三百元，那双黑的两百元。', 'Zhè shuāng bái de sānbǎi yuán, nà shuāng hēi de liǎngbǎi yuán.', 'Celle-ci, la blanche, fait 300 yuans ; celle-là, la noire, 200 yuans.', [
     o('黑的比白的便宜，我要黑的。', 'Hēi de bǐ bái de piányi, wǒ yào hēi de.', 'La noire est moins chère que la blanche, je prends la noire.', True, 'end'),
     o('白的比黑的便宜。', 'Bái de bǐ hēi de piányi.', 'La blanche est moins chère que la noire.', fix='300 c’est plus que 200 : c’est la noire qui est moins chère. « 黑的比白的便宜 ».')]),
  'end': node('好的，这双是新的。给你！', 'Hǎo de, zhè shuāng shì xīn de. Gěi nǐ!', 'D’accord, celle-ci est neuve. Voilà !', end=True)})],
 bonus=[{'h': '物美价廉', 'p': 'wùměi jiàlián', 'fr': 'Bonne qualité, petit prix', 'note': 'Ce que tout le monde cherche au marché ! Les vendeurs l’écrivent souvent sur leurs pancartes.'}]))

# ---------------- HSK 2 · 4 ----------------
PACKS.append(dict(id='hsk2-04', file='hsk2-04-chemin.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 4 — Trouver son chemin',
 desc='Dire si c’est loin ou près, à gauche ou à droite, et expliquer un trajet. 16 mots HSK 2.',
 grammar={'title': '离 et 从… 到… : la distance et le trajet',
  'explain': 'Pour la distance entre deux endroits, on dit : A 离 (lí) B 很远 / 很近. 我家离工厂很近 = ma maison est près de l’usine. Pour un trajet ou une durée, du début jusqu’à la fin, on dit : 从 (cóng) A 到 (dào) B.',
  'examples': [ex('我家离工厂很近。', 'Wǒ jiā lí gōngchǎng hěn jìn.', 'Ma maison est près de l’usine.'), ex('机场离这儿很远。', 'Jīchǎng lí zhèr hěn yuǎn.', 'L’aéroport est loin d’ici.'), ex('从我家到工厂走路十分钟。', 'Cóng wǒ jiā dào gōngchǎng zǒulù shí fēnzhōng.', 'De chez moi à l’usine, il faut dix minutes à pied.'), ex('我们从八点工作到五点。', 'Wǒmen cóng bā diǎn gōngzuò dào wǔ diǎn.', 'Nous travaillons de 8 h à 17 h.')],
  'tip': '离 = la distance, sans mouvement. 从…到… = un mouvement ou une durée, du départ à l’arrivée.'},
 items=items('''
h204_li | 离 | li | 2 | | À… de (distance)
h204_yuan | 远 | yuan | 3 | | Loin
h204_jin | 近 | jin | 4 | | Près
h204_lu | 路 | lu | 4 | | Route, chemin
h204_zou | 走 | zou | 3 | | Marcher, partir
h204_dao | 到 | dao | 4 | | Arriver ; jusqu’à
h204_cong | 从 | cong | 2 | | Depuis, à partir de
h204_zuobian | 左边 | zuo-bian | 3 1 | | À gauche
h204_youbian | 右边 | you-bian | 4 1 | | À droite
h204_pangbian | 旁边 | pang-bian | 2 1 | | À côté
h204_men | 门 | men | 2 | | Porte
h204_gongjiao | 公共汽车 | gong-gong qi-che | 1 4 4 1 | | Bus
h204_zixingche | 自行车 | zi-xing-che | 4 2 1 | | Vélo
h204_piao | 票 | piao | 4 | | Billet, ticket
h204_binguan | 宾馆 | bin-guan | 1 3 | | Hôtel
h204_fangjian | 房间 | fang-jian | 2 1 | | Chambre, pièce
h204_s_li | 你家离工厂远吗 | ni jia li gong-chang yuan ma | 3 1 2 1 3 3 0 | 3 1 2 1 2 3 0 | Ta maison est loin de l’usine ? | À la pause, demande à un collègue : 你家离工厂远吗？
h204_s_cong | 从家到工厂 | cong jia dao gong-chang | 2 1 4 1 3 | | De la maison jusqu’à l’usine
h204_s_zoulu | 走路十分钟 | zou-lu shi fen-zhong | 3 4 2 1 1 | | Dix minutes à pied | Explique à un collègue ton trajet du matin : 从家到工厂走路…分钟。
'''),
 pairs=[pair(('近', 'jin', 4, 'près'), ('今', 'jin', 1, 'aujourd’hui')), pair(('远', 'yuan', 3, 'loin'), ('元', 'yuan', 2, 'yuan'))],
 chars=chars('''
远 | yuǎn | loin | 辶 | marche
近 | jìn | près | 辶 | marche
路 | lù | route | 足 | pied
走 | zǒu | marcher | 走 | marcher
左 | zuǒ | gauche | 工 | travail
右 | yòu | droite | 口 | bouche
门 | mén | porte | 门 | porte
车 | chē | véhicule | 车 | char
'''),
 convs=[conv('hsk2-chemin', 'Le chemin de l’hôtel', '客人', 'Visiteur', 'Un visiteur chinois sort de l’usine. Il cherche son hôtel.', {
  'a': node('请问，宾馆离这儿远吗？', 'Qǐngwèn, bīnguǎn lí zhèr yuǎn ma?', 'Excuse-moi, l’hôtel est loin d’ici ?', [
     o('不远，很近。', 'Bù yuǎn, hěn jìn.', 'Non, c’est tout près.', True, 'b'),
     o('我不在宾馆。', 'Wǒ bú zài bīnguǎn.', 'Je ne suis pas à l’hôtel.', fix='Il demande si c’est loin : réponds « 很近 » (près) ou « 很远 » (loin).')]),
  'b': node('怎么走？', 'Zěnme zǒu?', 'Comment j’y vais ?', [
     o('宾馆在商店旁边。', 'Bīnguǎn zài shāngdiàn pángbiān.', 'L’hôtel est à côté du magasin.', True, 'c'),
     o('宾馆在左边。', 'Bīnguǎn zài zuǒbian.', 'L’hôtel est à gauche.', True, 'c'),
     o('我坐公共汽车。', 'Wǒ zuò gōnggòng qìchē.', 'Je prends le bus.', fix='Il demande le chemin vers l’hôtel : « 宾馆在商店旁边 » (à côté du magasin).')]),
  'c': node('走路要多长时间？', 'Zǒulù yào duō cháng shíjiān?', 'Ça prend combien de temps à pied ?', [
     o('走路五分钟。', 'Zǒulù wǔ fēnzhōng.', 'Cinq minutes à pied.', True, 'end'),
     o('五点。', 'Wǔ diǎn.', 'Cinq heures.', fix='Il demande une durée : « 五分钟 » (cinq minutes). 五点, c’est l’heure qu’il est.')]),
  'end': node('太好了，谢谢你！', 'Tài hǎo le, xièxie nǐ!', 'Super, merci !', end=True)})],
 bonus=[{'h': '一路平安', 'p': 'yílù píng’ān', 'fr': 'Bon voyage', 'note': 'Mot à mot « tout le chemin en paix ». À dire à quelqu’un qui part loin.'}]))

# ---------------- HSK 2 · 5 ----------------
PACKS.append(dict(id='hsk2-05', file='hsk2-05-comprendre.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 5 — Comprendre et s’entraider',
 desc='Demander, répondre, dire que tu as compris (ou pas), aider un collègue. 16 mots HSK 2.',
 grammar={'title': '正在 : « être en train de »',
  'explain': 'Pour dire qu’une action se passe en ce moment, mets 正在 (zhèngzài) juste avant le verbe. On peut ajouter 呢 (ne) à la fin : c’est plus naturel à l’oral. 我正在工作 = je suis en train de travailler.',
  'examples': [ex('我正在工作。', 'Wǒ zhèngzài gōngzuò.', 'Je suis en train de travailler.'), ex('他正在吃饭呢。', 'Tā zhèngzài chī fàn ne.', 'Il est en train de manger.'), ex('你正在做什么？', 'Nǐ zhèngzài zuò shénme?', 'Qu’est-ce que tu es en train de faire ?'), ex('组长正在找你。', 'Zǔzhǎng zhèngzài zhǎo nǐ.', 'Le chef d’équipe te cherche.')],
  'tip': 'À l’oral, on dit souvent juste 在 : 我在工作 veut dire la même chose.'},
 items=items('''
h205_bangzhu | 帮助 | bang-zhu | 1 4 | | Aider, aide
h205_gaosu | 告诉 | gao-su | 4 0 | | Dire à, informer
h205_wen | 问 | wen | 4 | | Demander (poser une question)
h205_huida | 回答 | hui-da | 2 2 | | Répondre
h205_dong | 懂 | dong | 3 | | Comprendre
h205_zhidao | 知道 | zhi-dao | 1 4 | | Savoir
h205_yisi | 意思 | yi-si | 4 0 | | Sens, signification
h205_zhunbei | 准备 | zhun-bei | 3 4 | | Préparer
h205_kaishi | 开始 | kai-shi | 1 3 | | Commencer
h205_wan | 完 | wan | 2 | | Finir (après un verbe : 做完)
h205_deng | 等 | deng | 3 | | Attendre
h205_zhao | 找 | zhao | 3 | | Chercher
h205_gei | 给 | gei | 3 | | Donner ; à, pour (quelqu’un)
h205_zhengzai | 正在 | zheng-zai | 4 4 | | Être en train de
h205_shiqing | 事情 | shi-qing | 4 0 | | Affaire, chose à faire
h205_cuo | 错 | cuo | 4 | | Faux, erreur
h205_s_yisi | 这是什么意思 | zhe shi shen-me yi-si | 4 4 2 0 4 0 | | Qu’est-ce que ça veut dire ? | Quand un collègue dit un mot que tu ne connais pas, demande-lui : 这是什么意思？
h205_s_deng | 请等一下 | qing deng yi-xia | 3 3 2 4 | 2 3 2 4 | Attends un instant, s’il te plaît
h205_s_bang | 我来帮你 | wo lai bang ni | 3 2 1 3 | | Je vais t’aider | Quand une collègue a trop de travail, propose-lui : 我来帮你！
'''),
 pairs=[pair(('问', 'wen', 4, 'demander'), ('文', 'wen', 2, 'écriture')), pair(('懂', 'dong', 3, 'comprendre'), ('东', 'dong', 1, 'est'))],
 chars=chars('''
帮 | bāng | aider | 巾 | tissu
告 | gào | annoncer | 口 | bouche
问 | wèn | demander | 门 | porte
答 | dá | répondre | 竹 | bambou
懂 | dǒng | comprendre | 忄 | cœur
知 | zhī | savoir | 矢 | flèche
完 | wán | finir | 宀 | toit
错 | cuò | erreur | 钅 | métal
'''),
 convs=[conv('hsk2-comprendre', 'Une consigne pas claire', '组长', 'Chef d’équipe', 'Ton chef d’équipe passe à ton poste et te donne une consigne.', {
  'a': node('{name}，你正在做什么？', '{name}, nǐ zhèngzài zuò shénme?', '{name}, qu’est-ce que tu es en train de faire ?', [
     o('我正在检查鞋。', 'Wǒ zhèngzài jiǎnchá xié.', 'Je suis en train de contrôler les chaussures.', True, 'b'),
     o('我是检查。', 'Wǒ shì jiǎnchá.', '(phrase incorrecte)', fix='Pour dire ce que tu fais en ce moment : « 我正在 + verbe », par exemple « 我正在检查鞋 ».')]),
  'b': node('好。做完了告诉我。', 'Hǎo. Zuò wán le gàosu wǒ.', 'Bien. Quand tu as fini, dis-le-moi.', [
     o('好的，我知道了。', 'Hǎo de, wǒ zhīdào le.', 'D’accord, c’est noté.', True, 'c'),
     o('对不起，我不懂。“告诉”是什么意思？', 'Duìbuqǐ, wǒ bù dǒng. “Gàosu” shì shénme yìsi?', 'Pardon, je ne comprends pas. Que veut dire « gàosu » ?', True, 'b2')]),
  'b2': node('“告诉”就是“说”。做完了跟我说。', '“Gàosu” jiùshì “shuō”. Zuò wán le gēn wǒ shuō.', '« Gàosu », c’est comme « dire ». Quand tu as fini, tu me le dis.', [
     o('懂了，谢谢！', 'Dǒng le, xièxie!', 'Compris, merci !', True, 'c')], coach='Bravo : demander 什么意思 quand on ne comprend pas, c’est la meilleure façon d’apprendre.'),
  'c': node('还有一件事情：你帮我找一下胶水。', 'Hái yǒu yí jiàn shìqing: nǐ bāng wǒ zhǎo yíxià jiāoshuǐ.', 'Autre chose : aide-moi à trouver la colle.', [
     o('好，请等一下。', 'Hǎo, qǐng děng yíxià.', 'D’accord, un instant.', True, 'end'),
     o('好，请找一下。', 'Hǎo, qǐng zhǎo yíxià.', 'D’accord, cherche un peu.', fix='C’est toi qui vas chercher la colle : « 好，请等一下 » (un instant).')]),
  'end': node('谢谢你的帮助！', 'Xièxie nǐ de bāngzhù!', 'Merci pour ton aide !', end=True)})],
 bonus=[{'h': '不懂就问', 'p': 'bù dǒng jiù wèn', 'fr': 'Si tu ne comprends pas, demande', 'note': 'Une phrase que les chefs chinois aiment bien : poser des questions, c’est bien travailler.'}]))

# ---------------- Branche Usine et travail ----------------
PACKS.append(dict(id='travail-compter', file='travail-01-compter.json', branch='travail', publish=True,
 title='Usine · Compter à l’atelier',
 desc='Compter les paires et les cartons, dire ce qui manque, faire le total de fin de poste.',
 grammar={'title': 'Les classificateurs (量词)',
  'explain': 'Entre le nombre et l’objet, on met un petit mot qui dépend de l’objet : 双 (une paire), 箱 (un carton), 个 (le mot passe-partout). Et « deux » devant un classificateur se dit 两 (liǎng), jamais 二 (èr).',
  'examples': [ex('一双鞋', 'yì shuāng xié', 'une paire de chaussures'), ex('两箱胶水', 'liǎng xiāng jiāoshuǐ', 'deux cartons de colle'), ex('三个人', 'sān ge rén', 'trois personnes'), ex('二十双', 'èrshí shuāng', 'vingt paires (ici 二, car c’est « vingt »)')],
  'tip': 'Si tu ne connais pas le bon classificateur, utilise 个 (ge) : on te comprendra.'},
 items=items('''
n_liang | 两 | liang | 3 | | Deux (devant une quantité)
n_yibai | 一百 | yi-bai | 4 3 | | Cent (100)
n_duoshaoshuang | 多少双 | duo-shao shuang | 1 0 1 | | Combien de paires ? | Demande à un collègue combien de paires il a faites : 多少双？
n_sanshishuang | 三十双鞋 | san-shi shuang xie | 1 2 1 2 | | Trente paires de chaussures
n_yixiang | 一箱 | yi xiang | 4 1 | | Un carton
n_bugou | 不够 | bu gou | 2 4 | | Pas assez
n_haicha | 还差五双 | hai cha wu shuang | 2 4 3 1 | | Il manque encore cinq paires
n_yigong | 一共多少 | yi-gong duo-shao | 2 4 1 0 | | Combien au total ? | À la fin du comptage, demande : 一共多少？
'''),
 pairs=[pair(('箱', 'xiang', 1, 'carton, caisse'), ('想', 'xiang', 3, 'vouloir'))],
 chars=chars('''
双 | shuāng | paire | 又 | main
箱 | xiāng | caisse | 竹 | bambou
鞋 | xié | chaussure | 革 | cuir
够 | gòu | assez | 夕 | soir
差 | chà | manquer | 工 | travail
共 | gòng | ensemble | 八 | huit
'''),
 convs=[conv('compter', 'Le comptage de fin de poste', '组长', 'Chef d’équipe', 'Fin de journée. Ton chef d’équipe vérifie la production.', {
  'a': node('今天做了多少双？', 'Jīntiān zuò le duōshao shuāng?', 'Combien de paires as-tu faites aujourd’hui ?', [
     o('做了八十双。', 'Zuò le bāshí shuāng.', 'J’en ai fait quatre-vingts.', True, 'b'),
     o('八点。', 'Bā diǎn.', 'Huit heures.', fix='八点 = huit heures. Il demande combien : « 八十双 » (80 paires).')]),
  'b': node('不够，今天要一百双。', 'Bú gòu, jīntiān yào yìbǎi shuāng.', 'Pas assez, aujourd’hui il en faut cent.', [
     o('还差二十双，我马上做。', 'Hái chà èrshí shuāng, wǒ mǎshàng zuò.', 'Il en manque vingt, je m’y mets tout de suite.', True, 'c'),
     o('还差十双。', 'Hái chà shí shuāng.', 'Il en manque dix.', fix='100 − 80 = 20 : « 还差二十双 ».')]),
  'c': node('胶水还有几箱？', 'Jiāoshuǐ hái yǒu jǐ xiāng?', 'Il reste combien de cartons de colle ?', [
     o('还有两箱。', 'Hái yǒu liǎng xiāng.', 'Il en reste deux.', True, 'end'),
     o('还有二箱。', 'Hái yǒu èr xiāng.', '(erreur)', fix='Devant un classificateur, on dit 两, pas 二 : « 两箱 ».')]),
  'end': node('好，加油！', 'Hǎo, jiāyóu!', 'Bien, courage !', end=True)})],
 bonus=[{'h': '一五一十', 'p': 'yī wǔ yī shí', 'fr': 'En détail, point par point', 'note': 'Mot à mot « un, cinq, un, dix » : tout raconter, comme si on comptait.'}]))

# ---------------- Branche Vie quotidienne ----------------
PACKS.append(dict(id='quotidien-marche', file='quotidien-01-marche.json', branch='quotidien', publish=True,
 title='Vie quotidienne · Au marché',
 desc='Acheter des produits, demander le prix, négocier, payer.',
 grammar={'title': '要 : « je veux, je prends »',
  'explain': '要 (yào) est le mot normal pour commander ou acheter : 我要这个 = je prends celui-ci. C’est plus direct que 想 (avoir envie). 不要 = je n’en veux pas.',
  'examples': [ex('我要这个。', 'Wǒ yào zhège.', 'Je prends celui-ci.'), ex('我要一斤西红柿。', 'Wǒ yào yì jīn xīhóngshì.', 'Je voudrais un demi-kilo de tomates.'), ex('不要，谢谢。', 'Bú yào, xièxie.', 'Non merci.')],
  'tip': '斤 (jīn) = un demi-kilo : c’est l’unité de poids des marchés chinois.'},
 items=items('''
q_yijin | 一斤多少钱 | yi jin duo-shao qian | 4 1 1 0 2 | | Combien le demi-kilo ? | Dans une boutique chinoise, demande : 一斤多少钱？
q_taigui | 太贵了 | tai gui le | 4 4 0 | | C’est trop cher
q_pianyi | 便宜一点儿 | pian-yi yi-dian-r | 2 0 4 3 0 | | Un peu moins cher
q_woyao | 我要这个 | wo yao zhe-ge | 3 4 4 0 | | Je prends celui-ci
q_buyao | 不要 | bu yao | 2 4 | | Je n’en veux pas
q_xihongshi | 西红柿 | xi-hong-shi | 1 2 4 | | Tomate
q_jidan | 鸡蛋 | ji-dan | 1 4 | | Œuf
q_dami | 大米 | da-mi | 4 3 | | Riz (cru)
q_you | 油 | you | 2 | | Huile
q_yu | 鱼 | yu | 2 | | Poisson
q_zhaoqian | 找钱 | zhao qian | 3 2 | | Rendre la monnaie
q_weixin | 可以用微信吗 | ke-yi yong Wei-xin ma | 3 3 4 1 4 0 | 2 3 4 1 4 0 | Je peux payer avec WeChat ?
'''),
 pairs=[pair(('油', 'you', 2, 'huile'), ('有', 'you', 3, 'avoir')), pair(('鱼', 'yu', 2, 'poisson'), ('雨', 'yu', 3, 'pluie'))],
 chars=chars('''
西 | xī | ouest | 西 | ouest
红 | hóng | rouge | 纟 | soie
鸡 | jī | poulet | 鸟 | oiseau
蛋 | dàn | œuf | 虫 | insecte
鱼 | yú | poisson | 鱼 | poisson
油 | yóu | huile | 氵 | eau
'''),
 convs=[conv('marche', 'Au stand de légumes', '老板', 'Vendeur', 'Tu fais tes courses chez un commerçant chinois.', {
  'a': node('你要什么？', 'Nǐ yào shénme?', 'Qu’est-ce que tu veux ?', [
     o('我要一斤西红柿。', 'Wǒ yào yì jīn xīhóngshì.', 'Un demi-kilo de tomates.', True, 'b'),
     o('我不要。', 'Wǒ bú yào.', 'Je ne veux rien.', fix='Dis ce que tu veux : « 我要… ».')]),
  'b': node('一斤八块。', 'Yì jīn bā kuài.', 'Huit yuans le demi-kilo.', [
     o('太贵了！便宜一点儿吧。', 'Tài guì le! Piányi yìdiǎnr ba.', 'Trop cher ! Un peu moins, s’il te plaît.', True, 'c'),
     o('好的，给你钱。', 'Hǎo de, gěi nǐ qián.', 'D’accord, voici l’argent.', True, 'end')]),
  'c': node('好吧，七块。', 'Hǎo ba, qī kuài.', 'Bon, sept yuans.', [
     o('好，可以用微信吗？', 'Hǎo, kěyǐ yòng Wēixìn ma?', 'D’accord, je peux payer avec WeChat ?', True, 'end')]),
  'end': node('可以，谢谢！', 'Kěyǐ, xièxie!', 'Oui, merci !', end=True)})],
 bonus=[{'h': '讨价还价', 'p': 'tǎojià-huánjià', 'fr': 'Marchander', 'note': 'Littéralement « demander un prix, rendre un prix ».'}]))

# ---------------- écriture ----------------
HSK1 = '''爱 八 爸爸 杯子 北京 本 不 不客气 菜 茶 吃 出租车 打电话 大 的 点 电脑 电视 电影 东西 都 读 对不起 多 多少 儿子 二 饭店 飞机 分钟 高兴 个 工作 狗 汉语 好 号 喝 和 很 后面 回 会 几 家 叫 今天 九 开 看 看见 块 来 老师 了 冷 里 六 吗 妈妈 买 猫 没关系 没有 米饭 名字 明天 哪 哪儿 那 呢 能 你 年 女儿 朋友 漂亮 苹果 七 前面 钱 请 去 热 人 认识 三 商店 上 上午 少 谁 什么 十 时候 是 书 水 水果 睡觉 说 四 岁 他 她 太 天气 听 同学 喂 我 我们 五 喜欢 下 下午 下雨 先生 现在 想 小 小姐 些 写 谢谢 星期 学生 学习 学校 一 一点儿 衣服 医生 医院 椅子 有 月 在 再见 怎么 怎么样 这 中国 中午 住 桌子 字 昨天 坐 做'''.split()

if __name__ == '__main__':
    # Version dépôt : régénère les chapitres sans jamais toucher à packs/packs.json.
    # Un chapitre déjà publié est réécrit dans packs/ (pense à augmenter "v" dans packs.json),
    # un chapitre non publié est écrit dans a-publier/.
    published = {p['id'] for p in json.load(open(os.path.join(OUT_PUB, 'packs.json'), encoding='utf-8'))['packs']}
    covered = set()
    for p in PACKS:
        data = {k: v for k, v in p.items() if k not in ('file', 'publish', 'id')}
        for it in p['items']:
            han = len(re.findall(r'[\u3400-\u9fff]', it['h'])); syl = len(re.split(r'[ -]', it['p']))
            assert han == syl == len(it['t']) and len(it.get('s', it['t'])) == syl, it['id']
            covered.add(it['h'])
        dest = OUT_PUB if p['id'] in published else OUT_QUEUE
        json.dump(data, open(os.path.join(dest, p['file']), 'w'), ensure_ascii=False, indent=1)
        print(('publié   ' if dest == OUT_PUB else 'en file  ') + p['file'])
    print('Mots HSK 1 non couverts :', [w for w in HSK1 if w not in covered and w not in ('谢谢', '对不起')])
