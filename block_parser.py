import re

total = 0
errors = {}
count = {}

def is_open_superblock_tag(s, pos):
    return is_open_block_tag(s, pos, close=False, superblock=True)
def is_close_superblock_tag(s, pos):
    return is_open_block_tag(s, pos, close=True, superblock=True)

def is_close_block_tag(s, pos):
    return is_open_block_tag(s, pos, close=True)

def is_open_block_tag(s, pos, close=False, superblock=False):
    if s[pos] != '<':
        return False
    tags = ['q','Q','ol','h1','h2','h3','h4','h5','h6','k','ind','pre']
    if superblock:
        tags = ['cp', 'cpb']
    for tag in tags:
        if close:
            tag = '</%s>' % tag
        else:
            tag = '<%s>' % tag
        if pos+len(tag) > len(s):
            continue
        match = s[pos:pos+len(tag)] == tag
        if match:
            return pos+len(tag)
    if close or pos+4 >= len(s):
        return False
    if superblock:
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
    pattern = re.compile(r'</?(?P<tag>q|Q|ol|h\d|k|ind|pre|cpb|cp).*?>')
    match = pattern.search(tag)
    assert match
    return match.group('tag').lower()


def fix_nesting(current_block, new_tag, current_tag, blocks, newpos, ignore_tags):
    old_tag = current_tag[-1]
    if old_tag == 'ol':
        # make sure it's not a nested list
        assert new_tag != 'ol'
        # tricky. for now just ignore inner tag
        ignore_tags.append(new_tag)
        return (newpos, current_block)
    else:
        # everything else, just come out the old block, do the new block,
        # and then go back inside the old block
        finish_block(current_block, current_tag, blocks)
        current_block = ''
        current_tag.append(new_tag)
        return (newpos, current_block)


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
    in_pre = False
    current_block = ''
    current_supertag = ''
    pos = 0

    while pos < len(s):
        #if pos+5 <= len(s) and s[pos:pos+5] == '<pre>':
        #    in_pre = True
        #    pos += 5
        #    continue
        #if pos+6 <= len(s) and s[pos:pos+6] == '</pre>':
        #    in_pre = False
        #    pos += 6
        #    continue

        newpos = is_open_superblock_tag(s, pos)
        if newpos:
            supertag = get_tag(s[pos:newpos])
            if len(current_supertag) != 0:
                print('NEW SUPERTAG WHEN ALREADY IN ONE')
                assert False
            if len(current_tag) != 0:
                print('STILL IN BLOCK WHILE OPENING SUPERTAG')
                print('STILL IN %s' % current_tag)
                print('TRYING TO OPEN %s' % supertag)
                assert False
            # finish the implicit paragraph
            finish_block(current_block, current_tag, blocks)
            blocks.append('<%s>' % supertag)
            current_block = ''
            current_supertag = supertag
            pos = newpos
            continue

        newpos = is_close_superblock_tag(s, pos)
        if newpos:
            supertag = get_tag(s[pos:newpos])
            if len(current_supertag) == 0 or supertag != current_supertag:
                print('CLOSING SUPERTAG DOES NOT MATCH OPENING ONE')
                assert False
            finish_block(current_block, current_tag, blocks)
            blocks.append('</%s>' % supertag)
            current_block = ''
            current_supertag = ''
            pos = newpos
            continue

        newpos = is_open_block_tag(s, pos)
        if newpos:
            tag = get_tag(s[pos:newpos])
            if len(current_tag) != 0:
                pos, current_block = fix_nesting(current_block, tag, current_tag, blocks, newpos, ignore_tags)
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
                    ignore_tags.pop()
                    pos = newpos
                else:
                    print('TAG MISMATCH')
                    print(tag)
                    print('expecting %s but got %s' % (current_tag[-1], tag))
                    print('in', name)
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
            elif len(current_tag) > 0 and current_tag[-1] == 'q':
                # don't do this if we're in a <Q>
                pass
            elif len(current_tag) > 0 and current_tag[-1] == 'pre':
                # don't do this if we're in a <pre>
                pass
            else:
                # stop and start the current block
                finish_block(current_block, current_tag, blocks)
                current_block = ''

        # add the current character to the current block
        if pos < len(s):
            current_block += s[pos]
            pos += 1

    if current_block.strip() != '':
        finish_block(current_block, current_tag, blocks)

    html = '\n\n'.join(blocks)
    return [html]
    #print(blocks)
    #assert False
    #return blocks
