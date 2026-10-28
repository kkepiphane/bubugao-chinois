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
 desc='Dire qui tu es, demander le nom de quelqu’un, d’où il vient. 15 mots de la liste officielle HSK 1 et 14 phrases pour t’en servir.',
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
k01_s_nishishei | 你是谁 | ni shi shei | 3 4 2 | | Tu es qui ?
k01_s_tashishei | 他是谁 | ta shi shei | 1 4 2 | | Qui est-ce ? (lui)
k01_s_shiwo | 是我 | shi wo | 4 3 | | C’est moi
k01_s_tazhongguo | 她是中国人 | ta shi Zhong-guo ren | 1 4 1 2 2 | | Elle est chinoise
k01_s_bushizhongguo | 我不是中国人 | wo bu shi Zhong-guo ren | 3 2 4 1 2 2 | | Je ne suis pas chinoise
k01_s_shibushi | 你是不是中国人 | ni shi bu shi Zhong-guo ren | 3 4 0 4 1 2 2 | | Tu es chinois ou pas ?
k01_s_tajiao | 他叫什么名字 | ta jiao shen-me ming-zi | 1 4 2 0 2 0 | | Comment il s’appelle ?
k01_s_renshita | 我认识她 | wo ren-shi ta | 3 4 0 1 | | Je la connais
k01_s_burenshi | 我不认识他 | wo bu ren-shi ta | 3 2 4 0 1 | | Je ne le connais pas
k01_s_tongshi | 我们是同事 | wo-men shi tong-shi | 3 0 4 2 4 | | Nous sommes collègues | Dis à une collègue chinoise de ton atelier : 我们是同事。
k01_s_hengaoxing | 我很高兴 | wo hen gao-xing | 3 3 1 4 | 2 3 1 4 | Je suis contente
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
 desc='Compter de 1 à 99, demander combien, dire son âge. 15 mots HSK 1 et 13 phrases pour t’en servir.',
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
k02_s_shiyi | 十一 | shi-yi | 2 1 | | Onze (11)
k02_s_ershi | 二十 | er-shi | 4 2 | | Vingt (20)
k02_s_liushi | 六十 | liu-shi | 4 2 | | Soixante (60)
k02_s_bashiba | 八十八 | ba-shi-ba | 1 2 1 | | Quatre-vingt-huit (88, porte-bonheur)
k02_s_jiushijiu | 九十九 | jiu-shi-jiu | 3 2 3 | | Quatre-vingt-dix-neuf (99)
k02_s_yigeren | 一个人 | yi ge ren | 2 0 2 | | Une personne, toute seule
k02_s_sangeren | 三个人 | san ge ren | 1 0 2 | | Trois personnes
k02_s_jigeren | 几个人 | ji ge ren | 3 0 2 | | Combien de personnes ? | Le matin, demande à ton chef d’équipe : 今天几个人？
k02_s_duoshaoren | 多少人 | duo-shao ren | 1 0 2 | | Combien de gens ?
k02_s_yinian | 一年 | yi nian | 4 2 | | Un an, une année
k02_s_shiwusui | 他十五岁 | ta shi-wu sui | 1 2 3 4 | | Il a quinze ans
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
 desc='Parler de ta famille, de tes amis, des gens autour de toi. 15 mots HSK 1 et 13 phrases pour t’en servir.',
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
k03_s_baba | 我爸爸是医生 | wo ba-ba shi yi-sheng | 3 4 0 4 1 1 | | Mon père est médecin
k03_s_mama | 我妈妈是老师 | wo ma-ma shi lao-shi | 3 1 0 4 3 1 | | Ma mère est enseignante
k03_s_nver | 她是我女儿 | ta shi wo nv-er | 1 4 3 3 2 | 1 4 2 3 2 | C’est ma fille
k03_s_meiyounver | 我没有女儿 | wo mei-you nv-er | 3 2 3 3 2 | 3 2 2 3 2 | Je n’ai pas de fille
k03_s_tongxue | 他是我的同学 | ta shi wo de tong-xue | 1 4 3 0 2 2 | | C’est mon camarade de classe
k03_s_shuide | 她是谁的朋友 | ta shi shei de peng-you | 1 4 2 0 2 0 | | C’est l’amie de qui ?
k03_s_zhongguopengyou | 我有中国朋友 | wo you Zhong-guo peng-you | 3 3 1 2 2 0 | 2 3 1 2 2 0 | J’ai des amis chinois
k03_s_xuesheng | 我不是学生 | wo bu shi xue-sheng | 3 2 4 2 0 | | Je ne suis pas étudiante
k03_s_womenjia | 我们家 | wo-men jia | 3 0 1 | | Chez nous, notre famille
k03_s_xiansheng | 王先生 | Wang xian-sheng | 2 1 0 | | Monsieur Wang | Pour appeler poliment un chef chinois, dis son nom de famille + 先生 : 王先生！
k03_s_xiaojie | 张小姐 | Zhang xiao-jie | 1 3 3 | 1 2 3 | Mademoiselle Zhang
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
 desc='Dire l’heure, la date, les moments de la journée. 13 mots HSK 1 et 14 phrases pour t’en servir.',
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
k04_s_badian | 八点 | ba dian | 1 3 | | Huit heures
k04_s_sandian | 现在三点 | xian-zai san dian | 4 4 1 3 | | Il est trois heures
k04_s_jiudianshifen | 九点十分 | jiu dian shi fen | 3 3 2 1 | 2 3 2 1 | Neuf heures dix
k04_s_shifenzhong | 十分钟 | shi fen-zhong | 2 1 1 | | Dix minutes
k04_s_mingtianshangwu | 明天上午 | ming-tian shang-wu | 2 1 4 3 | | Demain matin
k04_s_liudianxiaban | 下午六点下班 | xia-wu liu dian xia-ban | 4 3 4 3 4 1 | | Je finis à six heures du soir
k04_s_xingqiyi | 星期一 | xing-qi-yi | 1 1 1 | | Lundi
k04_s_xingqiliu | 星期六 | xing-qi-liu | 1 1 4 | | Samedi
k04_s_xingqitian | 星期天 | xing-qi-tian | 1 1 1 | | Dimanche
k04_s_xingqiji | 今天星期几 | jin-tian xing-qi ji | 1 1 1 1 3 | | On est quel jour de la semaine ? | Le matin, demande à une collègue : 今天星期几？
k04_s_yihao | 十月一号 | shi yue yi hao | 2 4 1 4 | | Le 1er octobre
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
 desc='Commander au restaurant, dire ce que tu aimes et ce que tu veux. 14 mots HSK 1 et 13 phrases pour t’en servir.',
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
k05_s_chifan | 吃饭 | chi fan | 1 4 | | Manger (un repas)
k05_s_chilema | 你吃饭了吗 | ni chi fan le ma | 3 1 4 0 0 | | Tu as mangé ? (salut amical) | À la pause de midi, demande à un collègue chinois : 你吃饭了吗？
k05_s_heshui | 我想喝水 | wo xiang he shui | 3 3 1 3 | 2 3 1 3 | J’ai envie de boire de l’eau
k05_s_qinghecha | 请喝茶 | qing he cha | 3 1 2 | | Prends du thé, je t’en prie
k05_s_yibeicha | 一杯茶 | yi bei cha | 4 1 2 | | Une tasse de thé
k05_s_yigepingguo | 一个苹果 | yi ge ping-guo | 2 0 2 3 | | Une pomme
k05_s_zhongguocai | 中国菜 | Zhong-guo cai | 1 2 4 | | La cuisine chinoise
k05_s_xihuanmifan | 我喜欢吃米饭 | wo xi-huan chi mi-fan | 3 3 0 1 3 4 | 2 3 0 1 3 4 | J’aime manger du riz
k05_s_aishuiguo | 我爱吃水果 | wo ai chi shui-guo | 3 4 1 3 3 | 3 4 1 2 3 | J’adore les fruits
k05_s_buxiangchi | 我不想吃 | wo bu xiang chi | 3 4 3 1 | | Je n’ai pas envie de manger
k05_s_shenmecai | 你喜欢什么菜 | ni xi-huan shen-me cai | 3 3 0 2 0 4 | 2 3 0 2 0 4 | Quels plats tu aimes ?
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
 desc='Faire des achats, demander le prix, dire que c’est trop. 12 mots HSK 1 et 14 phrases pour t’en servir.',
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
k06_s_sankuai | 三块钱 | san kuai qian | 1 4 2 | | Trois yuans
k06_s_ershiwukuai | 二十五块 | er-shi-wu kuai | 4 2 3 4 | | Vingt-cinq yuans
k06_s_maishenme | 你买什么 | ni mai shen-me | 3 3 2 0 | 2 3 2 0 | Tu achètes quoi ?
k06_s_maiyifu | 我想买衣服 | wo xiang mai yi-fu | 3 3 3 1 0 | 2 2 3 1 0 | J’ai envie d’acheter des vêtements
k06_s_piaoliang | 你的衣服很漂亮 | ni de yi-fu hen piao-liang | 3 0 1 0 3 4 0 | | Tes vêtements sont très beaux
k06_s_taishao | 太少了 | tai shao le | 4 3 0 | | C’est trop peu
k06_s_duoyidianr | 多一点儿 | duo yi-dian-r | 1 4 3 0 | | Un peu plus
k06_s_shaoyidianr | 少一点儿 | shao yi-dian-r | 3 4 3 0 | | Un peu moins
k06_s_meiqian | 我没有钱 | wo mei-you qian | 3 2 3 2 | | Je n’ai pas d’argent
k06_s_shuiguo | 买一些水果 | mai yi-xie shui-guo | 3 4 1 3 3 | 3 4 1 2 3 | Acheter quelques fruits
k06_s_shangdian | 中国商店 | Zhong-guo shang-dian | 1 2 1 4 | | Une boutique chinoise
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
 desc='Dire où tu habites, où se trouve quelque chose, devant, derrière. 14 mots HSK 1 et 13 phrases pour t’en servir.',
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
k07_s_lome | 我住在洛美 | wo zhu zai Luo-mei | 3 4 4 4 3 | | J’habite à Lomé | Quand un collègue chinois te demande où tu habites, réponds : 我住在洛美。
k07_s_nizainar | 你在哪儿 | ni zai na-r | 3 4 3 0 | | Tu es où ?
k07_s_zher | 我在这儿 | wo zai zhe-r | 3 4 4 0 | | Je suis ici
k07_s_zainar | 在那儿 | zai na-r | 4 4 0 | | Là-bas
k07_s_zheshinar | 这是哪儿 | zhe shi na-r | 4 4 3 0 | | On est où, ici ?
k07_s_yiyuanzainar | 医院在哪儿 | yi-yuan zai na-r | 1 4 4 3 0 | | Où est l’hôpital ?
k07_s_jiali | 在家里 | zai jia li | 4 1 3 | | À la maison
k07_s_qianmian | 在前面 | zai qian-mian | 4 2 4 | | C’est devant
k07_s_houmian | 他在我后面 | ta zai wo hou-mian | 1 4 3 4 4 | | Il est derrière moi
k07_s_nageren | 那个人是谁 | na-ge ren shi shei | 4 0 2 4 2 | | Qui est cette personne ?
k07_s_beijingren | 他是北京人 | ta shi Bei-jing ren | 1 4 3 1 2 | | Il vient de Pékin
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
 desc='Aller, venir, rentrer, prendre un taxi, passer un appel. 13 mots HSK 1 et 14 phrases pour t’en servir.',
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
k08_s_huijia | 我回家 | wo hui jia | 3 2 1 | | Je rentre à la maison
k08_s_qushangban | 去上班 | qu shang-ban | 4 4 1 | | Aller au travail
k08_s_zenmequ | 怎么去 | zen-me qu | 3 0 4 | | Comment on y va ?
k08_s_feiji | 坐飞机去中国 | zuo fei-ji qu Zhong-guo | 4 1 1 4 1 2 | | Aller en Chine en avion
k08_s_shihoulai | 你什么时候来 | ni shen-me shi-hou lai | 3 2 0 2 0 2 | | Tu viens quand ?
k08_s_nenglai | 你能来吗 | ni neng lai ma | 3 2 2 0 | | Tu peux venir ?
k08_s_bunengqu | 我不能去 | wo bu neng qu | 3 4 2 4 | | Je ne peux pas y aller
k08_s_kaiche | 他会开车 | ta hui kai che | 1 4 1 1 | | Il sait conduire
k08_s_dadianhua | 我能打电话吗 | wo neng da dian-hua ma | 3 2 3 4 4 0 | | Je peux passer un coup de fil ?
k08_s_weinihao | 喂，你好 | wei ni hao | 4 3 3 | 4 2 3 | Allô, bonjour
k08_s_qingzuo | 请坐 | qing zuo | 3 4 | | Assieds-toi, je t’en prie
k08_s_mingtianjian | 明天见 | ming-tian jian | 2 1 4 | | À demain | En partant du travail, dis à tes collègues : 明天见！
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
 desc='Regarder, écouter, lire, écrire, travailler, étudier le chinois. 18 mots HSK 1 et 10 phrases pour t’en servir.',
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
k09_s_shuohanyu | 你会说汉语吗 | ni hui shuo Han-yu ma | 3 4 1 4 3 0 | | Tu parles chinois ?
k09_s_yidianr | 我会说一点儿汉语 | wo hui shuo yi-dian-r Han-yu | 3 4 1 4 3 0 4 3 | | Je parle un peu chinois | Quand un collègue chinois s’étonne que tu le comprennes, dis-lui : 我会说一点儿汉语。
k09_s_zenmexie | 这个字怎么写 | zhe-ge zi zen-me xie | 4 0 4 3 0 3 | | Comment s’écrit ce caractère ?
k09_s_zenmedu | 这个字怎么读 | zhe-ge zi zen-me du | 4 0 4 3 0 2 | | Comment se lit ce caractère ?
k09_s_gongzuo | 你做什么工作 | ni zuo shen-me gong-zuo | 3 4 2 0 1 4 | | Tu fais quel travail ?
k09_s_kandianshi | 看电视 | kan dian-shi | 4 4 4 | | Regarder la télé
k09_s_yibenshu | 一本书 | yi ben shu | 4 3 1 | | Un livre
k09_s_shuijiao | 我想睡觉 | wo xiang shui-jiao | 3 3 4 4 | 2 3 4 4 | J’ai envie de dormir
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
 desc='Le temps qu’il fait, décrire, remercier, s’excuser, poser des questions. 19 mots HSK 1 et 8 phrases pour t’en servir : le HSK 1 est complet !',
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
k10_s_nihaoma | 你好吗 | ni hao ma | 3 3 0 | 2 3 0 | Tu vas bien ?
k10_s_zenmeyang | 你怎么样 | ni zen-me-yang | 3 3 0 4 | 2 3 0 4 | Et toi, comment ça va ?
k10_s_douhao | 我们都很好 | wo-men dou hen hao | 3 0 1 3 3 | 3 0 1 2 3 | Nous allons tous bien
k10_s_henre | 今天很热 | jin-tian hen re | 1 1 3 4 | | Il fait très chaud aujourd’hui
k10_s_tailengle | 太冷了 | tai leng le | 4 3 0 | | Il fait trop froid
k10_s_xiayule | 下雨了 | xia-yu le | 4 3 0 | | Il pleut | Quand il commence à pleuvoir, dis à un collègue : 下雨了！
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
 desc='Parler de tes frères et sœurs, de ton mari ou de ta femme, et te présenter poliment. 16 mots HSK 2 et 12 phrases pour t’en servir.',
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
h201_s_ninhao | 您好 | nin hao | 2 3 | | Bonjour (poli) | Salue poliment le patron ou un client : 您好！
h201_s_dajiahao | 大家好 | da-jia hao | 4 1 3 | | Bonjour tout le monde | En arrivant à l’atelier le matin, dis : 大家好！
h201_s_xingwang | 他姓王 | ta xing Wang | 1 4 2 | | Son nom de famille est Wang
h201_s_gege | 我有一个哥哥 | wo you yi ge ge-ge | 3 3 2 0 1 0 | 2 3 2 0 1 0 | J’ai un grand frère
h201_s_jiejie | 这是我姐姐 | zhe shi wo jie-jie | 4 4 3 3 0 | 4 4 2 3 0 | C’est ma grande sœur
h201_s_meimei | 我妹妹是学生 | wo mei-mei shi xue-sheng | 3 4 0 4 2 0 | | Ma petite sœur est étudiante
h201_s_haizi | 她有两个孩子 | ta you liang ge hai-zi | 1 3 3 0 2 0 | 1 2 3 0 2 0 | Elle a deux enfants
h201_s_zhangfu | 你丈夫做什么工作 | ni zhang-fu zuo shen-me gong-zuo | 3 4 0 4 2 0 1 4 | | Que fait ton mari ?
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
 desc='Dire quand tu te lèves, si tu es fatiguée ou malade, et expliquer pourquoi. 15 mots HSK 2 et 13 phrases pour t’en servir.',
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
h202_s_zaoshanghao | 早上好 | zao-shang hao | 3 0 3 | | Bonjour (le matin)
h202_s_wanshanghao | 晚上好 | wan-shang hao | 3 0 3 | | Bonsoir
h202_s_qichuang | 我早上六点起床 | wo zao-shang liu dian qi-chuang | 3 3 0 4 3 3 2 | 2 3 0 4 2 3 2 | Je me lève à six heures du matin
h202_s_henmang | 我今天很忙 | wo jin-tian hen mang | 3 1 1 3 2 | | Je suis très occupée aujourd’hui
h202_s_meishijian | 我没有时间 | wo mei-you shi-jian | 3 2 3 2 1 | | Je n’ai pas le temps
h202_s_bagexiaoshi | 八个小时 | ba ge xiao-shi | 1 0 3 2 | | Huit heures (de travail)
h202_s_yijing | 已经十点了 | yi-jing shi dian le | 3 1 2 3 0 | | Il est déjà dix heures
h202_s_shentihao | 你身体好吗 | ni shen-ti hao ma | 3 1 3 3 0 | 3 1 2 3 0 | Tu es en bonne santé ?
h202_s_yanjing | 我的眼睛很累 | wo de yan-jing hen lei | 3 0 3 0 3 4 | | J’ai les yeux fatigués
h202_s_chiyao | 吃药 | chi yao | 1 4 | | Prendre un médicament
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
 desc='Vendre et acheter, dire les couleurs, les grands prix, et comparer deux choses. 16 mots HSK 2 et 12 phrases pour t’en servir.',
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
h203_s_yibaiyuan | 一百元 | yi-bai yuan | 4 3 2 | | Cent yuans
h203_s_yiqiankuai | 一千块 | yi-qian kuai | 4 1 4 | | Mille yuans
h203_s_zenmemai | 这个怎么卖 | zhe-ge zen-me mai | 4 0 3 0 4 | | Ça se vend comment ? (le prix) | Au marché, montre un produit et demande : 这个怎么卖？
h203_s_lianggongjin | 两公斤 | liang gong-jin | 3 1 1 | | Deux kilos
h203_s_shenmeyanse | 什么颜色 | shen-me yan-se | 2 0 2 4 | | Quelle couleur ?
h203_s_baise | 白色的鞋 | bai-se de xie | 2 4 0 2 | | Des chaussures blanches
h203_s_xinde | 这双鞋是新的 | zhe shuang xie shi xin de | 4 1 2 4 1 0 | | Cette paire est neuve
h203_s_zhuozi | 一张桌子 | yi zhang zhuo-zi | 4 1 1 0 | | Une table
h203_s_bizuotian | 今天比昨天热 | jin-tian bi zuo-tian re | 1 1 3 2 1 4 | | Aujourd’hui, il fait plus chaud qu’hier
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
 desc='Dire si c’est loin ou près, à gauche ou à droite, et expliquer un trajet. 16 mots HSK 2 et 11 phrases pour t’en servir.',
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
h204_s_buyuan | 不远，很近 | bu yuan hen jin | 4 3 3 4 | 4 2 3 4 | Pas loin, tout près
h204_s_zuobian | 在左边 | zai zuo-bian | 4 3 1 | | C’est à gauche
h204_s_youbian | 在右边 | zai you-bian | 4 4 1 | | C’est à droite
h204_s_pangbian | 在商店旁边 | zai shang-dian pang-bian | 4 1 4 2 1 | | À côté de la boutique
h204_s_zenmezou | 去医院怎么走 | qu yi-yuan zen-me zou | 4 1 4 3 0 3 | | Pour aller à l’hôpital, c’est par où ?
h204_s_gongjiao | 我坐公共汽车上班 | wo zuo gong-gong qi-che shang-ban | 3 4 1 4 4 1 4 1 | | Je vais au travail en bus
h204_s_maipiao | 买票 | mai piao | 3 4 | | Acheter un billet
h204_s_daole | 到了 | dao le | 4 0 | | On est arrivés
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
 desc='Demander, répondre, dire que tu as compris (ou pas), aider un collègue. 16 mots HSK 2 et 12 phrases pour t’en servir.',
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
h205_s_tingbudong | 我听不懂 | wo ting bu dong | 3 1 0 3 | | Je ne comprends pas (ce que j’entends) | Si un collègue parle trop vite, dis-lui : 我听不懂，请再说一遍。
h205_s_dongle | 我懂了 | wo dong le | 3 3 0 | 2 3 0 | J’ai compris
h205_s_buzhidao | 我不知道 | wo bu zhi-dao | 3 4 1 4 | | Je ne sais pas
h205_s_gaosuwo | 请告诉我 | qing gao-su wo | 3 4 0 3 | | Dis-moi, s’il te plaît
h205_s_zhaoshei | 你找谁 | ni zhao shei | 3 3 2 | 2 3 2 | Tu cherches qui ?
h205_s_geini | 给你 | gei ni | 3 3 | 2 3 | Tiens, voilà
h205_s_kaishi | 开始工作 | kai-shi gong-zuo | 1 3 1 4 | | Commencer le travail
h205_s_zhunbeihao | 准备好了 | zhun-bei hao le | 3 4 3 0 | | C’est prêt
h205_s_cuole | 错了 | cuo le | 4 0 | | C’est faux
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

