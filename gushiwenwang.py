import re
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions


options = EdgeOptions()
options.use_chromium = True
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 浏览器的位置
driver = Edge(options=options, executable_path=r"D:\edgeDriver_win64\msedgedriver.exe")  # 相应的浏览器的驱动位置​


def getText(url):
    try:
        driver.get(url)
        poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    except:
        print("2爬取失败")
        return

    poetry_dict = {"诗名": "", "朝代": "", "作者": "", "原文": "", "翻译": "", "注释": "", "鉴赏": "", "新解": "", "创作背景": ""}
    # 找标题
    title = poetry_soup.select("#sonsyuanwen > div.cont > h1")[0].text
    print("标题：" + title)
    poetry_dict['诗名'] = title
    author = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(1)")[0].text
    print("作者：" + author)
    poetry_dict['作者'] = author
    dynasty = poetry_soup.select("#sonsyuanwen > div.cont > p > a:nth-child(2)")[0].text[1:-1]
    print("朝代：" + dynasty)
    poetry_dict['朝代'] = dynasty
    # 原文
    # raw_content = poetry_soup.select("#sonsyuanwen > div.cont > div.contson")[0].text.strip()
    temp_content1 = poetry_soup.select("#sonsyuanwen > div.cont > div.contson")[0]
    temp_content2 = str(temp_content1).replace("<br/>", "|")[50:-11].strip()
    # 把括号去掉
    no_bracket_content = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", temp_content2)
    content = no_bracket_content + "|"
    print("原文：" + content)
    # 译文
    input = driver.find_element_by_xpath('//*[@alt="译文"]')
    input.click()
    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    raw_yiwen = poetry_soup.select("#sonsyuanwen > div.cont > div.contson > p > span")
    yiwen = ""
    for each in raw_yiwen:
        yiwen += each.text + "|"
    print("译文：" + yiwen)
    # 注释
    input = driver.find_element_by_xpath('//*[@alt="注释"]')
    input.click()
    # 取消掉
    input = driver.find_element_by_xpath('//*[@alt="译文2"]')
    input.click()
    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    raw_zhushi = poetry_soup.select("#sonsyuanwen > div.cont > div.contson > p > span")
    zhushi = ""
    for each in raw_zhushi:
        zhushi += each.text + "|"
    print("注释：" + zhushi)
    # 点开“展开阅读全文”
    buttons = driver.find_elements_by_link_text("展开阅读全文 ∨")
    for button in buttons:
        button.click()
    poetry_soup = BeautifulSoup(driver.page_source, 'lxml')
    hide_list = poetry_soup.select("div.main3 > div.left > div.sons > div.contyishang")

    all_hide_tags = []
    for each in hide_list:
        if (each.span.text not in all_hide_tags):
            if (each.span.text != '译文及注释'):
                all_hide_tags.append(each.span.text)
    print(all_hide_tags)

    for each in all_hide_tags:
        output = ""
        for e in hide_list:
            if (e.span.text == each):
                each_pList = e.select('p')
                for p in each_pList:
                    output += p.text.strip()
        print(each + ": " + output)

# 这里放古诗对应的网页就行
getText("https://so.gushiwen.cn/shiwenv_d963cf7df117.aspx")

