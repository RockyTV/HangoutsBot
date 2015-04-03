import errno
from glob import glob
import subprocess
from .fliptextdict import fliptextdict
from .youtube_banlist import youtube_banlist

@DispatcherSingleton.register
def me(bot, event, *args):
    pass

@DispatcherSingleton.register
def image(bot, event, *args):
    yield from img(bot, event, *args)

@DispatcherSingleton.register_hidden
def load_ezhiks(bot, event, *args):
    file_exception = False
    # load ezhiks.json
    try:
        imageids_filename = 'ezhiks.json'
        imageids = json.loads(open(imageids_filename, encoding='utf-8').read(), encoding='utf-8')
    except IOError as e:
        if e.errno == errno.ENOENT:
            imageids = {}
        else:
           print('Exception:')
           print(str(e))
           file_exception = True
    # loop through ezhiks folder
    for filename in glob(os.path.join('ezhiks', '*')):
        # if filename not in imageids, upload it and store filename,id
        filekey = os.path.split(filename)[1]
        imageID = imageids.get(filekey)
        if imageID is None:
            imageID = yield from bot._client.upload_image(filename)
            if not file_exception:
                imageids[filekey] = imageID
                with open(imageids_filename, 'w') as f:
                    json.dump(imageids, f, indent=2, sort_keys=True)
                os.remove(filename)

@DispatcherSingleton.register
def ezhik(bot, event, *args):
    file_exception = False
    try:
        imageids_filename = 'ezhiks.json'
        imageids = json.loads(open(imageids_filename, encoding='utf-8').read(), encoding='utf-8')
    except IOError as e:
        imageids = {}
        if e.errno == errno.ENOENT:
           print('Exception: ezhiks.json not found!')
        else:
           print('Exception:')
           print(str(e))
           file_exception = True
        return
    imageID = imageids.get(random.choice(list(imageids.keys())))
    if imageID is None:
        print('Exception: ezhik not found (this should never happen!)')
    else:
        bot.send_image(event.conv, imageID)

@DispatcherSingleton.register
def img(bot, event, *args):
    if len(args) > 0:
        url = args[0]
        file_exception = False
        try:
            imageids_filename = os.path.join('images', 'imageids.json')
            imageids = json.loads(open(imageids_filename, encoding='utf-8').read(), encoding='utf-8')
            imageID = imageids.get(url)
        except IOError as e:
            if e.errno == errno.ENOENT:
                imageids = {}
            else:
               print('Exception:')
               print(str(e))
               file_exception = True
            imageID = None;
        if imageID is None:
            filename = UtilBot.download_image(url, 'images')
            imageID = yield from bot._client.upload_image(filename)
            if not file_exception:
                imageids[url] = imageID
                with open(imageids_filename, 'w') as f:
                    json.dump(imageids, f, indent=2, sort_keys=True)
                os.remove(filename)
        bot.send_image(event.conv, imageID)

@DispatcherSingleton.register
def log(bot, event, *args):
    msg = ' '.join(args)
    log = open('log.txt', 'a+')
    log.writelines(msg + "\n")
    for c in msg: log.writelines(hex(ord(c)) + " ")
    log.writelines("\n")
    log.close()

@DispatcherSingleton.register
def rate(bot, event, *args):
    ratings = dict(
                   agree      ="\u2714"
                  ,disagree   ="\u274c"
                  ,funny      ="\U0001f604"
                  ,winner     ="\U0001f31f"
                  ,zing       ="\u26a1"
                  ,informative="\u2139"
                  ,friendly   ="\u2764"
                  ,useful     ="\U0001f527"
                  ,optimistic ="\U0001f308"
                  ,artistic   ="\U0001f3a8"
                  ,late       ="\u23f0"
                  ,dumb       ="\U0001f4e6"
                  ,box        ="\U0001f4e6"
                  )

    try:
        bot.send_message(event.conv, ratings[args[0]])
    except KeyError:
        bot.send_message(event.conv, "That's not a valid rating. You are \U0001f4e6 x 1")

@DispatcherSingleton.register
def navyseals(bot, event, *args):
     if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*Navy Seals*
Usage: /navyseals
Purpose: Shits fury all over you.
""")
        bot.send_message_segments(event.conv, segments)
     else:
        bot.send_message(event.conv, "What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.")

@DispatcherSingleton.register
def yt(bot, event, *args):
    youtube(bot, event, *args)
    
@DispatcherSingleton.register
def YouTube(bot, event, *args):
    youtube(bot, event, *args)
    
@DispatcherSingleton.register
def xfiles(bot, event, *args):
    if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*xfiles*
Usage: /xfiles
Purpose: but what if bot is not kill
""")
        bot.send_message_segments(event.conv, segments)
    else:
        args = ['xfiles','theme']
        youtube(bot, event, *args)
    