# ---------------- HSK 2 · 6 ----------------
PACKS.append(dict(id='hsk2-06', file='hsk2-06-loisirs.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 6 — Sport et loisirs',
 desc='Dire ce que tu aimes faire, proposer une sortie, parler de tes rêves de voyage. 14 mots HSK 2 et 13 phrases pour t’en servir.',
 grammar={'title': '吧 : proposer ou demander l’accord',
  'explain': '吧 (ba) à la fin d’une phrase la rend plus douce : c’est une proposition, pas un ordre. 我们走吧 = « allons-y ! », 一起去吧 = « on y va ensemble ? ». Pour accepter, réponds 好啊 (hǎo a) ou 好吧 (hǎo ba).',
  'examples': [ex('我们一起去吧！', 'Wǒmen yìqǐ qù ba!', 'Allons-y ensemble !'), ex('星期六去玩吧。', 'Xīngqīliù qù wán ba.', 'Samedi, allons nous amuser.'), ex('你是多哥人吧？', 'Nǐ shì Duōgē rén ba?', 'Tu es Togolaise, je crois ?'), ex('好吧，我也去。', 'Hǎo ba, wǒ yě qù.', 'Bon, d’accord, j’y vais aussi.')],
  'tip': '一起 (ensemble) se place avant le verbe : 我们一起吃饭 = mangeons ensemble.'},
 items=items('''
h206_yundong | 运动 | yun-dong | 4 4 | | Faire du sport, sport
h206_paobu | 跑步 | pao-bu | 3 4 | | Courir, faire un footing
h206_youyong | 游泳 | you-yong | 2 3 | | Nager
h206_lanqiu | 打篮球 | da lan-qiu | 3 2 2 | | Jouer au basket
h206_zuqiu | 踢足球 | ti zu-qiu | 1 2 2 | | Jouer au foot
h206_changge | 唱歌 | chang-ge | 4 1 | | Chanter
h206_tiaowu | 跳舞 | tiao-wu | 4 3 | | Danser
h206_lvyou | 旅游 | lv-you | 3 2 | | Voyager (pour le plaisir)
h206_wan | 玩 | wan | 2 | | S’amuser, jouer
h206_yiqi | 一起 | yi-qi | 4 3 | | Ensemble
h206_ba | 吧 | ba | 0 | | (proposition : « …, d’accord ? »)
h206_xiwang | 希望 | xi-wang | 1 4 | | Espérer
h206_zui | 最 | zui | 4 | | Le plus
h206_feichang | 非常 | fei-chang | 1 2 | | Très, extrêmement
h206_s_yiqiqu | 我们一起去吧 | wo-men yi-qi qu ba | 3 0 4 3 4 0 | | Allons-y ensemble ! | Le samedi, propose à une collègue : 我们一起去吧！
h206_s_shenmeyundong | 你喜欢什么运动 | ni xi-huan shen-me yun-dong | 3 3 0 2 0 4 4 | 2 3 0 2 0 4 4 | Quel sport tu aimes ?
h206_s_paobu | 我喜欢跑步 | wo xi-huan pao-bu | 3 3 0 3 4 | 2 3 0 3 4 | J’aime courir
h206_s_huiyouyong | 你会游泳吗 | ni hui you-yong ma | 3 4 2 3 0 | | Tu sais nager ?
h206_s_buhuiyouyong | 我不会游泳 | wo bu hui you-yong | 3 2 4 2 3 | | Je ne sais pas nager
h206_s_tizuqiu | 我们去踢足球吧 | wo-men qu ti zu-qiu ba | 3 0 4 1 2 2 0 | | On va jouer au foot ?
h206_s_zuixihuan | 我最喜欢唱歌 | wo zui xi-huan chang-ge | 3 4 3 0 4 1 | | Ce que j’aime le plus, c’est chanter
h206_s_quwan | 星期六去玩吧 | xing-qi-liu qu wan ba | 1 1 4 4 2 0 | | Samedi, allons nous amuser
h206_s_feichanghao | 非常好 | fei-chang hao | 1 2 3 | | Très bien !
h206_s_lvyou | 我希望去中国旅游 | wo xi-wang qu Zhong-guo lv-you | 3 1 4 4 1 2 3 2 | | J’espère voyager en Chine
h206_s_yiqichifan | 一起吃饭吧 | yi-qi chi fan ba | 4 3 1 4 0 | | Mangeons ensemble
h206_s_lanqiulei | 打篮球很累 | da lan-qiu hen lei | 3 2 2 3 4 | | Le basket, c’est fatigant
h206_s_haoa | 好啊 | hao a | 3 0 | | Avec plaisir, d’accord !
'''),
 pairs=[pair(('歌', 'ge', 1, 'chanson'), ('个', 'ge', 4, 'classificateur (一个)')), pair(('玩', 'wan', 2, 's’amuser'), ('晚', 'wan', 3, 'soir, tard'))],
 chars=chars('''
运 | yùn | transporter, bouger | 辶 | marche
动 | dòng | bouger | 力 | force
跑 | pǎo | courir | 足 | pied
游 | yóu | nager, voyager | 氵 | eau
球 | qiú | ballon | 王 | jade
唱 | chàng | chanter | 口 | bouche
起 | qǐ | se lever | 走 | marcher
最 | zuì | le plus | 曰 | dire
'''),
 convs=[conv('hsk2-loisirs', 'Que fais-tu dimanche ?', '小陈', 'Collègue', 'Vendredi soir, à la sortie de l’usine. Une collègue chinoise te parle du week-end.', {
  'a': node('星期天你做什么？', 'Xīngqītiān nǐ zuò shénme?', 'Qu’est-ce que tu fais dimanche ?', [
     o('我想去跑步。你呢？', 'Wǒ xiǎng qù pǎobù. Nǐ ne?', 'J’ai envie d’aller courir. Et toi ?', True, 'b'),
     o('我是跑步。', 'Wǒ shì pǎobù.', '(phrase mal construite)', fix='Pas de 是 devant une action : « 我想去跑步 ».')]),
  'b': node('我喜欢游泳。我们一起去游泳吧！', 'Wǒ xǐhuan yóuyǒng. Wǒmen yìqǐ qù yóuyǒng ba!', 'Moi, j’aime nager. Allons nager ensemble !', [
     o('我不会游泳……我们去唱歌吧！', 'Wǒ bú huì yóuyǒng… Wǒmen qù chànggē ba!', 'Je ne sais pas nager… Allons chanter !', True, 'c'),
     o('好啊，一起去吧！', 'Hǎo a, yìqǐ qù ba!', 'Avec plaisir, allons-y ensemble !', True, 'c'),
     o('一起我们去吧。', 'Yìqǐ wǒmen qù ba.', '(phrase mal construite)', fix='一起 se place juste avant le verbe : « 我们一起去吧 ».')]),
  'c': node('好啊！我最喜欢唱歌。几点去？', 'Hǎo a! Wǒ zuì xǐhuan chànggē. Jǐ diǎn qù?', 'Super ! Chanter, c’est ce que je préfère. On y va à quelle heure ?', [
     o('下午三点吧。', 'Xiàwǔ sān diǎn ba.', 'Trois heures de l’après-midi, d’accord ?', True, 'end'),
     o('我最喜欢下午。', 'Wǒ zuì xǐhuan xiàwǔ.', 'Je préfère l’après-midi.', fix='Elle demande l’heure : réponds avec l’heure, « 下午三点吧 ».')]),
  'end': node('好，星期天见！', 'Hǎo, xīngqītiān jiàn!', 'D’accord, à dimanche !', end=True)})],
 bonus=[{'h': '生命在于运动', 'p': 'shēngmìng zàiyú yùndòng', 'fr': 'La vie, c’est le mouvement', 'note': 'Dicton chinois très connu pour encourager à faire du sport.'}]))