# 结果展示
# 标题：夏日过郑七山斋
# 作者：杜审言
# 朝代：唐代
# 原文：共有樽中好，言寻谷口来。|薜萝山径入，荷芰水亭开。|日气含残雨，云阴送晚雷。|洛阳钟鼓至，车马系迟回。|
# 译文：我们都有喜爱酒的嗜好，我就找到你的山中别墅来。|薜荔女萝伸向山上的的jì小径，荷花菱花开在水亭的周围。|太阳尤散发着的热气含着残雨，阴云传送看黄昏的雷声。|洛阳城里报暮的钟、鼓之声清晰地传来，但车马仍然拴着，迟迟没有起程。|
# 注释：(zūn)|(hào)|樽中好：喜爱杯中之物。樽：古代的盛酒器具。言：句首助词，无义，凑足音节。谷口：汉代县名，在今陕西礼泉县东。|(bì)|(jì)|薜：薜荔，木本植物，又名末莲、木馒头，茎蔓生，花小，果实形似莲房。萝：女萝：地衣类植物，即松萝，常寄生松树上，丝状，蔓延下垂。晋后多以薜萝指隐士的服装。此用以赞美郑七归隐之志。芰：菱角，两角者为菱，四角者为芰。此用其意，赞赏友人。|日气：日光散发的热气。|(xì)|洛阳：唐代东都。钟鼓：古代有黄昏时击鼓、撞钟以报时的风尚。此指时近傍晚。系：拴缚。迟回：迟疑，徘徊。|
# ['创作背景', '赏析']
# 创作背景: 此诗约作于高宗上元年间（674～676），杜审言任洛阳丞时。郑七的山斋在洛阳附近。诗人与郑七既是文友，又是酒友，故于夏日造访，过山径，开水亭，在雨后丽日、云阴晚凉的清爽气氛中，文酒相乐，流连忘返。因此诗人用明朗爽快的笔调描写了这一过程。
# 赏析: “共有樽中好，言寻谷口来。”首联是介绍过郑斋的缘起。诗人说：我和郑七都有饮酒的爱好，所以来找他。隐居与饮酒几乎是不可分离的，它是隐士们高雅、旷达情怀的表现。可见，诗中的言外之意，是说郑七有隐者的高洁胸怀，诗人对他十分倾慕，引为同调，因此才去拜访他。“言寻谷口来”一句，用典故进一步说明了这一点。用典十分贴切，一个“寻”字，也透露了山斋的幽深。两句诗看似平常，却有深刻的义蕴，不仅曲折地交待了郑七的身份和思想情操，也婉转地点出了过山斋的原因和二人深厚的友情。接着诗人以极大的兴趣，用工细的笔墨，在中间两联描绘山斋内外的景色，展现出一幅优美的山居夏图。“薜萝山径入，荷芰水“共有樽中好，言寻谷口来。”首联是介绍过郑斋的缘起。诗人说：我和郑七都有饮酒的爱好，所以来找他。隐居与饮酒几乎是不可分离的，它是隐士们高雅、旷达情怀的表现。可见，诗中的言外之意，是说郑七有隐者的高洁胸怀，诗人对他十分倾慕，引为同调，因此才去拜访他。“言寻谷口来”一句，用典故进一步说明了这一点。用典十分贴切，一个“寻”字，也透露了山斋的幽深。两句诗看似平常，却有深刻的义蕴，不仅曲折地交待了郑七的身份和思想情操，也婉转地点出了过山斋的原因和二人深厚的友情。接着诗人以极大的兴趣，用工细的笔墨，在中间两联描绘山斋内外的景色，展现出一幅优美的山居夏图。“薜萝山径入，荷芰水亭开。”上一句说，在通往郑七山斋的曲折的山路上，长满了茂盛的薜荔和女萝，隐隐传达出山斋的幽深和清静。接着是进入山斋后的景象：在水亭周围的水池中，一望无际的荷、菱开放出纯洁清丽的花朵，在微风中散发着清香。“山径”是崎岖的，而水池却是开阔的，从狭窄山路中穿行而至来到山斋后，诗人顿觉豁然开朗，诗中“入”字和“开”字，不仅实指了诗人的行动，也透露出心情的变化。接着，在“日气含残雨，云阴送晚雷”一联中，诗人又把笔触从平面的描写转向立体的空间：在那荷、菱盛开的水池上，雨后初晴，空中铺下明朗的阳光，照在残留的雨水上，蒸气冉冉升腾；到傍晚，天气渐渐转阴了，天边又传来隐隐的雷声。其中“日”、“雨”、“阴”几个字，暗示着天气变化很快。诗人来之前，刚下过雨（“含残雨”），而到达时天气才放晴，傍晚又转阴，并且传来隆隆的雷声，又要下雨了。这正是深山中特有的天气，诗人用天气变化之快，烘托山斋的既幽且深，既是实写，也有助于诗歌意境的表现。同时在“日”、“晚”二字中，也包含着时间的推移，暗示了诗人在山斋中逗留的时间。通过这一联的描写，充分渲染了山斋的幽静景色，地上风物和空中景象融为一体，在静谧中包含变化，在幽深中充满生机。诗人形象的描写，使山斋风光充满着感人的魅力，令人心驰神往。中间两联，似乎全是写景。其实，主人的酒盛情款待，席间杯觥交错的欢乐气氛，全都隐藏在字里行间中。“洛阳钟鼓至，车马系迟回”，与天边隆隆的雷声相应和，洛阳城里报暮的钟、鼓之声也清晰地传来，诗人该回程了，但车马仍然拴着，迟迟没有起程。诗到这里戛然而止，却留下了耐人寻味的余韵，在迟迟未回中，既包含着诗人对山斋风光的倾心爱慕、流连忘返，同时也表现出主人的深情厚谊。在这悠远的余韵中，诗歌产生了动人心弦的艺术力量。这首《夏日过郑七山斋》，是杜审言五律中的成功之作。不仅在文字、结构、意境等方面取得了成功，在诗歌的声律上，对仗工稳，音韵协调，整体匀称，也表现出纯熟的技巧。▲

