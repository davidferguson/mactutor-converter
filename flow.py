import lektor.metaformat

def to_flow_block(block_name, array):
    output = []
    for item in array:
        items = list(item.items())
        output.append('#### %s ####\n' % block_name)
        lektordata = list(lektor.metaformat.serialize(items))
        output += lektordata
    return ''.join(output)