# ---------------- HSK 2 · 7 ----------------
PACKS.append(dict(id='hsk2-07', file='hsk2-07-temps-qui-passe.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 7 — Le temps qu’il fait, le temps qui passe',
 desc='Parler du beau temps et de la neige, dire « déjà une fois », « la première fois », « chaque jour ». 14 mots HSK 2 et 14 phrases pour t’en servir.',
 grammar={'title': '过 : « déjà… une fois » (l’expérience)',
  'explain': 'Pour dire qu’on a déjà vécu quelque chose, mets 过 (guo) juste après le verbe : 我去过中国 = je suis déjà allée en Chine. Pour dire « jamais », mets 没 (méi) devant le verbe, et garde 过 : 我没去过 = je n’y suis jamais allée.',
  'examples': [ex('我去过北京。', 'Wǒ qù guo Běijīng.', 'Je suis déjà allée à Pékin.'), ex('你吃过饺子吗？', 'Nǐ chī guo jiǎozi ma?', 'Tu as déjà mangé des raviolis chinois ?'), ex('我没见过雪。', 'Wǒ méi jiàn guo xuě.', 'Je n’ai jamais vu la neige.'), ex('这是我第一次来。', 'Zhè shì wǒ dì-yī cì lái.', 'C’est la première fois que je viens.')],
  'tip': 'Avec 过, on dit toujours 没, jamais 不 : 我没去过 (et pas 我不去过).'},
 items=items('''
h207_qing | 晴 | qing | 2 | | Ensoleillé, beau temps
h207_yin | 阴 | yin | 1 | | Couvert, nuageux
h207_xue | 雪 | xue | 3 | | Neige
h207_qunian | 去年 | qu-nian | 4 2 | | L’année dernière
h207_mei | 每 | mei | 3 | | Chaque
h207_ci | 次 | ci | 4 | | Fois
h207_diyi | 第一 | di-yi | 4 1 | | Premier, premièrement
h207_guo | 过 | guo | 0 | | (déjà fait, une fois : 去过)
h207_ling | 零 | ling | 2 | | Zéro
h207_zhen | 真 | zhen | 1 | | Vraiment
h207_chang | 长 | chang | 2 | | Long
h207_gao | 高 | gao | 1 | | Grand, haut
h207_kuai | 快 | kuai | 4 | | Rapide, vite
h207_man | 慢 | man | 4 | | Lent, lentement
h207_s_qingtian | 今天是晴天 | jin-tian shi qing-tian | 1 1 4 2 1 | | Aujourd’hui, il fait beau
h207_s_yintian | 明天是阴天 | ming-tian shi yin-tian | 2 1 4 1 1 | | Demain, le temps sera couvert
h207_s_jianguoxue | 你见过雪吗 | ni jian guo xue ma | 3 4 0 3 0 | | Tu as déjà vu la neige ?
h207_s_meijianguo | 我没见过雪 | wo mei jian guo xue | 3 2 4 0 3 | | Je n’ai jamais vu la neige
h207_s_quguo | 你去过中国吗 | ni qu guo Zhong-guo ma | 3 4 0 1 2 0 | | Tu es déjà allée en Chine ?
h207_s_meitian | 我每天六点起床 | wo mei-tian liu dian qi-chuang | 3 3 1 4 3 3 2 | 2 3 1 4 2 3 2 | Je me lève à six heures tous les jours
h207_s_sanci | 一个星期去三次 | yi ge xing-qi qu san ci | 2 0 1 1 4 1 4 | | Trois fois par semaine
h207_s_diyici | 第一次 | di-yi ci | 4 1 4 | | La première fois
h207_s_diyicilai | 这是我第一次来 | zhe shi wo di-yi ci lai | 4 4 3 4 1 4 2 | | C’est la première fois que je viens
h207_s_qunian | 我去年开始工作 | wo qu-nian kai-shi gong-zuo | 3 4 2 1 3 1 4 | | J’ai commencé à travailler l’année dernière
h207_s_yibailingwu | 一百零五 | yi-bai ling wu | 4 3 2 3 | | Cent cinq (105)
h207_s_nizhenhao | 你真好 | ni zhen hao | 3 1 3 | | Tu es vraiment gentille ! | Quand une collègue t’aide, dis-lui : 你真好！
h207_s_taimanle | 太慢了 | tai man le | 4 4 0 | | C’est trop lent
h207_s_tahengao | 他很高 | ta hen gao | 1 3 1 | | Il est grand
h207_s_taichang | 时间太长了 | shi-jian tai chang le | 2 1 4 2 0 | | C’est trop long
'''),
 pairs=[pair(('晴', 'qing', 2, 'beau temps'), ('请', 'qing', 3, 's’il te plaît')), pair(('雪', 'xue', 3, 'neige'), ('学', 'xue', 2, 'étudier'))],
 chars=chars('''
晴 | qíng | beau temps | 日 | soleil
阴 | yīn | couvert, ombre | 阝 | colline
雪 | xuě | neige | 雨 | pluie
零 | líng | zéro | 雨 | pluie
每 | měi | chaque | 母 | mère
次 | cì | fois | 欠 | bâiller
第 | dì | (rang : 第一) | 竹 | bambou
慢 | màn | lent | 忄 | cœur
'''),
 convs=[conv('hsk2-neige', 'La neige de Pékin', '组长', 'Chef d’équipe', 'Il fait très chaud à l’atelier. Ton chef d’équipe parle du temps qu’il fait chez lui, en Chine.', {
  'a': node('今天是晴天，真热！你去过中国吗？', 'Jīntiān shì qíngtiān, zhēn rè! Nǐ qù guo Zhōngguó ma?', 'Il fait beau aujourd’hui, vraiment chaud ! Tu es déjà allée en Chine ?', [
     o('没去过。中国冷吗？', 'Méi qù guo. Zhōngguó lěng ma?', 'Jamais. Il fait froid en Chine ?', True, 'b'),
     o('我不去过。', 'Wǒ bú qù guo.', '(phrase mal construite)', fix='Avec 过, on dit 没 et pas 不 : « 我没去过 ».')]),
  'b': node('北京十二月很冷，会下雪。你见过雪吗？', 'Běijīng shí’èr yuè hěn lěng, huì xià xuě. Nǐ jiàn guo xuě ma?', 'À Pékin, en décembre, il fait très froid, il neige. Tu as déjà vu la neige ?', [
     o('没见过，我很想看！', 'Méi jiàn guo, wǒ hěn xiǎng kàn!', 'Jamais, j’ai très envie de la voir !', True, 'c'),
     o('我没见雪过。', 'Wǒ méi jiàn xuě guo.', '(phrase mal construite)', fix='过 se colle juste après le verbe : « 我没见过雪 ».')]),
  'c': node('你可以来北京看雪！', 'Nǐ kěyǐ lái Běijīng kàn xuě!', 'Tu pourras venir voir la neige à Pékin !', [
     o('真的吗？太好了！', 'Zhēn de ma? Tài hǎo le!', 'Vraiment ? Super !', True, 'end'),
     o('真好吃！', 'Zhēn hǎochī!', 'C’est vraiment bon (à manger) !', fix='好吃 = bon à manger. Ici, dis plutôt « 真的吗？太好了！ ».')]),
  'end': node('真的！', 'Zhēn de!', 'Vraiment !', end=True)})],
 bonus=[{'h': '瑞雪兆丰年', 'p': 'ruìxuě zhào fēngnián', 'fr': 'Une bonne neige annonce une bonne récolte', 'note': 'Proverbe des paysans chinois : un hiver neigeux prépare une bonne année.'}]))

