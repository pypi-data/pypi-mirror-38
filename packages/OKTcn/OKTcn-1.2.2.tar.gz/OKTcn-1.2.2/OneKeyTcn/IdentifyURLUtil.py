import requests, re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
}


# 是否是京东链接
def isJDUrl(url):
    if url == '':
        return False
    pattern = re.compile('.jd.')
    pattern_search = re.findall(pattern, url)
    if len(pattern_search) == 0:
        return False
    return True


# 是否是京东联盟jdc链接
# http://union-click.jd.com/jdc?d=ftKbOO
def isJDShortUnion(url):
    if url == '':
        return False
    pattern = re.compile('http(s?)://union-click.jd.com/jdc\?d=')
    pattern_search = re.findall(pattern, url)
    if len(pattern_search) == 0:
        return False
    return True

# https://union-click.jd.com/jda?e=99_2|99_2|1_2_2|tagA&p=AyIHVCtaJQMiQwpDBUoyS0IQWhkeHAxbSkAYCllHGAdFBwtJQBkAWAtTYFpFEE8HC0BMXhEFA0pXRk5KQh5JXxxVC0QeQV1XZgVYC0kOEgZUGloUBhoFQkkfGUdRQwEMC0ZHHgVlayFtSk4dXEg5TgVQWyhvHmJCe0c3TVcZbBEGVRJHFAQOBFYKWBYJFwBeH10lAyIEVBtbFgAUD1ASayUCFjcedVolAyIHURlYFgQTDlUdUxABIgdTKwBAbBVXVhhYFAIbUgcYCxwyIjdlK2sUMhI3Cl8GSA%3D%3D&t=W1dCFFlQCxxOGA5YRE5XDVULR0VeUAxSFksdd0pQQgFHRVdcS0NLQwRAVlsYDF4HSAxAWQpeD0pHc1cWSwcZAhMGVBpaEQoQEAdfV1BBVlNCSwhQDhA%3D&a=fCg9UgoiAwwHO1BcXkQYFFlgdXpyfVFdQVwzVRBSUll%2bAQAPDSwjLw%3d%3d&refer=norefer&d=ftKbOO
def isJDLongUnioin(url):
    if url == '':
        return False
    pattern = re.compile('http(s?)://union-click.jd.com/jda\?d=')
    pattern_search = re.findall(pattern, url)
    if len(pattern_search) == 0:
        return False
    return True


# http://union-click.jd.com/jdc?d=ftKbOO  --->https://union-click.jd.com/jda?e=99_2|99_2|1_2_2|tagA&p=AyIHVCtaJQMiQwpDBUoyS0IQWhkeHAxbSkAYCllHGAdFBwtJQBkAWAtTYFpFEE8HC0BMXhEFA0pXRk5KQh5JXxxVC0QeQV1XZgVYC0kOEgZUGloUBhoFQkkfGUdRQwEMC0ZHHgVlayFtSk4dXEg5TgVQWyhvHmJCe0c3TVcZbBEGVRJHFAQOBFYKWBYJFwBeH10lAyIEVBtbFgAUD1ASayUCFjcedVolAyIHURlYFgQTDlUdUxABIgdTKwBAbBVXVhhYFAIbUgcYCxwyIjdlK2sUMhI3Cl8GSA%3D%3D&t=W1dCFFlQCxxOGA5YRE5XDVULR0VeUAxSFksdd0pQQgFHRVdcS0NLQwRAVlsYDF4HSAxAWQpeD0pHc1cWSwcZAhMGVBpaEQoQEAdfV1BBVlNCSwhQDhA%3D&a=fCg9UgoiAwwHO1BcXkQYFFlgdXpyfVFdQVwzVRBSUll%2bAQAPDSwjLw%3d%3d&refer=norefer&d=ftKbOO
# 还原jdc短链为长链接
def recoverJDC(url):
    try:
        req = requests.get(url, headers, allow_redirects=False)
        status_code = req.status_code
        print(status_code)
        if status_code == 200:
            html = req.text
            print(html)
            pattern = re.compile('(?<=var hrl=\').*?(?=\')')
            items = re.findall(pattern, html)
            print(items)
            if len(items) == 1:
                return items[0]
        return url
    except:
        return url










