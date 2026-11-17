"""Pinyin fiable pour les phrases de Zìzì.
- découpage en mots par plus longue correspondance sur notre vocabulaire (pas de mots collés au hasard)
- tons neutres des mots courants (名字 míngzi, 谢谢 xièxie…)
- changements de ton de 一 et 不 selon le ton suivant
- 儿 rétroflexe (哪儿 nǎr), noms propres en majuscule, corrections de lecture au cas par cas
"""
import re
from pypinyin import pinyin, Style

HAN = re.compile(r'[㐀-鿿]')
PUNCT = {'，': ',', '。': '.', '？': '?', '！': '!', '：': ':', '、': ','}
# mots dont la ou les dernières syllabes sont neutres (pinyin complet, sans espace)
FIXED = {
 '高兴': 'gāoxìng', '兴趣': 'xìngqù', '国家': 'guójiā', '认真': 'rènzhēn', '知识': 'zhīshi', '有名': 'yǒumíng', '医生': 'yīshēng', '医师': 'yīshī', '有问题': 'yǒu wèntí', '每双鞋': 'měi shuāng xié', '查一下': 'chá yíxià', '好了': 'hǎo le', '做完了': 'zuòwán le', '坏了': 'huài le', '太贵了': 'tài guì le', '够了': 'gòu le', '小姐': 'xiǎojiě', '哪里': 'nǎlǐ', '这台': 'zhè tái', '这家': 'zhè jiā', '这件': 'zhè jiàn', '这本': 'zhè běn', '这把': 'zhè bǎ', '爸妈': 'bàmā', '男朋友': 'nánpéngyou', '好朋友': 'hǎo péngyou', '老朋友': 'lǎo péngyou', '友好': 'yǒuhǎo', '多少钱': 'duōshao qián', '一块钱': 'yí kuài qián', '买东西': 'mǎi dōngxi', '请坐': 'qǐng zuò', '再说': 'zàishuō', '去哪儿': 'qù nǎr', '星期六': 'xīngqīliù', '十分钟': 'shí fēnzhōng', '五分钟': 'wǔ fēnzhōng', '十分': 'shífēn', '三十': 'sānshí', '八十': 'bāshí', '二十三': 'èrshísān', '星期天': 'xīngqītiān', '开心': 'kāixīn', '快一点': 'kuài yìdiǎn', '慢一点': 'màn yìdiǎn', '发工资': 'fā gōngzī', '帮我': 'bāng wǒ', '看电视': 'kàn diànshì', '看电影': 'kàn diànyǐng', '一本书': 'yì běn shū', '几号': 'jǐ hào', '看医生': 'kàn yīshēng', '在哪儿呢': 'zài nǎr ne', '喂，你好': 'wèi, nǐ hǎo',
 '名字': 'míngzi', '认识': 'rènshi', '谢谢': 'xièxie', '爸爸': 'bàba', '妈妈': 'māma', '朋友': 'péngyou',
 '东西': 'dōngxi', '衣服': 'yīfu', '喜欢': 'xǐhuan', '漂亮': 'piàoliang', '时候': 'shíhou', '休息': 'xiūxi',
 '先生': 'xiānsheng', '学生': 'xuésheng', '姐姐': 'jiějie', '早上': 'zǎoshang', '晚上': 'wǎnshang',
 '关系': 'guānxi', '客气': 'kèqi', '不客气': 'bú kèqi', '商量': 'shāngliang', '明白': 'míngbai', '星星': 'xīngxing',
 '多少': 'duōshao', '月亮': 'yuèliang', '过来': 'guòlai', '过去': 'guòqu', '出去': 'chūqu', '回来': 'huílai',
 '回去': 'huíqu', '什么': 'shénme', '怎么': 'zěnme', '怎么样': 'zěnmeyàng', '这个': 'zhège', '那个': 'nàge',
 '哪个': 'nǎge', '我们': 'wǒmen', '你们': 'nǐmen', '他们': 'tāmen', '她们': 'tāmen', '儿子': 'érzi',
 '桌子': 'zhuōzi', '椅子': 'yǐzi', '杯子': 'bēizi', '箱子': 'xiāngzi', '鞋子': 'xiézi', '本子': 'běnzi',
 '影子': 'yǐngzi', '房子': 'fángzi', '孩子': 'háizi', '女儿': 'nǚ’ér', '哪儿': 'nǎr', '一点儿': 'yìdiǎnr',
 '这儿': 'zhèr', '那儿': 'nàr', '对不起': 'duìbuqǐ', '没关系': 'méi guānxi', '觉得': 'juéde', '猫咪': 'māomī',
 '便宜': 'piányi', '告诉': 'gàosu', '意思': 'yìsi', '知道': 'zhīdào', '事情': 'shìqing', '舒服': 'shūfu',
 '眼睛': 'yǎnjing', '耳朵': 'ěrduo', '头发': 'tóufa', '地方': 'dìfang', '工夫': 'gōngfu', '麻烦': 'máfan',
 '好的': 'hǎo de', '是的': 'shì de', '太好了': 'tài hǎo le', '慢慢来': 'mànmàn lái', '看见': 'kànjiàn',
 '听不懂': 'tīng bu dǒng', '能不能': 'néng bu néng', '一共': 'yígòng', '一起': 'yìqǐ', '一下': 'yíxià',
 '一样': 'yíyàng', '一些': 'yìxiē', '一定': 'yídìng', '一点': 'yìdiǎn', '已经': 'yǐjīng',
 '数量': 'shùliàng', '质量': 'zhìliàng', '长大': 'zhǎngdà', '组长': 'zǔzhǎng', '校长': 'xiàozhǎng',
 '还有': 'hái yǒu', '还差': 'hái chà', '只': 'zhī', '说得': 'shuō de', '中文': 'Zhōngwén', '中国': 'Zhōngguó',
 '中国人': 'Zhōngguó rén', '汉语': 'Hànyǔ', '法语': 'Fǎyǔ', '北京': 'Běijīng', '南京': 'Nánjīng', '多哥': 'Duōgē',
 '多哥人': 'Duōgē rén', '洛美': 'Luòměi', '玛丽': 'Mǎlì', '汉字': 'Hànzì', '谁': 'shéi', '是谁': 'shì shéi',
 '谁的': 'shéi de', '不是': 'bú shì', '不要': 'bú yào', '不够': 'bú gòu', '不对': 'bú duì', '不用': 'bú yòng',
 '不在': 'bú zài', '不难': 'bù nán', '一只': 'yì zhī', '这只': 'zhè zhī', '那只': 'nà zhī', '一双': 'yì shuāng', '一个': 'yí ge', '一杯': 'yì bēi',
 '一本': 'yì běn', '一斤': 'yì jīn', '一块': 'yí kuài', '一遍': 'yí biàn', '一箱': 'yì xiāng', '一月': 'yīyuè',
 '十一': 'shíyī', '没事': 'méi shì', '有事': 'yǒu shì', '好吃': 'hǎochī', '好听': 'hǎotīng', '好看': 'hǎokàn',
 '小时候': 'xiǎo shíhou', '二号线': 'èr hào xiàn', '三号线': 'sān hào xiàn', '几个': 'jǐ ge', '三个': 'sān ge',
 '四个': 'sì ge', '七个': 'qī ge', '十个': 'shí ge', '在家': 'zài jiā', '回家': 'huí jiā',
}
# autres mots à garder ensemble (pinyin donné par le dictionnaire)
WORDS = set('''女人 好了 做完了 做完 用完 一个 感谢 帮助 老师 同事 同学 学习 工作 工厂 工资 鞋厂 生产 生产线 电线 鞋底 到底 胶水 橡胶 每天 质量检查 这里 那里 家里 检查 上班 上午 加班 下班 下午 小组 老板 地板 机器 飞机 手机 电器 首先 问题 没有 白色 今天 今年 新年 大家 大米 天气 明天 昨天 昨晚 发现 现在 几点 分钟 钟头 中午 星期 日期 几号 号码 小时 等候 米饭 饭店 点菜 做菜 绿茶 水果 苹果 苹果汁 商店 恭喜 欢迎 小心 开心 想要 爱人 可爱 请问 请坐 买单 有钱 东边 西红柿 毛衣 服务员 这些 以前 前面 后面 面条 以后 住址 学校 医院 电影院 北方 去哪儿 来自 出租车 租房子 火车 起飞 开门 开车 打电话 打开 电话 电脑 说话 再见 再说 可能 开会 听说 读书 阅读 写字 写信 书店 一本书 练习 作业 做饭 做鞋 睡觉 午睡 大脑 电视 重视 电影 生气 冷水 热水 下雨 雨天 小狗 狗叫 小猫 全都 和平 客人 客户 关门 椅子 饭桌 好坏 双手 加油 资料 退休 消息 快乐 起床 用 到 每 帮 冬天 晚上 过来 过去 慢慢来 时间 司机 鞋子 七月 十月 六月 三月 四月 九点 八点 六点 十点 七点 五点 八十 九十 二十 五十 十二 二十三 中午 晚上 每个 一共 早上 已经 还有 可以 洛美'''.split())
WORDS |= set(FIXED)
TONE_OF = {}
def tone_of(s):
    for ch in s:
        for t, group in enumerate(['āēīōūǖ', 'áéíóúǘ', 'ǎěǐǒǔǚ', 'àèìòùǜ'], 1):
            if ch in group: return t
    return 0