# ---------------- HSK 2 · 8 ----------------
PACKS.append(dict(id='hsk2-08', file='hsk2-08-a-table.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 8 — À table : encore, aussi, permis',
 desc='Dire que c’est bon, commander des nouilles ou un café, demander « encore » et « est-ce que je peux ? ». 12 mots HSK 2 et 16 phrases pour t’en servir.',
 grammar={'title': '还 et 再 : deux façons de dire « encore »',
  'explain': '还 (hái) = « encore, en plus » ou « toujours pas » : 我还要一个 = j’en veux encore un, 我还没吃饭 = je n’ai pas encore mangé. 再 (zài) = « de nouveau, plus tard » pour une action qui va se répéter : 明天再来 = reviens demain.',
  'examples': [ex('我还要一杯牛奶。', 'Wǒ hái yào yì bēi niúnǎi.', 'Je veux encore un verre de lait.'), ex('你还要什么？', 'Nǐ hái yào shénme?', 'Tu veux autre chose ?'), ex('请再说一遍。', 'Qǐng zài shuō yí biàn.', 'Redis-le, s’il te plaît.'), ex('先洗手，再吃饭。', 'Xiān xǐ shǒu, zài chī fàn.', 'D’abord on se lave les mains, ensuite on mange.')],
  'tip': '再 parle toujours de ce qui va arriver. Pour le passé, on ne l’utilise pas.'},
 items=items('''
h208_haochi | 好吃 | hao-chi | 3 1 | | Bon (à manger)
h208_miantiao | 面条 | mian-tiao | 4 2 | | Nouilles
h208_yangrou | 羊肉 | yang-rou | 2 4 | | Viande de mouton
h208_niunai | 牛奶 | niu-nai | 2 3 | | Lait
h208_kafei | 咖啡 | ka-fei | 1 1 | | Café
h208_xigua | 西瓜 | xi-gua | 1 1 | | Pastèque
h208_fuwuyuan | 服务员 | fu-wu-yuan | 2 4 2 | | Serveur, serveuse
h208_xi | 洗 | xi | 3 | | Laver
h208_yao | 要 | yao | 4 | | Vouloir ; il faut
h208_zai | 再 | zai | 4 | | De nouveau, encore (plus tard)
h208_hai | 还 | hai | 2 | | Encore, en plus ; toujours
h208_keyi | 可以 | ke-yi | 3 3 | 2 3 | Pouvoir (avoir le droit)
h208_s_haochi | 这个菜很好吃 | zhe-ge cai hen hao-chi | 4 0 4 3 3 1 | 4 0 4 2 3 1 | Ce plat est très bon | À la cantine, fais plaisir à la cuisinière : 这个菜很好吃！
h208_s_miantiao | 一碗面条 | yi wan mian-tiao | 4 3 4 2 | | Un bol de nouilles
h208_s_yangrou | 我不吃羊肉 | wo bu chi yang-rou | 3 4 1 2 4 | | Je ne mange pas de mouton
h208_s_niunai | 一杯牛奶 | yi bei niu-nai | 4 1 2 3 | | Un verre de lait
h208_s_kafei | 你喝咖啡吗 | ni he ka-fei ma | 3 1 1 1 0 | | Tu bois du café ?
h208_s_xigua | 西瓜很甜 | xi-gua hen tian | 1 1 3 2 | | La pastèque est très sucrée
h208_s_fuwuyuan | 服务员，有咖啡吗 | fu-wu-yuan you ka-fei ma | 2 4 2 3 1 1 0 | | S’il vous plaît, vous avez du café ?
h208_s_xishou | 洗手 | xi shou | 3 3 | 2 3 | Se laver les mains
h208_s_xianxishou | 先洗手再吃饭 | xian xi shou zai chi fan | 1 3 3 4 1 4 | 1 2 3 4 1 4 | D’abord se laver les mains, ensuite manger
h208_s_haiyao | 我还要一个 | wo hai yao yi ge | 3 2 4 2 0 | | J’en veux encore un
h208_s_haiyaoshenme | 你还要什么 | ni hai yao shen-me | 3 2 4 2 0 | | Tu veux autre chose ?
h208_s_keyizuo | 可以坐这儿吗 | ke-yi zuo zhe-r ma | 3 3 4 4 0 0 | 2 3 4 4 0 0 | Je peux m’asseoir ici ? | À la cantine, avant de t’asseoir à côté d’un collègue chinois, demande : 可以坐这儿吗？
h208_s_bukeyi | 不可以 | bu ke-yi | 4 3 3 | 4 2 3 | Non, ce n’est pas permis
h208_s_zailai | 明天再来 | ming-tian zai lai | 2 1 4 2 | | Reviens demain
h208_s_yaoheshenme | 你要喝什么 | ni yao he shen-me | 3 4 1 2 0 | | Qu’est-ce que tu veux boire ?
h208_s_haimeichi | 我还没吃饭 | wo hai mei chi fan | 3 2 2 1 4 | | Je n’ai pas encore mangé
'''),
 pairs=[pair(('洗', 'xi', 3, 'laver'), ('西', 'xi', 1, 'ouest')), pair(('羊', 'yang', 2, 'mouton'), ('样', 'yang', 4, 'manière (怎么样)'))],
 chars=chars('''
面 | miàn | nouilles, visage | 面 | visage
条 | tiáo | bande (pour les choses longues) | 木 | bois
羊 | yáng | mouton | 羊 | mouton
奶 | nǎi | lait | 女 | femme
瓜 | guā | melon | 瓜 | melon
洗 | xǐ | laver | 氵 | eau
还 | hái | encore | 辶 | marche
'''),
 convs=[conv('hsk2-nouilles', 'Au restaurant de nouilles', '服务员', 'Serveur', 'Tu vas manger des nouilles avec une collègue après le travail.', {
  'a': node('你好！请问吃什么？', 'Nǐ hǎo! Qǐngwèn chī shénme?', 'Bonjour ! Qu’est-ce que vous mangez ?', [
     o('一碗面条，不要羊肉。', 'Yì wǎn miàntiáo, bú yào yángròu.', 'Un bol de nouilles, sans mouton.', True, 'b'),
     o('我要服务员。', 'Wǒ yào fúwùyuán.', 'Je veux le serveur.', fix='Le serveur, c’est lui ! Dis ce que tu veux manger : « 一碗面条 ».')]),
  'b': node('好的。还要什么？', 'Hǎo de. Hái yào shénme?', 'Très bien. Autre chose ?', [
     o('还要一杯牛奶。', 'Hái yào yì bēi niúnǎi.', 'Un verre de lait aussi.', True, 'c'),
     o('不要了，谢谢。', 'Bú yào le, xièxie.', 'Ce sera tout, merci.', True, 'c'),
     o('一杯牛奶很好吃。', 'Yì bēi niúnǎi hěn hǎochī.', 'Un verre de lait très bon à manger.', fix='好吃 se dit pour ce qu’on mange. Pour commander, dis « 还要一杯牛奶 ».')]),
  'c': node('面条好吃吗？', 'Miàntiáo hǎochī ma?', 'Les nouilles sont bonnes ?', [
     o('非常好吃！我明天再来。', 'Fēicháng hǎochī! Wǒ míngtiān zài lái.', 'Délicieuses ! Je reviendrai demain.', True, 'end'),
     o('非常好吃！我昨天再来。', 'Fēicháng hǎochī! Wǒ zuótiān zài lái.', '(erreur de temps)', fix='再 parle du futur : « 我明天再来 » (demain), pas 昨天 (hier).')]),
  'end': node('欢迎再来！', 'Huānyíng zài lái!', 'Au plaisir de vous revoir !', end=True)})],
 bonus=[{'h': '民以食为天', 'p': 'mín yǐ shí wéi tiān', 'fr': 'Pour le peuple, manger passe avant tout', 'note': 'Proverbe ancien : en Chine, le repas est sacré. C’est pour ça qu’on se salue avec 你吃饭了吗？'}]))