@DispatcherSingleton.register
def youtube(bot, event, *args):
    Segment = hangups.ChatMessageSegment
    if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*YouTube*
Usage: /youtube <optional: search parameter>
Purpose: Get the first result from YouTube\'s search using search parameter.
""")
        bot.send_message_segments(event.conv, segments)
    else:
        search_terms = " ".join(args)
        if search_terms == "" or search_terms == " ":
            search_terms = "Fabulous Secret Powers"
        query = parse.urlencode({'search_query': search_terms, 'filters': 'video'})
        results_url = 'https://www.youtube.com/results?%s' \
              % query
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
        req = request.Request(results_url, None, headers)
        resp = request.urlopen(req)
        soup = BeautifulSoup(resp)
        item_id = soup.find_all("div", class_="yt-lockup")[0]['data-context-item-id']
        query = parse.urlencode({'v': item_id})
        item_url = 'https://www.youtube.com/watch?%s' \
              % query
        item_title = soup.find_all("a", class_="yt-uix-tile-link")[0]['title']

        if item_id in youtube_banlist:
            bot.send_message(event.conv, 'Sorry, that video is banned.')
        else:
            bot.send_message_segments(event.conv, [hangups.ChatMessageSegment('Result:', is_bold=True),
                                                   hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
                                                   hangups.ChatMessageSegment(item_title, hangups.SegmentType.LINK,
                                                                              link_target=item_url)])

@DispatcherSingleton.register
def linktest(bot, event, *args):
        link_url = 'http://facepunch.com'
        link_title = 'Facepunch'
        bot.send_message_segments(event.conv,
                                  [hangups.ChatMessageSegment(link_title,
                                                              hangups.SegmentType.LINK,
                                                              link_target=link_url),
                                   hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK),
                                   hangups.ChatMessageSegment(link_url,
                                                              hangups.SegmentType.LINK,
                                                              link_target=link_url)])

@DispatcherSingleton.register
def roulette(bot, event, *args):
    #static variables
    if not hasattr(roulette, "_rouletteChamber"):
        roulette._rouletteChamber = random.randrange(0, 6)
    if not hasattr(roulette, "_rouletteBullet"):
        roulette._rouletteBullet = random.randrange(0, 6)

    if len(args) > 0 and args[0] == 'spin':
        roulette._rouletteBullet = random.randrange(0, 6)
        bot.send_message(event.conv, '*SPIN* Are you feeling lucky?')
        return
    if roulette._rouletteChamber == roulette._rouletteBullet:
        roulette._rouletteBullet = random.randrange(0, 6)
        roulette._rouletteChamber = random.randrange(0, 6)
        bot.send_message(event.conv, '*BANG*')
    else:
        bot.send_message(event.conv, '*click*')
        roulette._rouletteChamber += 1
        roulette._rouletteChamber %= 6

#TODO: move this to UtilBot or find a native replacement
def choice(iterable):
    if isinstance(iterable, (list, tuple)):
        return random.choice(iterable)
    else:
        n = 1
        m = new.module('') # Guaranteed unique value.
        ret = m
        for x in iterable:
            if random.random() < 1/n:
                ret = x
            n += 1
        if ret is m:
            raise IndexError
        return ret

def _checkTheBall(questionLength):
    if not hasattr(_checkTheBall, "_responses"):
        _checkTheBall._responses = {'positive': ['It is possible.', 'Yes!', 'Of course.',
                           'Naturally.', 'Obviously.', 'It shall be.',
                           'The outlook is good.', 'It is so.',
                           'One would be wise to think so.',
                           'The answer is certainly yes.'],
              'negative': ['In your dreams.', 'I doubt it very much.',
                           'No chance.', 'The outlook is poor.',
                           'Unlikely.', 'About as likely as pigs flying.',
                           'You\'re kidding, right?', 'NO!', 'NO.', 'No.',
                           'The answer is a resounding no.', ],
              'unknown' : ['Maybe...', 'No clue.', '_I_ don\'t know.',
                           'The outlook is hazy, please ask again later.',
                           'What are you asking me for?', 'Come again?',
                           'You know the answer better than I.',
                           'The answer is def-- oooh! shiny thing!'],
             } 
    if questionLength % 3 == 0:
        category = 'positive'
    elif questionLength % 3 == 1:
        category = 'negative'
    else:
        category = 'unknown'
    return choice(_checkTheBall._responses[category])

@DispatcherSingleton.register
def eightball(bot, event, *args):
    if len(args) > 0:
        bot.send_message(event.conv, _checkTheBall(len(' '.join(args))))
    else:
        bot.send_message(event.conv, _checkTheBall(random.randint(0, 2)))

@DispatcherSingleton.register
def source(bot, event, *args):
    if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*Source*
Usage: /source
Purpose: Links to the GitHub
""")
        bot.send_message_segments(event.conv, segments)
    else:
        url = 'https://github.com/ShaunOfTheLive/HangoutsBot'
        segments = [hangups.ChatMessageSegment(url,
                                               hangups.SegmentType.LINK,
                                               link_target=url)]
        bot.send_message_segments(event.conv, segments)
        
