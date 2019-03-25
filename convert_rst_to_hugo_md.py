# -*- coding: utf-8 -*-

import logging
import os
import re
from collections import namedtuple

logging.basicConfig(filename="./convert.log", level=logging.DEBUG)
Header = namedtuple('Header', ['title', 'date', 'tags', 'status', 'category'])
fname_re = re.compile(r'\.rst$')


class ErrorBlog(Exception):
    def __init__(self, fname, lines):
        super(ErrorBlog, self).__init__()
        self.fname = fname
        self.lines = lines

    def __str__(self):
        return "file: {} foramt error\n{}\n".format(self.fname,
                                                    "\n".join(self.lines))


def get_header_from_rst(name, lines):
    if set(lines[1].strip()) != set('='):
        raise ErrorBlog(name, lines)

    result = dict()
    result['title'] = lines[0].strip()

    for line in lines:
        if line.lower().startswith(':date:'):
            result['date'] = line[7:].strip()
        elif line.lower().startswith(':tags:'):
            result['tags'] = [i.strip() for i in line[7:].strip().split(',')]
        elif line.lower().startswith(':status:'):
            result['status'] = line[9:].strip()
        elif line.lower().startswith(':category:'):
            result['category'] = [i.strip()
                                  for i in line[11:].strip().split(',')]

    return result


def get_new_header(header):
    result = ['---']
    result.append('title: %s' % header['title'])
    result.append('author: hackrole')
    result.append('email: hack.role@gmail.com')
    if 'date' in header:
        result.append('date: %s' % header['date'])
    if 'status' in header:
        result.append('status: %s' % header['status'])
    else:
        result.append('status: draft')
    if 'tags' in header:
        tags = ','.join(['"' + tag + '"' for tag in header['tags']])
        result.append('tags: [%s]' % tags)
    if 'category' in header:
        category = ','.join(['"' + cate + '"' for cate in header['category']])
        result.append('category: [%s]' % category)

    result.append('---')
    result.append('')
    result.append('')

    return [ln + "\n" for ln in result]


def replace_file(fname, new_headers, num):
    global fname_re
    with open(fname, 'r') as f:
        lines = f.readlines()
        new_lines = new_headers + lines[num:]

    new_fname = fname_re.sub('.md', fname)
    with open(new_fname, 'w') as f:
        f.writelines(new_lines)


def get_all_rst(dirname='./content/post'):
    fnames = [os.path.join(dirname, name)
              for name in os.listdir(dirname)
              if name.endswith('.rst')]
    return fnames


def read_lines(fname):
    with open(fname) as f:
        result = [f.readline().strip() for i in range(2)]
        hd = False
        num = 1
        for ln in f.xreadlines():
            num += 1
            if ln.strip() != '':
                result.append(ln.strip())
            if not ln.startswith(':') and hd is True:
                break
            elif ln.startswith(':') and hd is False:
                hd = True
        return result, num


def main():
    fnames = get_all_rst()

    count = 0
    for fname in fnames:
        count += 1
        lines, num = read_lines(fname)
        try:
            header = get_header_from_rst(fname, lines)
            new_header = get_new_header(header)
            replace_file(fname, new_header, num)
            logging.info("filename:\t%s\tfinish", fname)
        except ErrorBlog as e:
            print e
            continue
    print count


if __name__ == "__main__":
    main()