def segment(text):
    out, i = [], 0
    maxlen = max(len(w) for w in WORDS)
    while i < len(text):
        if not HAN.search(text[i]):
            out.append(text[i]); i += 1; continue
        for L in range(min(maxlen, len(text) - i), 0, -1):
            w = text[i:i + L]
            if L == 1 or w in WORDS:
                out.append(w); i += L; break
    return out

def word_py(w, nxt_tone):
    if w in FIXED: return FIXED[w]
    syl = [x[0] for x in pinyin(w, style=Style.TONE)]
    res = []
    for k, (ch, s) in enumerate(zip(w, syl)):
        nt = tone_of(syl[k + 1]) if k + 1 < len(syl) else nxt_tone
        if ch == '一' and nt:
            s = 'yí' if nt == 4 else 'yì'
        if ch == '不' and nt:
            s = 'bú' if nt == 4 else 'bù'
        if ch == '个' and len(w) > 1: s = 'ge'
        if ch == '了': s = 'le'
        if ch == '的': s = 'de'
        if ch == '吗': s = 'ma'
        if ch == '呢': s = 'ne'
        if ch == '吧': s = 'ba'
        if k > 0 and s[:1] in 'aāáǎàeēéěèoōóǒò': s = '’' + s
        res.append(s)
    return ''.join(res)