# ---------------- HSK 2 · 9 ----------------
PACKS.append(dict(id='hsk2-09', file='hsk2-09-inviter.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 9 — Entrer, sortir, offrir',
 desc='Accueillir quelqu’un, offrir un cadeau, dire « ne fais pas ça », entrer et sortir. 15 mots HSK 2 et 13 phrases pour t’en servir.',
 grammar={'title': '别 : « ne… pas ! » (interdire gentiment)',
  'explain': 'Pour dire à quelqu’un de ne pas faire quelque chose, mets 别 (bié) devant le verbe : 别走 = ne pars pas. On ajoute souvent 了 à la fin pour adoucir : 别送了 = ne te dérange pas pour me raccompagner.',
  'examples': [ex('别笑！', 'Bié xiào!', 'Ne ris pas !'), ex('别担心。', 'Bié dānxīn.', 'Ne t’inquiète pas.'), ex('别送了，谢谢！', 'Bié sòng le, xièxie!', 'Ne me raccompagne pas, merci !'), ex('别在这儿吃饭。', 'Bié zài zhèr chī fàn.', 'Ne mange pas ici.')],
  'tip': '别 s’utilise pour parler à quelqu’un. Pour décrire (« il ne mange pas »), on garde 不.'},
 items=items('''
h209_shouji | 手机 | shou-ji | 3 1 | | Téléphone portable
h209_shoubiao | 手表 | shou-biao | 3 3 | 2 3 | Montre
h209_baozhi | 报纸 | bao-zhi | 4 3 | | Journal
h209_qianbi | 铅笔 | qian-bi | 1 3 | | Crayon
h209_song | 送 | song | 4 | | Offrir ; raccompagner
h209_ta | 它 | ta | 1 | | Il, elle (objet, animal)
h209_xiao | 笑 | xiao | 4 | | Rire, sourire
h209_huanying | 欢迎 | huan-ying | 1 2 | | Bienvenue, accueillir
h209_jin | 进 | jin | 4 | | Entrer
h209_chu | 出 | chu | 1 | | Sortir
h209_wai | 外 | wai | 4 | | Dehors, extérieur
h209_wang | 往 | wang | 3 | | Vers, en direction de
h209_rang | 让 | rang | 4 | | Laisser, faire faire
h209_bie | 别 | bie | 2 | | Ne… pas ! (défense)
h209_chuan | 船 | chuan | 2 | | Bateau
h209_s_huanying | 欢迎欢迎 | huan-ying huan-ying | 1 2 1 2 | | Bienvenue !
h209_s_qingjin | 请进 | qing jin | 3 4 | | Entre, je t’en prie | Quand quelqu’un frappe au bureau, dis : 请进！
h209_s_chuqu | 我出去一下 | wo chu-qu yi-xia | 3 1 0 2 4 | | Je sors un instant
h209_s_waimian | 在外面 | zai wai-mian | 4 4 0 | | Dehors
h209_s_wangyou | 往右走 | wang you zou | 3 4 3 | | Va vers la droite
h209_s_songni | 这是送你的 | zhe shi song ni de | 4 4 4 3 0 | | C’est pour toi (un cadeau)
h209_s_songnihuijia | 我送你回家 | wo song ni hui jia | 3 4 3 2 1 | | Je te raccompagne chez toi
h209_s_biexiao | 别笑 | bie xiao | 2 4 | | Ne ris pas !
h209_s_biedanxin | 别担心 | bie dan-xin | 2 1 1 | | Ne t’inquiète pas | Quand une collègue a fait une erreur, rassure-la : 别担心！
h209_s_biezou | 别走 | bie zou | 2 3 | | Ne pars pas !
h209_s_rangwokan | 让我看看 | rang wo kan-kan | 4 3 4 0 | | Laisse-moi voir
h209_s_shoujizainar | 我的手机在哪儿 | wo de shou-ji zai na-r | 3 0 3 1 4 3 0 | | Où est mon téléphone ?
h209_s_tazai | 它在桌子上 | ta zai zhuo-zi shang | 1 4 1 0 4 | | Il est sur la table
'''),
 pairs=[pair(('进', 'jin', 4, 'entrer'), ('今', 'jin', 1, 'aujourd’hui (今天)')), pair(('笑', 'xiao', 4, 'rire'), ('小', 'xiao', 3, 'petit'))],
 chars=chars('''
进 | jìn | entrer | 辶 | marche
出 | chū | sortir | 凵 | creux
外 | wài | dehors | 夕 | soir
送 | sòng | offrir | 辶 | marche
别 | bié | ne… pas ! | 刂 | couteau
笑 | xiào | rire | 竹 | bambou
船 | chuán | bateau | 舟 | barque
纸 | zhǐ | papier | 纟 | soie
'''),
 convs=[conv('hsk2-invitation', 'Invitée chez une collègue', '小王', 'Collègue', 'Une collègue chinoise t’invite chez elle. Tu arrives avec un petit cadeau.', {
  'a': node('欢迎欢迎！请进！', 'Huānyíng huānyíng! Qǐng jìn!', 'Bienvenue ! Entre, je t’en prie !', [
     o('谢谢！这是送你的。', 'Xièxie! Zhè shì sòng nǐ de.', 'Merci ! C’est pour toi.', True, 'b'),
     o('我出去一下。', 'Wǒ chūqu yíxià.', 'Je sors un instant.', fix='Tu viens d’arriver ! Dis merci et offre ton cadeau : « 这是送你的 ».')]),
  'b': node('太客气了！哇，一块手表！', 'Tài kèqi le! Wā, yí kuài shǒubiǎo!', 'Il ne fallait pas ! Oh, une montre !', [
     o('你喜欢吗？', 'Nǐ xǐhuan ma?', 'Elle te plaît ?', True, 'c'),
     o('别笑！', 'Bié xiào!', 'Ne ris pas !', fix='别笑 = ne ris pas ! Elle est contente : demande-lui plutôt « 你喜欢吗？ ».')]),
  'c': node('非常喜欢！很晚了，我送你回家吧。', 'Fēicháng xǐhuan! Hěn wǎn le, wǒ sòng nǐ huí jiā ba.', 'Elle me plaît beaucoup ! Il est tard, je te raccompagne.', [
     o('别送了，谢谢！', 'Bié sòng le, xièxie!', 'Ne te dérange pas, merci !', True, 'end'),
     o('好，谢谢你！', 'Hǎo, xièxie nǐ!', 'D’accord, merci !', True, 'end'),
     o('不送了！', 'Bú sòng le!', '(mauvais mot)', fix='Pour dire à quelqu’un de ne pas faire quelque chose, on dit 别 : « 别送了 ».')]),
  'end': node('好，路上小心！', 'Hǎo, lùshang xiǎoxīn!', 'D’accord, fais attention sur la route !', end=True)})],
 bonus=[{'h': '礼轻情意重', 'p': 'lǐ qīng qíngyì zhòng', 'fr': 'Petit cadeau, grande amitié', 'note': 'Ce qui compte, ce n’est pas le prix du cadeau mais l’intention.'}]))

# ---------------- HSK 2 · 10 ----------------
PACKS.append(dict(id='hsk2-10', file='hsk2-10-examen.json', branch='hsk', level=2, publish=False,
 title='HSK 2 · 10 — Examen, raisons et avis',
 desc='Dire comment on fait quelque chose, demander pourquoi, dire « bien que… mais… », préparer ton examen. 14 mots HSK 2 et 15 phrases pour t’en servir.',
 grammar={'title': 'Verbe + 得 + adjectif : dire comment on fait',
  'explain': 'Pour dire comment quelqu’un fait une action, on met 得 (de) après le verbe, puis l’adjectif : 说得很好 = parler très bien, 跑得很快 = courir vite. Pour la négation, 不 va après 得 : 说得不好 = ne pas bien parler.',
  'examples': [ex('你说得很好。', 'Nǐ shuō de hěn hǎo.', 'Tu parles très bien.'), ex('她跑得很快。', 'Tā pǎo de hěn kuài.', 'Elle court très vite.'), ex('我写得不好。', 'Wǒ xiě de bù hǎo.', 'Je n’écris pas bien.'), ex('你做得对。', 'Nǐ zuò de duì.', 'Tu as bien fait.')],
  'tip': '虽然… 但是… = « bien que… mais… » : en chinois on garde les deux mots, 虽然很难，但是我喜欢.'},
 items=items('''
h210_kaoshi | 考试 | kao-shi | 3 4 | | Examen, passer un examen
h210_ke | 课 | ke | 4 | | Cours, leçon
h210_jiaoshi | 教室 | jiao-shi | 4 4 | | Salle de classe
h210_ti | 题 | ti | 2 | | Question (d’exercice)
h210_wenti | 问题 | wen-ti | 4 2 | | Question, problème
h210_weishenme | 为什么 | wei-shen-me | 4 2 0 | | Pourquoi
h210_suiran | 虽然 | sui-ran | 1 2 | | Bien que
h210_danshi | 但是 | dan-shi | 4 4 | | Mais
h210_keneng | 可能 | ke-neng | 3 2 | | Peut-être, possible
h210_de | 得 | de | 0 | | (après un verbe : 说得很好)
h210_zhe | 着 | zhe | 0 | | (état qui dure : 开着)
h210_yixia | 一下 | yi-xia | 2 4 | | Un peu, un instant (après un verbe)
h210_shuohua | 说话 | shuo-hua | 1 4 | | Parler
h210_dui | 对 | dui | 4 | | Juste, correct
h210_jiu | 就 | jiu | 4 | | Tout de suite, justement
h210_s_shuodehao | 你说得很好 | ni shuo de hen hao | 3 1 0 3 3 | 3 1 0 2 3 | Tu parles très bien
h210_s_paodekuai | 她跑得很快 | ta pao de hen kuai | 1 3 0 3 4 | | Elle court très vite
h210_s_shuodebuhao | 我说得不好 | wo shuo de bu hao | 3 1 0 4 3 | | Je ne parle pas bien
h210_s_weishenme | 你为什么不来 | ni wei-shen-me bu lai | 3 4 2 0 4 2 | | Pourquoi tu ne viens pas ?
h210_s_kaoshi | 因为我要考试 | yin-wei wo yao kao-shi | 1 4 3 4 3 4 | | Parce que j’ai un examen
h210_s_suiran | 虽然很累，但是我很高兴 | sui-ran hen lei dan-shi wo hen gao-xing | 1 2 3 4 4 4 3 3 1 4 | 1 2 3 4 4 4 2 3 1 4 | Je suis fatiguée, mais contente
h210_s_keneng | 可能会下雨 | ke-neng hui xia yu | 3 2 4 4 3 | | Il va peut-être pleuvoir
h210_s_shuodedui | 你说得对 | ni shuo de dui | 3 1 0 4 | | Tu as raison | Quand ton chef d’équipe a raison, dis-lui : 你说得对。
h210_s_duibudui | 对不对 | dui bu dui | 4 0 4 | | C’est juste ? (n’est-ce pas ?)
h210_s_kaizhe | 门开着 | men kai zhe | 2 1 0 | | La porte est ouverte
h210_s_biezhanzhe | 别站着，请坐 | bie zhan zhe qing zuo | 2 4 0 3 4 | | Ne reste pas debout, assieds-toi
h210_s_kanyixia | 你看一下 | ni kan yi-xia | 3 4 2 4 | | Regarde un peu | Montre une chaussure abîmée à ton chef d’équipe : 你看一下。
h210_s_youwenti | 有问题吗 | you wen-ti ma | 3 4 2 0 | | Il y a un problème ? Des questions ?
h210_s_tihennan | 这个题很难 | zhe-ge ti hen nan | 4 0 2 3 2 | | Cette question est difficile
h210_s_zaijiaoshi | 我们在教室上课 | wo-men zai jiao-shi shang ke | 3 0 4 4 4 4 4 | | Nous avons cours dans la salle de classe
'''),
 pairs=[pair(('题', 'ti', 2, 'question'), ('体', 'ti', 3, 'corps (身体)')), pair(('课', 'ke', 4, 'cours'), ('可', 'ke', 3, 'pouvoir (可以)'))],
 chars=chars('''
考 | kǎo | passer un examen | 耂 | vieux
试 | shì | essayer | 讠 | parole
课 | kè | cours | 讠 | parole
题 | tí | question | 页 | page
为 | wèi | pour | 丶 | point
虽 | suī | bien que | 虫 | insecte
但 | dàn | mais | 亻 | personne
能 | néng | pouvoir | 月 | chair
'''),
 convs=[conv('hsk2-examen', 'Bientôt l’examen', '小陈', 'Collègue', 'Pendant la pause, une collègue chinoise t’entend parler chinois.', {
  'a': node('{name}，你的汉语说得很好！', '{name}, nǐ de Hànyǔ shuō de hěn hǎo!', '{name}, tu parles très bien chinois !', [
     o('哪里哪里，我说得不好。', 'Nǎli nǎli, wǒ shuō de bù hǎo.', 'Oh non, je ne parle pas bien.', True, 'b'),
     o('我说很好。', 'Wǒ shuō hěn hǎo.', '(phrase mal construite)', fix='Après le verbe, il faut 得 : « 我说得不好 ». Et en Chine, on répond avec modestie !')]),
  'b': node('你为什么学汉语？', 'Nǐ wèishénme xué Hànyǔ?', 'Pourquoi tu apprends le chinois ?', [
     o('因为我要考试。', 'Yīnwèi wǒ yào kǎoshì.', 'Parce que je vais passer un examen.', True, 'c'),
     o('我为什么学汉语。', 'Wǒ wèishénme xué Hànyǔ.', '(tu répètes la question)', fix='Pour répondre « parce que », commence par 因为 : « 因为我要考试 ».')]),
  'c': node('考试难吗？', 'Kǎoshì nán ma?', 'L’examen est difficile ?', [
     o('虽然很难，但是我很喜欢。', 'Suīrán hěn nán, dànshì wǒ hěn xǐhuan.', 'C’est difficile, mais j’aime beaucoup.', True, 'end'),
     o('虽然很难，所以我很喜欢。', 'Suīrán hěn nán, suǒyǐ wǒ hěn xǐhuan.', '(mauvais mot)', fix='Avec 虽然 (bien que), on met 但是 (mais), pas 所以 (donc) : « 虽然很难，但是我很喜欢 ».')]),
  'end': node('你说得对！加油！', 'Nǐ shuō de duì! Jiāyóu!', 'Tu as raison ! Courage !', end=True)})],
 bonus=[{'h': '活到老，学到老', 'p': 'huó dào lǎo, xué dào lǎo', 'fr': 'On apprend toute sa vie', 'note': 'Mot à mot « vivre jusqu’à vieux, apprendre jusqu’à vieux ».'}]))

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
n_shuang | 双 | shuang | 1 | | Paire (pour compter les chaussures)
n_xiangzi | 箱子 | xiang-zi | 1 0 | | Carton, caisse
n_shu | 数 | shu | 3 | | Compter
n_shuyixia | 我数一下 | wo shu yi-xia | 3 3 2 4 | 2 3 2 4 | Je vais compter | Avant de fermer un carton, dis à ton chef d’équipe : 我数一下。
n_shucuo | 数错了 | shu cuo le | 3 4 0 | | Je me suis trompée en comptant
n_zaishu | 再数一遍 | zai shu yi bian | 4 3 2 4 | | Recompte encore une fois
n_yixiangduoshao | 一箱多少双 | yi xiang duo-shao shuang | 4 1 1 0 1 | | Combien de paires par carton ? | Demande à ton chef d’équipe : 一箱多少双？
n_shiershuang | 一箱十二双 | yi xiang shi-er shuang | 4 1 2 4 1 | | Douze paires par carton
n_jintian | 今天做了多少双 | jin-tian zuo le duo-shao shuang | 1 1 4 0 1 0 1 | | Combien de paires aujourd’hui ?
n_jiushi | 我做了九十双 | wo zuo le jiu-shi shuang | 3 4 0 3 2 1 | | J’ai fait quatre-vingt-dix paires
n_wubai | 五百双 | wu-bai shuang | 3 3 1 | 2 3 1 | Cinq cents paires
n_yiqian | 一千 | yi-qian | 4 1 | | Mille (1 000)
n_haichaduoshao | 还差多少 | hai cha duo-shao | 2 4 1 0 | | Il en manque combien ?
n_haiyoujixiang | 还有几箱 | hai you ji xiang | 2 3 3 1 | 2 2 3 1 | Il reste combien de cartons ?
n_duole | 多了两双 | duo le liang shuang | 1 0 3 1 | | Il y a deux paires en trop
n_shaole | 少了一双 | shao le yi shuang | 3 0 4 1 | | Il manque une paire
n_goule | 够了 | gou le | 4 0 | | Ça suffit, c’est assez
n_duoshaoma | 多少码 | duo-shao ma | 1 0 3 | | Quelle pointure ?
n_sanshibama | 三十八码 | san-shi-ba ma | 1 2 1 3 | | Pointure 38
n_zhuangxiang | 装箱 | zhuang xiang | 1 1 | | Mettre en carton
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
q_yigong | 一共多少钱 | yi-gong duo-shao qian | 2 4 1 0 2 | | Ça fait combien en tout ? | À la caisse d’une boutique chinoise, demande : 一共多少钱？
q_youmeiyou | 有没有鸡蛋 | you mei you ji-dan | 3 2 3 1 4 | | Tu as des œufs ?
q_geiwo | 给我两个 | gei wo liang ge | 3 3 3 0 | 2 2 3 0 | Donne-m’en deux
q_xinxian | 新鲜吗 | xin-xian ma | 1 1 0 | | C’est frais ?
q_tudou | 土豆 | tu-dou | 3 4 | | Pomme de terre
q_yangcong | 洋葱 | yang-cong | 2 1 | | Oignon
q_lajiao | 辣椒 | la-jiao | 4 1 | | Piment
q_xiangjiao | 香蕉 | xiang-jiao | 1 1 | | Banane
q_jirou | 鸡肉 | ji-rou | 1 4 | | Viande de poulet
q_niurou | 牛肉 | niu-rou | 2 4 | | Viande de bœuf
q_mianbao | 面包 | mian-bao | 4 1 | | Pain
q_yan | 盐 | yan | 2 | | Sel
q_tang | 糖 | tang | 2 | | Sucre
q_suliaodai | 塑料袋 | su-liao-dai | 4 4 4 | | Sachet en plastique
q_xianjin | 现金 | xian-jin | 4 1 | | Espèces (billets, pièces)
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

