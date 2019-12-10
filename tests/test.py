import re
SPE = re.compile(r'\^|\&|\$|\=|\+|\-|\!|\@|\#|\%|\*|\?|\{|\}|\:')
IS_N = re.compile(r'[A-Za-z]*')

HTML_TAG_REGEX = re.compile(
    '<div[^>]*>|</div>|<math[^>]*>[^<>]*</math(s)?>|<dl[^>]*>|</dl>|<dt[^>]*>|</dt>|'
    '<dd[^>]*>|</dd>|<ul[^>]*>|</ul>|<li[^>]*>|</li>|<ol[^>]*>|</ol>|'
    '<span[^>]*>|</span>|<sup>|</sup>|<sub>|</sub>|<!--['
    '^!]*-->|<u>|</u>|<b>|</b>|<i>|</i>')
# def is_name(text):
#     if IS_N.search(text):
#         print(IS_N.match(text))
#         return str(True)
#     else:
#         print(IS_N.search(text))
#         return str(False)


if __name__ == '__main__':
    text = 'cat<\b>'
    t = HTML_TAG_REGEX.search(text)
    print(t)