def sentence_py(text):
    seg = segment(text)
    raw = []
    for idx, w in enumerate(seg):
        if not HAN.search(w): raw.append(('p', PUNCT.get(w, w))); continue
        # ton du premier caractère du mot suivant (pour 一 / 不 en fin de mot)
        nxt = next((x for x in seg[idx + 1:] if HAN.search(x)), None)
        nt = 0
        if nxt and seg[idx + 1:idx + 2] == [nxt]:
            nt = tone_of(word_py(nxt, 0).split(' ')[0])
        raw.append(('w', word_py(w, nt)))
    out = ''
    for kind, s in raw:
        if kind == 'p': out = out.rstrip() + s + ' '
        elif out.endswith((': ', '! ', '? ', '. ')) and out.strip(): out += s[:1].upper() + s[1:] + ' '
        else: out += s + ' '
    out = re.sub(r'\s+', ' ', out).strip()
    if out and HAN.search(text[-1]) is None:  # une vraie phrase : majuscule initiale
        out = out[0].upper() + out[1:]
    return out

if __name__ == '__main__':
    for t in ['今天天气很好。', '请给我一杯水。', '这只猫很可爱。', '你说得很好！', '我会说一点儿中文。', '你住在哪儿？',
              '我不喝茶。', '一共五块钱。', '名字', '一点儿', '我爱我的家。', '我想学中文。', '还有两箱胶水。']:
        print(t, '→', sentence_py(t))