# ---------------- Vie quotidienne · 2 : restaurant ----------------
PACKS.append(dict(id='quotidien-02-restaurant', file='quotidien-02-restaurant.json', branch='quotidien', publish=False,
 title='Vie quotidienne · Au restaurant et à la cantine',
 desc='Commander un plat, dire si tu as faim, demander pas trop piquant, payer ou emporter.',
 grammar={'title': '来 + quantité : commander',
  'explain': 'Au restaurant, les Chinois ne disent presque jamais « je voudrais ». Ils disent 来 (lái, « venir ») + la quantité + le plat : 来一碗米饭 = un bol de riz, s’il te plaît. C’est poli et très naturel.',
  'examples': [ex('来一碗米饭。', 'Lái yì wǎn mǐfàn.', 'Un bol de riz, s’il te plaît.'), ex('来两瓶矿泉水。', 'Lái liǎng píng kuàngquánshuǐ.', 'Deux bouteilles d’eau minérale.'), ex('再来一碗。', 'Zài lái yì wǎn.', 'Encore un bol.'), ex('来一个炒饭，不要太辣。', 'Lái yí ge chǎofàn, bú yào tài là.', 'Un riz sauté, pas trop piquant.')],
  'tip': '碗 (bol) et 瓶 (bouteille) servent aussi à compter : 一碗汤 = un bol de soupe, 一瓶水 = une bouteille d’eau.'},
 items=items('''
q2_shitang | 食堂 | shi-tang | 2 2 | | Cantine | À midi, demande à une collègue : 你去食堂吗？
q2_wan | 碗 | wan | 3 | | Bol
q2_kuaizi | 筷子 | kuai-zi | 4 0 | | Baguettes
q2_shaozi | 勺子 | shao-zi | 2 0 | | Cuillère
q2_caidan | 菜单 | cai-dan | 4 1 | | Menu, la carte
q2_diancai | 点菜 | dian cai | 3 4 | | Commander (des plats)
q2_maidan | 买单 | mai dan | 3 1 | | Payer l’addition
q2_dabao | 打包 | da bao | 3 1 | | Emballer pour emporter
q2_la | 辣 | la | 4 | | Piquant, pimenté
q2_tian | 甜 | tian | 2 | | Sucré
q2_xian | 咸 | xian | 2 | | Salé
q2_e | 饿 | e | 4 | | Avoir faim
q2_ke | 渴 | ke | 3 | | Avoir soif
q2_bao | 饱 | bao | 3 | | Rassasiée (j’ai assez mangé)
q2_tang | 汤 | tang | 1 | | Soupe
q2_jiaozi | 饺子 | jiao-zi | 3 0 | | Raviolis chinois
q2_chaofan | 炒饭 | chao-fan | 3 4 | | Riz sauté
q2_kuangquanshui | 矿泉水 | kuang-quan-shui | 4 2 3 | | Eau minérale
q2_s_laiyiwan | 来一碗米饭 | lai yi wan mi-fan | 2 4 3 3 4 | 2 4 2 3 4 | Un bol de riz, s’il te plaît | Au restaurant chinois ou à la cantine, commande : 来一碗米饭。
q2_s_buyaotaila | 不要太辣 | bu yao tai la | 2 4 4 4 | | Pas trop piquant
q2_s_youbulade | 有不辣的吗 | you bu la de ma | 3 2 4 0 0 | | Il y a des plats pas piquants ?
q2_s_zheshishenmecai | 这是什么菜 | zhe shi shen-me cai | 4 4 2 0 4 | | C’est quel plat ? | À la cantine, montre un plat que tu ne connais pas et demande : 这是什么菜？
q2_s_eile | 我饿了 | wo e le | 3 4 0 | | J’ai faim
q2_s_chibaole | 我吃饱了 | wo chi bao le | 3 1 3 0 | | J’ai bien mangé, je n’ai plus faim
q2_s_buchizhurou | 我不吃猪肉 | wo bu chi zhu-rou | 3 4 1 1 4 | | Je ne mange pas de porc
q2_s_laiyiping | 来一瓶矿泉水 | lai yi ping kuang-quan-shui | 2 4 2 4 2 3 | | Une bouteille d’eau minérale
q2_s_zailaiyiwan | 再来一碗 | zai lai yi wan | 4 2 4 3 | | Encore un bol, s’il te plaît
q2_s_zaizhechi | 在这儿吃还是带走 | zai zhe-r chi hai-shi dai zou | 4 4 0 1 2 0 4 3 | | Sur place ou à emporter ?
q2_s_bangwodabao | 帮我打包 | bang wo da bao | 1 3 3 1 | 1 2 3 1 | Mets-le-moi à emporter
q2_s_fuwuyuanmaidan | 服务员，买单 | fu-wu-yuan mai dan | 2 4 2 3 1 | | L’addition, s’il vous plaît !
'''),
 pairs=[pair(('汤', 'tang', 1, 'soupe'), ('糖', 'tang', 2, 'sucre')), pair(('饱', 'bao', 3, 'rassasiée'), ('包', 'bao', 1, 'sac, emballer'))],
 chars=chars('''
饭 | fàn | repas, riz cuit | 饣 | nourriture
饿 | è | avoir faim | 饣 | nourriture
饱 | bǎo | rassasiée | 饣 | nourriture
碗 | wǎn | bol | 石 | pierre
筷 | kuài | baguette | 竹 | bambou
汤 | tāng | soupe | 氵 | eau
辣 | là | piquant | 辛 | saveur forte
甜 | tián | sucré | 舌 | langue
'''),
 convs=[conv('restaurant', 'Un midi au petit restaurant', '服务员', 'Serveuse', 'Pause de midi. Tu vas manger dans un petit restaurant chinois près de l’usine.', {
  'a': node('你好！吃什么？', 'Nǐ hǎo! Chī shénme?', 'Bonjour ! Tu manges quoi ?', [
     o('来一个炒饭。', 'Lái yí ge chǎofàn.', 'Un riz sauté, s’il te plaît.', True, 'b'),
     o('我饿了。', 'Wǒ è le.', 'J’ai faim.', fix='Elle sait que tu as faim ! Dis ce que tu veux : « 来一个炒饭 ».')]),
  'b': node('要辣的吗？', 'Yào là de ma?', 'Tu le veux piquant ?', [
     o('不要太辣，谢谢。', 'Bú yào tài là, xièxie.', 'Pas trop piquant, merci.', True, 'c'),
     o('要，我喜欢辣的。', 'Yào, wǒ xǐhuan là de.', 'Oui, j’aime le piquant.', True, 'c'),
     o('我很辣。', 'Wǒ hěn là.', 'Je suis très piquante.', fix='我很辣 = « je suis piquante » ! Dis « 不要太辣 » (pas trop piquant) ou « 要辣的 ».')]),
  'c': node('喝什么？', 'Hē shénme?', 'Et à boire ?', [
     o('来一瓶矿泉水。', 'Lái yì píng kuàngquánshuǐ.', 'Une bouteille d’eau minérale.', True, 'd'),
     o('来一碗矿泉水。', 'Lái yì wǎn kuàngquánshuǐ.', 'Un bol d’eau minérale.', fix='L’eau minérale, c’est en bouteille : « 一瓶矿泉水 ».')]),
  'd': node('吃饱了吗？', 'Chī bǎo le ma?', 'Tu as bien mangé ?', [
     o('吃饱了！服务员，买单。', 'Chī bǎo le! Fúwùyuán, mǎidān.', 'Oui, j’ai bien mangé ! L’addition, s’il vous plaît.', True, 'end'),
     o('我渴了。', 'Wǒ kě le.', 'J’ai soif.', fix='渴 = avoir soif. Pour dire que tu as assez mangé : « 吃饱了 ».')]),
  'end': node('一共二十五块。谢谢，慢走！', 'Yígòng èrshíwǔ kuài. Xièxie, màn zǒu!', 'Ça fait vingt-cinq yuans en tout. Merci, au revoir !', end=True)})],
 bonus=[{'h': '慢走', 'p': 'màn zǒu', 'fr': 'Au revoir (à quelqu’un qui part)', 'note': 'Mot à mot « marche lentement » : le patron le dit aux clients qui s’en vont.'}]))

