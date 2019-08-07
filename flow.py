import lektor.metaformat
import re
_block_re = re.compile(r'^###(?:#+)\s*([^#]*?)\s*###(?:#+)\s*$')

def _line_is_flowheader(line):
    match = _block_re.search(line)
    return match

def to_flow_block(block_name, array):
    output = []
    for item in array:
        items = list(item.items())
        output.append('#### %s ####\n' % block_name)
        lektordata = list(lektor.metaformat.serialize(items))

        for idx, line in enumerate(lektordata):
            if _line_is_flowheader(line):
                lektordata[idx] = u'#' + line.strip() + u'#\n'

        output += lektordata

    return ''.join(output)