@DispatcherSingleton.register
def fliptext(bot, event, *args):
    if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*Flip Text*
Usage: /fliptext <text>
Purpose: Flips your message 180 degrees
""")
        bot.send_message_segments(event.conv, segments)
    else:
        args = ' '.join(args)
        output = ''.join([fliptextdict.get(letter, letter) for letter in args])
        output = output[::-1]
        bot.send_message(event.conv, output)
        
@DispatcherSingleton.register
def latex(bot, event, *args):
    if ''.join(args) == '?':
        segments = UtilBot.text_to_segments("""\
*LaTeX*
Usage: /latex <LaTeX code>
Purpose: Renders LaTeX code to an image and sends it
""")
        bot.send_message_segments(event.conv, segments)
    else:
        cmd = "texvc /tmp images '" + \
              ' '.join(args).replace("'", "'\\''") + \
              "' utf-8 'rgb 1.0 1.0 1.0'"
        print('args: ')
        print(cmd)
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode(encoding='UTF-8')
        print(output)
        filename = output[1:33] + '.png'
        filename = os.path.join('images', filename)
        imageID = yield from bot._client.upload_image(filename)
        bot.send_image(event.conv, imageID)

@DispatcherSingleton.register
def greentext(bot, event, *args):
    """
    *Greentext*
    Usage: /greentext <text>
    Purpose: makes your text green and adds an epic maymay arrow
    """
    filename = 'greentext.png'
    message = ' '.join(args)
    if message[0] == '>':
        message = message[1:]
    message = message.replace('>', '\n>')
    message = '>' + message
    print(message)
    cmd = ['convert',
           '-size',
           '164x',
           '-font',
           '/usr/share/fonts/truetype/windows/arial.ttf',
           '-pointsize',
           '13',
           '-fill',
           '#789922',
           '-background',
           '#ffffee',
           'caption:%s' % message,
           filename]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = output.decode(encoding='UTF-8')
        if output != '':
            bot.send_message(event.conv, output)
        imageID = yield from bot._client.upload_image(filename)
        bot.send_image(event.conv, imageID)
        os.remove(filename)
    except subprocess.CalledProcessError as e:
        output = e.output.decode(encoding='UTF-8')
        if output != '':
            bot.send_message(event.conv, output)

@DispatcherSingleton.register
def colour(bot, event, *args):
    yield from color(bot, event, *args)
 
@DispatcherSingleton.register
def color(bot, event, *args):
    filename = 'color.png'
    cmd = ['convert',
           '-size',
           '500x500',
           'xc:%s' % ' '.join(args),
           filename]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = output.decode(encoding='UTF-8')
        if output != '':
            bot.send_message(event.conv, output)
        imageID = yield from bot._client.upload_image(filename)
        bot.send_image(event.conv, imageID)
        os.remove(filename)
    except subprocess.CalledProcessError as e:
        output = e.output.decode(encoding='UTF-8')
        if output != '':
            bot.send_message(event.conv, output)

from pyvirtualdisplay import Display
from selenium import webdriver

@DispatcherSingleton.register
def html(bot, event, *args):
    display = Display(visible=0, size=(1280, 1024))
    display.start()

    html = '<meta charset="utf-8" />' + ' '.join(args)

    with open('/var/www/tmp.html', 'w') as f:
        f.write(html)

    browser = webdriver.Firefox()
    browser.get('http://shaunofthelive.com/tmp.html')
    filename = 'screenie.png'

    ret = browser.save_screenshot(filename)
    print(str(ret))
    browser.quit()

    display.stop()   

    imageID = yield from bot._client.upload_image(filename)
    bot.send_image(event.conv, imageID)
    os.remove(filename)