# ---------------- Vie quotidienne · 3 : transport ----------------
PACKS.append(dict(id='quotidien-03-transport', file='quotidien-03-transport.json', branch='quotidien', publish=False,
 title='Vie quotidienne · Moto-taxi, bus et taxi',
 desc='Dire où tu vas, demander le prix, guider le chauffeur et demander l’arrêt.',
 grammar={'title': '在 + lieu + verbe : dire où ça se passe',
  'explain': 'En chinois, le lieu vient AVANT l’action : 在 (zài) + lieu + verbe. Pour dire « arrête-toi ici », on dit 在这儿停 (mot à mot « ici arrête-toi »). En français c’est l’inverse, alors entraîne-toi !',
  'examples': [ex('请在这儿停。', 'Qǐng zài zhèr tíng.', 'Arrête-toi ici, s’il te plaît.'), ex('在路口左拐。', 'Zài lùkǒu zuǒ guǎi.', 'Au carrefour, tourne à gauche.'), ex('我在车站下车。', 'Wǒ zài chēzhàn xià chē.', 'Je descends à la gare.'), ex('我在路口等你。', 'Wǒ zài lùkǒu děng nǐ.', 'Je t’attends au carrefour.')],
  'tip': 'Pour appeler un chauffeur poliment, dis 师傅 (shīfu) : c’est le mot normal pour tous les chauffeurs et les ouvriers qualifiés.'},
 items=items('''
q3_motuoche | 摩托车 | mo-tuo-che | 2 1 1 | | Moto
q3_modi | 摩的 | mo-di | 2 1 | | Moto-taxi (zémidjan)
q3_siji | 司机 | si-ji | 1 1 | | Chauffeur
q3_shifu | 师傅 | shi-fu | 1 0 | | Chef ! (pour appeler un chauffeur) | En moto-taxi ou en taxi avec un chauffeur chinois, appelle-le : 师傅！
q3_toukui | 头盔 | tou-kui | 2 1 | | Casque
q3_gongjiaoche | 公交车 | gong-jiao-che | 1 1 1 | | Bus (en ville)
q3_chezhan | 车站 | che-zhan | 1 4 | | Gare routière, station
q3_zhan | 站 | zhan | 4 | | Arrêt (de bus)
q3_shangche | 上车 | shang che | 4 1 | | Monter (dans un véhicule)
q3_xiache | 下车 | xia che | 4 1 | | Descendre (d’un véhicule)
q3_ting | 停 | ting | 2 | | S’arrêter
q3_lukou | 路口 | lu-kou | 4 3 | | Carrefour
q3_hongludeng | 红绿灯 | hong-lv-deng | 2 4 1 | | Feu (de circulation)
q3_guai | 拐 | guai | 3 | | Tourner
q3_yizhizou | 一直走 | yi-zhi zou | 4 2 3 | | Tout droit
q3_duche | 堵车 | du che | 3 1 | | Embouteillage
q3_dizhi | 地址 | di-zhi | 4 3 | | Adresse
q3_s_quxiechang | 我去鞋厂 | wo qu xie-chang | 3 4 2 3 | | Je vais à l’usine de chaussures
q3_s_daoshichang | 到市场多少钱 | dao shi-chang duo-shao qian | 4 4 3 1 0 2 | | C’est combien jusqu’au marché ? | Avant de monter, demande le prix au chauffeur : 到市场多少钱？
q3_s_zaizheerting | 请在这儿停 | qing zai zhe-r ting | 3 4 4 0 2 | | Arrête-toi ici, s’il te plaît
q3_s_zuoguai | 在路口左拐 | zai lu-kou zuo guai | 4 4 3 3 3 | 4 4 3 2 3 | Au carrefour, tourne à gauche
q3_s_youguai | 右拐 | you guai | 4 3 | | Tourne à droite
q3_s_yaoxiache | 我要下车 | wo yao xia che | 3 4 4 1 | | Je veux descendre
q3_s_daolema | 到了吗 | dao le ma | 4 0 0 | | On est arrivés ?
q3_s_duchele | 堵车了 | du che le | 3 1 0 | | Ça bouchonne
q3_s_xiayizhan | 下一站是哪儿 | xia yi zhan shi na-r | 4 2 4 4 3 0 | | Le prochain arrêt, c’est où ?
q3_s_zheluche | 这路车去市场吗 | zhe lu che qu shi-chang ma | 4 4 1 4 4 3 0 | | Ce bus va au marché ?
q3_s_dengni | 我在路口等你 | wo zai lu-kou deng ni | 3 4 4 3 3 3 | 3 4 4 3 2 3 | Je t’attends au carrefour
'''),
 pairs=[pair(('停', 'ting', 2, 's’arrêter'), ('听', 'ting', 1, 'écouter')), pair(('拐', 'guai', 3, 'tourner'), ('怪', 'guai', 4, 'bizarre'))],
 chars=chars('''
站 | zhàn | arrêt, se tenir debout | 立 | debout
停 | tíng | s’arrêter | 亻 | personne
拐 | guǎi | tourner | 扌 | main
堵 | dǔ | boucher | 土 | terre
灯 | dēng | lampe, feu | 火 | feu
机 | jī | machine | 木 | bois
摩 | mó | frotter (dans « moto ») | 手 | main
'''),
 convs=[conv('transport', 'En taxi dans une ville chinoise', '司机', 'Chauffeur de taxi', 'Tu es en voyage en Chine. Tu montes dans un taxi pour aller à la gare.', {
  'a': node('你好，去哪儿？', 'Nǐ hǎo, qù nǎr?', 'Bonjour, on va où ?', [
     o('师傅，去火车站。', 'Shīfu, qù huǒchēzhàn.', 'Chef, à la gare, s’il vous plaît.', True, 'b'),
     o('我在这儿。', 'Wǒ zài zhèr.', 'Je suis ici.', fix='Il demande où tu vas : réponds « 去… » + le lieu, par exemple « 去火车站 ».')]),
  'b': node('前面堵车，我们右拐，好吗？', 'Qiánmiàn dǔchē, wǒmen yòu guǎi, hǎo ma?', 'Ça bouchonne devant, on tourne à droite, d’accord ?', [
     o('好，没问题。', 'Hǎo, méi wèntí.', 'D’accord, pas de problème.', True, 'c'),
     o('我要下车。', 'Wǒ yào xià chē.', 'Je veux descendre.', fix='Pas besoin de descendre ! Il te propose un autre chemin : dis « 好，没问题 ».')]),
  'c': node('到了。在这儿停吗？', 'Dào le. Zài zhèr tíng ma?', 'On est arrivés. Je m’arrête ici ?', [
     o('对，请在这儿停。多少钱？', 'Duì, qǐng zài zhèr tíng. Duōshao qián?', 'Oui, arrêtez-vous ici. C’est combien ?', True, 'end'),
     o('请这儿在停。', 'Qǐng zhèr zài tíng.', '(phrase mal construite)', fix='在 se met juste avant le lieu, puis vient le verbe : « 请在这儿停 ».')]),
  'end': node('三十块。谢谢！', 'Sānshí kuài. Xièxie!', 'Trente yuans. Merci !', end=True)})],
 bonus=[{'h': '一路平安', 'p': 'yílù píng’ān', 'fr': 'Bon voyage !', 'note': 'Mot à mot « toute la route en paix » : à dire à quelqu’un qui part loin.'}]))

# ---------------- Vie quotidienne · 4 : santé ----------------
PACKS.append(dict(id='quotidien-04-sante', file='quotidien-04-sante.json', branch='quotidien', publish=False,
 title='Vie quotidienne · Pharmacie et médecin',
 desc='Dire où tu as mal, expliquer que tu as de la fièvre ou que tu t’es blessée, comprendre comment prendre un médicament.',
 grammar={'title': '… 疼 : dire où tu as mal',
  'explain': 'Pour dire « j’ai mal à… », on dit la partie du corps puis 疼 (téng, « avoir mal ») : 我头疼 = j’ai mal à la tête (mot à mot « moi tête mal »). Pas besoin de verbe « avoir ».',
  'examples': [ex('我头疼。', 'Wǒ tóu téng.', 'J’ai mal à la tête.'), ex('我肚子疼。', 'Wǒ dùzi téng.', 'J’ai mal au ventre.'), ex('我的脚很疼。', 'Wǒ de jiǎo hěn téng.', 'J’ai très mal au pied.'), ex('你哪儿疼？', 'Nǐ nǎr téng?', 'Où as-tu mal ?')],
  'tip': 'Pour dire « je ne me sens pas bien » sans savoir où, dis simplement 我不舒服 (wǒ bù shūfu).'},
 items=items('''
q4_teng | 疼 | teng | 2 | | Avoir mal, douleur
q4_tou | 头 | tou | 2 | | Tête
q4_duzi | 肚子 | du-zi | 4 0 | | Ventre
q4_yao | 腰 | yao | 1 | | Bas du dos, reins
q4_shou | 手 | shou | 3 | | Main
q4_jiao | 脚 | jiao | 3 | | Pied
q4_ya | 牙 | ya | 2 | | Dent
q4_fashao | 发烧 | fa-shao | 1 1 | | Avoir de la fièvre
q4_ganmao | 感冒 | gan-mao | 3 4 | | Rhume, grippe
q4_kesou | 咳嗽 | ke-sou | 2 0 | | Tousser
q4_nveji | 疟疾 | nve-ji | 4 0 | | Paludisme
q4_yaodian | 药店 | yao-dian | 4 4 | | Pharmacie
q4_kanbing | 看病 | kan bing | 4 4 | | Aller voir le médecin
q4_shoushang | 受伤 | shou-shang | 4 1 | | Se blesser
q4_liuxue | 流血 | liu xue | 2 3 | | Saigner
q4_shufu | 舒服 | shu-fu | 1 0 | | Se sentir bien, à l’aise
q4_s_bushufu | 我不舒服 | wo bu shu-fu | 3 4 1 0 | | Je ne me sens pas bien | Si tu es malade à l’atelier, dis à ton chef d’équipe : 我不舒服。
q4_s_touteng | 我头疼 | wo tou teng | 3 2 2 | | J’ai mal à la tête
q4_s_duziteng | 我肚子疼 | wo du-zi teng | 3 4 0 2 | | J’ai mal au ventre
q4_s_yaoteng | 我腰疼 | wo yao teng | 3 1 2 | | J’ai mal au dos
q4_s_narteng | 哪儿疼 | na-r teng | 3 0 2 | | Où as-tu mal ?
q4_s_fashaole | 我发烧了 | wo fa-shao le | 3 1 1 0 | | J’ai de la fièvre
q4_s_shoushangle | 我的手受伤了 | wo de shou shou-shang le | 3 0 3 4 1 0 | | Je me suis blessée à la main | Si tu te blesses à une machine, préviens tout de suite ton chef : 我的手受伤了！
q4_s_ganmaoyao | 有感冒药吗 | you gan-mao yao ma | 3 3 4 4 0 | 2 3 4 4 0 | Vous avez un médicament contre le rhume ?
q4_s_jici | 一天吃几次 | yi tian chi ji ci | 4 1 1 3 4 | | Combien de fois par jour ?
q4_s_sanci | 一天三次 | yi tian san ci | 4 1 1 4 | | Trois fois par jour
q4_s_qukanbing | 我要去看病 | wo yao qu kan bing | 3 4 4 4 4 | | Je dois aller voir le médecin
q4_s_haoduole | 好多了 | hao duo le | 3 1 0 | | Ça va beaucoup mieux
q4_s_duoheshui | 多喝水 | duo he shui | 1 1 3 | | Bois beaucoup d’eau
'''),
 pairs=[pair(('腰', 'yao', 1, 'bas du dos'), ('药', 'yao', 4, 'médicament')), pair(('头', 'tou', 2, 'tête'), ('豆', 'dou', 4, 'haricot (土豆)'))],
 chars=chars('''
疼 | téng | avoir mal | 疒 | maladie
病 | bìng | maladie | 疒 | maladie
头 | tóu | tête | 大 | grand
肚 | dù | ventre | 月 | chair
腰 | yāo | bas du dos | 月 | chair
脚 | jiǎo | pied | 月 | chair
烧 | shāo | brûler, fièvre | 火 | feu
店 | diàn | magasin | 广 | abri
'''),
 convs=[conv('pharmacie', 'À la pharmacie', '店员', 'Pharmacienne', 'Tu ne te sens pas bien. Tu vas à la pharmacie chinoise près de l’usine.', {
  'a': node('你好，你哪儿不舒服？', 'Nǐ hǎo, nǐ nǎr bù shūfu?', 'Bonjour, qu’est-ce qui ne va pas ?', [
     o('我头疼，也发烧了。', 'Wǒ tóu téng, yě fāshāo le.', 'J’ai mal à la tête, et j’ai de la fièvre.', True, 'b'),
     o('我很舒服。', 'Wǒ hěn shūfu.', 'Je me sens très bien.', fix='舒服 = se sentir bien ! Dis « 我不舒服 », puis où tu as mal : « 我头疼 ».')]),
  'b': node('你咳嗽吗？', 'Nǐ késou ma?', 'Tu tousses ?', [
     o('有一点儿咳嗽。', 'Yǒu yìdiǎnr késou.', 'Je tousse un peu.', True, 'c'),
     o('不咳嗽。', 'Bù késou.', 'Je ne tousse pas.', True, 'c'),
     o('我是咳嗽。', 'Wǒ shì késou.', '(phrase mal construite)', fix='Pas besoin de 是 ici : dis « 有一点儿咳嗽 » (un peu) ou « 不咳嗽 ».')]),
  'c': node('你感冒了。这个药一天三次，一次两片。', 'Nǐ gǎnmào le. Zhège yào yì tiān sān cì, yí cì liǎng piàn.', 'Tu as un rhume. Ce médicament : trois fois par jour, deux comprimés à chaque fois.', [
     o('好的，饭前吃还是饭后吃？', 'Hǎo de, fàn qián chī háishi fàn hòu chī?', 'D’accord. Avant ou après le repas ?', True, 'd'),
     o('一天两次，对吗？', 'Yì tiān liǎng cì, duì ma?', 'Deux fois par jour, c’est ça ?', fix='Non : 一天三次 = trois fois par jour. 两片 = deux comprimés.')]),
  'd': node('饭后吃。多喝水，多休息。', 'Fàn hòu chī. Duō hē shuǐ, duō xiūxi.', 'Après le repas. Bois beaucoup d’eau et repose-toi bien.', [
     o('谢谢！多少钱？', 'Xièxie! Duōshao qián?', 'Merci ! C’est combien ?', True, 'end')]),
  'end': node('十五块。早日康复！', 'Shíwǔ kuài. Zǎorì kāngfù!', 'Quinze yuans. Bon rétablissement !', end=True)})],
 bonus=[{'h': '早日康复', 'p': 'zǎorì kāngfù', 'fr': 'Bon rétablissement !', 'note': 'À dire à une collègue malade : elle sera touchée que tu le dises en chinois.'}]))

