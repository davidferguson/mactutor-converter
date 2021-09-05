import re
import sys

lines = sys.stdin.readlines()
text = ''.join(lines)

text = text.replace('<p align=justify>', '')
text = text.replace('<blockquote>', '\n<Q>')
text = text.replace('</blockquote>', '</Q>\n')
text = re.sub(r'<a href=javascript:fnote\(\d+\)>.*?</a>', '', text)
text = re.sub(r'<img src= "../../../Symbolgifs/(.*?).gif".*?>', r'<s \1>', text)

output = '''<NUMBER>

</NUMBER>

<TITLE>

</TITLE>

<CONTENT>
%s
</CONTENT>''' % text

print(output)
