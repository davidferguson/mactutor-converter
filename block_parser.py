import regex as re

total = 0
errors = {}
count = {}

def is_close_block_tag(s, pos):
    return is_open_block_tag(s, pos, close=True)

def is_open_block_tag(s, pos, close=False):
    tags = ['q','Q','ol','h1','h2','h3','h4','h5','h6','k','ind','cp','cpb']
    for tag in tags:
        if close:
            tag = '</%s>' % tag
        else:
            tag = '<%s>' % tag
        if pos+len(tag) >= len(s):
            continue
        match = s[pos:pos+len(tag)] == tag
        if match:
            return pos+len(tag)
    if close or pos+4 >= len(s):
        return False
    # special case for ol
    tag = '<ol'
    if s[pos:pos+3] == tag:
        pos += 2
        while s[pos] != '>':
            pos += 1
            tag += s[pos]
        return pos + 1
    else:
        return False

def get_tag(tag):
    pattern = re.compile(r'</?(?P<tag>q|Q|ol|h\d|k|ind|cp|cpb).*?>')
    match = pattern.search(tag)
    assert match
    return match.group('tag').lower()


def fix_nesting(current_block, new_tag, current_tag, blocks, newpos, ignore_tags):
    old_tag = current_tag[-1]
    if old_tag == 'ol':
        # make sure it's not a nested list
        assert new_tag != 'old'
        # tricky. for now just ignore inner tag
        ignore_tags.append(new_tag)
        return newpos
    else:
        # everything else, just come out the old block, do the new block,
        # and then go back inside the old block
        finish_block(current_block, current_tag, blocks)
        current_block = ''
        current_tag.append(new_tag)
        return newpos


def finish_block(current_block, current_tag, blocks):
    block = current_block.strip()
    # no content?
    if block == '':
        return
    # paragraph block?
    if len(current_tag) == 0:
        block = '<p>%s</p>' % block
        blocks.append(block)
        return
    # not a paragraph block?
    block = '<%s>%s</%s>' % (current_tag[-1], block, current_tag[-1])
    blocks.append(block)
    return


def process_blocks(s, name):
    blocks = []
    current_tag = []
    ignore_tags = []
    current_block = ''
    pos = 0

    while pos < len(s):
        newpos = is_open_block_tag(s, pos)
        if newpos:
            tag = get_tag(s[pos:newpos])
            if len(current_tag) != 0:
                pos = fix_nesting(current_block, tag, current_tag, blocks, newpos, ignore_tags)
            else:
                finish_block(current_block, current_tag, blocks)
                current_block = ''
                current_tag.append(tag)
                pos = newpos
            continue

        newpos = is_close_block_tag(s, pos)
        if newpos:
            tag = get_tag(s[pos:newpos])
            if len(current_tag) == 0 or tag != current_tag[-1]:
                # but can we handle it?
                if len(ignore_tags) != 0 and tag == ignore_tags[-1]:
                    # yes we can, just ignore this closing tag
                    pass
                else:
                    print('TAG MISMATCH')
                    print('expecting %s but got %s' % (current_tag[-1], tag))
                    assert False
            else:
                finish_block(current_block, current_tag, blocks)
                current_block = ''
                current_tag.pop()
                pos = newpos
                continue

        if pos+1 < len(s) and s[pos] == '\n' and s[pos+1] == '\n':
            if len(current_tag) > 0 and current_tag[-1] == 'ol':
                # dont do this for lists
                pass
            else:
                # stop and start the current block
                finish_block(current_block, current_tag, blocks)
                current_block = ''

        if pos+1 >= len(s) and current_tag == None:
            # finish this block if it's a paragraph
            finish_block(current_block, current_tag, blocks)

        # add the current character to the current block
        if pos < len(s):
            current_block += s[pos]
            pos += 1

    html = '\n\n'.join(blocks)
    return html