# ---------------- Vie quotidienne · 5 : téléphone et WeChat ----------------
PACKS.append(dict(id='quotidien-05-wechat', file='quotidien-05-wechat.json', branch='quotidien', publish=False,
 title='Vie quotidienne · Téléphone et WeChat',
 desc='Échanger ton numéro, ajouter quelqu’un sur WeChat, envoyer un message ou un vocal, payer avec le QR code.',
 grammar={'title': '给 + personne + verbe : « à quelqu’un »',
  'explain': 'Pour dire « appeler quelqu’un » ou « envoyer un message à quelqu’un », on met 给 (gěi) + la personne AVANT le verbe : 给我打电话 = appelle-moi (mot à mot « à moi téléphone »).',
  'examples': [ex('给我打电话。', 'Gěi wǒ dǎ diànhuà.', 'Appelle-moi.'), ex('我给你发消息。', 'Wǒ gěi nǐ fā xiāoxi.', 'Je t’envoie un message.'), ex('你给组长打电话吧。', 'Nǐ gěi zǔzhǎng dǎ diànhuà ba.', 'Appelle le chef d’équipe.'), ex('她给我发了一个红包。', 'Tā gěi wǒ fā le yí ge hóngbāo.', 'Elle m’a envoyé une enveloppe rouge.')],
  'tip': 'Tu entendras aussi 我打电话给你 : c’est juste aussi, mais 我给你打电话 est la forme la plus courante.'},
 items=items('''
q5_weixin | 微信 | Wei-xin | 1 4 | | WeChat
q5_haoma | 号码 | hao-ma | 4 3 | | Numéro
q5_fa | 发 | fa | 1 | | Envoyer
q5_xiaoxi | 消息 | xiao-xi | 1 0 | | Message
q5_yuyin | 语音 | yu-yin | 3 1 | | Message vocal
q5_shipin | 视频 | shi-pin | 4 2 | | Vidéo, appel vidéo
q5_jia | 加 | jia | 1 | | Ajouter (en contact)
q5_sao | 扫 | sao | 3 | | Scanner
q5_erweima | 二维码 | er-wei-ma | 4 2 3 | | QR code
q5_chongdian | 充电 | chong dian | 1 4 | | Recharger (la batterie)
q5_guanji | 关机 | guan ji | 1 1 | | Éteindre (le téléphone)
q5_xinhao | 信号 | xin-hao | 4 4 | | Réseau (le signal)
q5_liuliang | 流量 | liu-liang | 2 4 | | Données mobiles (internet)
q5_mima | 密码 | mi-ma | 4 3 | | Mot de passe, code
q5_zhuanzhang | 转账 | zhuan zhang | 3 4 | | Envoyer de l’argent (virement)
q5_hongbao | 红包 | hong-bao | 2 1 | | Enveloppe rouge (argent offert)
q5_s_jiaweixin | 加个微信吧 | jia ge Wei-xin ba | 1 0 1 4 0 | | On s’ajoute sur WeChat ? | Propose à une collègue chinoise : 加个微信吧！
q5_s_saoni | 我扫你 | wo sao ni | 3 3 3 | 2 2 3 | Je scanne ton code
q5_s_haomaduoshao | 你的电话号码是多少 | ni de dian-hua hao-ma shi duo-shao | 3 0 4 4 4 3 4 1 0 | | C’est quoi ton numéro ?
q5_s_geiwoda | 给我打电话 | gei wo da dian-hua | 3 3 3 4 4 | 2 2 3 4 4 | Appelle-moi
q5_s_faxiaoxi | 给我发消息 | gei wo fa xiao-xi | 3 3 1 1 0 | 2 3 1 1 0 | Envoie-moi un message
q5_s_meidianle | 我的手机没电了 | wo de shou-ji mei dian le | 3 0 3 1 2 4 0 | | Mon téléphone n’a plus de batterie
q5_s_tingbuqing | 听不清楚 | ting bu qing-chu | 1 0 1 0 | | Je n’entends pas bien
q5_s_meixinhao | 这儿没有信号 | zhe-r mei-you xin-hao | 4 0 2 3 4 4 | | Il n’y a pas de réseau ici
q5_s_yihuirzaida | 一会儿再打 | yi-hui-r zai da | 2 4 0 4 3 | | Je rappelle tout à l’heure
q5_s_shoudaole | 收到了 | shou dao le | 1 4 0 | | Bien reçu | Quand ton chef t’envoie une consigne sur WeChat, réponds : 收到了！
q5_s_fageyuyin | 发个语音 | fa ge yu-yin | 1 0 3 1 | | Envoie un vocal
q5_s_saomafukuan | 扫二维码付款 | sao er-wei-ma fu kuan | 3 4 2 3 4 3 | | Payer en scannant le QR code
'''),
 pairs=[pair(('号', 'hao', 4, 'numéro'), ('好', 'hao', 3, 'bien')), pair(('发', 'fa', 1, 'envoyer'), ('法', 'fa', 3, 'France (法国)'))],
 chars=chars('''
微 | wēi | petit, micro | 彳 | pas
信 | xìn | lettre, message | 亻 | personne
号 | hào | numéro | 口 | bouche
码 | mǎ | code | 石 | pierre
扫 | sǎo | balayer, scanner | 扌 | main
发 | fā | envoyer | 又 | main
包 | bāo | sac, emballer | 勹 | envelopper
'''),
 convs=[conv('wechat', 'On s’ajoute sur WeChat ?', '小陈', 'Collègue', 'Une collègue chinoise sympathique veut garder le contact avec toi.', {
  'a': node('{name}，我们加个微信吧！', '{name}, wǒmen jiā ge Wēixìn ba!', '{name}, on s’ajoute sur WeChat ?', [
     o('好啊，我扫你。', 'Hǎo a, wǒ sǎo nǐ.', 'Avec plaisir, je scanne ton code.', True, 'b'),
     o('我没有钱。', 'Wǒ méiyǒu qián.', 'Je n’ai pas d’argent.', fix='Elle ne parle pas d’argent : 加微信 = s’ajouter sur WeChat. Dis « 好啊，我扫你 ».')]),
  'b': node('这是我的二维码。', 'Zhè shì wǒ de èrwéimǎ.', 'Voilà mon QR code.', [
     o('好了，我加你了。', 'Hǎo le, wǒ jiā nǐ le.', 'C’est bon, je t’ai ajoutée.', True, 'c'),
     o('二维码多少钱？', 'Èrwéimǎ duōshao qián?', 'Il coûte combien, le QR code ?', fix='Le QR code est gratuit ! Scanne-le, puis dis « 我加你了 ».')]),
  'c': node('收到了！晚上我给你发消息。', 'Shōudào le! Wǎnshang wǒ gěi nǐ fā xiāoxi.', 'Bien reçu ! Ce soir, je t’envoie un message.', [
     o('好的，也可以给我打电话。', 'Hǎo de, yě kěyǐ gěi wǒ dǎ diànhuà.', 'D’accord, tu peux aussi m’appeler.', True, 'end'),
     o('好的，我发消息你。', 'Hǎo de, wǒ fā xiāoxi nǐ.', '(phrase mal construite)', fix='给 + la personne se met AVANT le verbe : « 我给你发消息 ».')]),
  'end': node('好，晚上见！', 'Hǎo, wǎnshang jiàn!', 'D’accord, à ce soir !', end=True)})],
 bonus=[{'h': '点赞', 'p': 'diǎn zàn', 'fr': 'Mettre un « j’aime »', 'note': 'Sur WeChat, quand une collègue publie une photo, tu peux 点赞 (cliquer sur le pouce).'}]))

# ---------------- écriture ----------------
HSK1 = '''爱 八 爸爸 杯子 北京 本 不 不客气 菜 茶 吃 出租车 打电话 大 的 点 电脑 电视 电影 东西 都 读 对不起 多 多少 儿子 二 饭店 飞机 分钟 高兴 个 工作 狗 汉语 好 号 喝 和 很 后面 回 会 几 家 叫 今天 九 开 看 看见 块 来 老师 了 冷 里 六 吗 妈妈 买 猫 没关系 没有 米饭 名字 明天 哪 哪儿 那 呢 能 你 年 女儿 朋友 漂亮 苹果 七 前面 钱 请 去 热 人 认识 三 商店 上 上午 少 谁 什么 十 时候 是 书 水 水果 睡觉 说 四 岁 他 她 太 天气 听 同学 喂 我 我们 五 喜欢 下 下午 下雨 先生 现在 想 小 小姐 些 写 谢谢 星期 学生 学习 学校 一 一点儿 衣服 医生 医院 椅子 有 月 在 再见 怎么 怎么样 这 中国 中午 住 桌子 字 昨天 坐 做'''.split()

# Mots nouveaux du HSK 2 (ancien format, 150 mots ; 虽然…但是 et 因为…所以 comptés en deux).
HSK2 = '''吧 白 百 帮助 报纸 比 别 宾馆 长 唱歌 出 穿 船 次 从 错 打篮球 大家 到 得 等 弟弟 第一 懂 对 房间 非常 服务员 高 告诉 哥哥 给 公共汽车 公斤 公司 贵 过 还 孩子 好吃 黑 红 欢迎 回答 机场 鸡蛋 件 教室 姐姐 介绍 进 近 就 觉得 咖啡 开始 考试 可能 可以 课 快 快乐 累 离 两 零 路 旅游 卖 慢 忙 每 妹妹 门 面条 男 您 牛奶 女 旁边 跑步 便宜 票 妻子 起床 千 铅笔 晴 去年 让 日 上班 身体 生病 生日 时间 事情 手表 手机 说话 送 虽然 但是 它 踢足球 题 跳舞 外 完 玩 晚上 往 为什么 问 问题 西瓜 希望 洗 小时 笑 新 姓 休息 雪 颜色 眼睛 羊肉 药 要 也 一下 一起 已经 意思 因为 所以 阴 游泳 右边 鱼 远 运动 再 早上 丈夫 找 着 真 正在 知道 准备 走 最 左边 号 元'''.split()
# Déjà enseignés ailleurs : dans le contenu de base de index.html, ou dans un mot plus long (男人, 女人, 生日).
HSK2_AILLEURS = ('公司', '机场', '休息', '上班', '男', '女', '日')

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
    print('Mots HSK 2 non couverts :', [w for w in HSK2 if w not in covered and w not in HSK2_AILLEURS])
