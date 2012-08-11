#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will retrieve the documentation corresponding
to given PayPal API service and method.

Once retrieved the types will be extracted and their descriptions
will be converted into docstrings intended for usage in the
SDK type implementations.

The intention of this script is to remove the need to manually
write the docstrings for each PayPal type. Which spares a
significant amount of time during development.

Equally valuable is the ability to persist the output to disk.
Allowing us to easily get a diff of our implemented types and their
docstrings and the latest versions of the documentation. Thereby
easily detecting once changes have been made to the API.

"""

import sys
import urllib2
from BeautifulSoup import BeautifulSoup


EXPRESS_CHECKOUT_URLS = {
    'SetExpressCheckout': 'setexpresscheckout-api-operation-nvp',
}

ALL_URLS = {
    'ExpressCheckout': EXPRESS_CHECKOUT_URLS,
}

CHARACTER_LIMITATIONS_NEEDLE = 'Character length and limitations: '
CHARACTER_LIMITATIONS_NEEDLE_LEN = len(CHARACTER_LIMITATIONS_NEEDLE)

VERSION_REQUIREMENT_NEEDLE = 'This field is introduced in API version '
VERSION_REQUIREMENT_NEEDLE_LEN = len(VERSION_REQUIREMENT_NEEDLE)

VERSION_REQUIREMENT_NEEDLE_ALT = 'This field is available since version '
VERSION_REQUIREMENT_NEEDLE_ALT_LEN = len(VERSION_REQUIREMENT_NEEDLE_ALT)


def generate_documentation_url(service, method):
    base = 'https://www.x.com/developers/paypal/documentation-tools/api/%s'
    return base % ALL_URLS[service][method]


def get_documentation_html(url):
    f = urllib2.urlopen(url)
    documentation = f.read()
    f.close()
    return documentation


def normalize_text(parts):
    parts = filter(lambda value: value != '\n', parts)
    return ''.join(parts)


def get_type_group_name(tag):
    parts = tag.find('h4').findAll(text=True)
    return normalize_text(parts)


def parse_type_api_version(string):
    if string.startswith(VERSION_REQUIREMENT_NEEDLE):
        offset = VERSION_REQUIREMENT_NEEDLE_LEN
    elif string.startswith(VERSION_REQUIREMENT_NEEDLE_ALT):
        offset = VERSION_REQUIREMENT_NEEDLE_ALT_LEN
    else:
        return ''

    version = string[offset:]
    trailing_period_idx = version.rfind('.')
    if trailing_period_idx != -1:
        version = version[:trailing_period_idx]
    return version


def parse_type_docstring_paragraph(tag, sections, description_key):
    value = tag.findAll(text=True)
    value = normalize_text(value)

    # Add string describing value limitations to the limitations
    # list so that we can concatenate all of the limitations in one
    # section in our docstring.
    if value.startswith(CHARACTER_LIMITATIONS_NEEDLE):
        value = value[CHARACTER_LIMITATIONS_NEEDLE_LEN:]
        sections['limitations'].append(value)
        return

    version = parse_type_api_version(value)
    if version:
        sections['required_version'] = version
        return

    sections[description_key].append(value)


def parse_type_docstring_notes(tag, sections):
    notes = tag.findAll('p')
    for note in notes:
        note = normalize_text(note.findAll(text=True))
        sections['notes'].append(note)


def parse_type_docstring_choices(tag, sections):
    choices = tag('li')
    for choice in choices:
        choice = normalize_text(choice.findAll(text=True))
        sections['choices'].append(choice.strip())


def generate_docstring_lines(sentences, indentation=1, max_length=77):
    def generate_line(words, indentation):
        row = ' '.join(words)
        indentation = ' ' * indentation
        return '%s%s' % (indentation, row)

    doclines, line = [], []
    current_line_length = 0
    max_length -= indentation
    for sentence in sentences:
        words = sentence.split(' ')
        for word in words:
            word_len = len(word)
            if word_len + current_line_length >= max_length:
                doclines.append(generate_line(line, indentation))
                current_line_length = 0
                line = []

            line.append(word)
            current_line_length += word_len + 1
    doclines.append(generate_line(line, indentation))
    return doclines


def generate_docstring_description(sentences):
    return generate_docstring_lines(sentences)


def _generate_docstring_section(rows, headline=None):
    lines = []
    lines.append('')

    if headline is not None:
        lines.append(' %s:' % headline)

    i = 0
    row_count = len(rows)
    for row in rows:
        lines.extend(generate_docstring_lines([row], indentation=5))
        i += 1
        if i < row_count:
            lines.append('')
    return lines


def generate_docstring_choices(choices):
    return _generate_docstring_section(choices)


def generate_docstring_limitations(limitations):
    headline = 'Character length and limitations'
    return _generate_docstring_section(limitations, headline=headline)


def generate_docstring_notes(notes):
    return _generate_docstring_section(notes, headline='Notes')


def parse_docstring_sections(description):
    sections = {
        'head': [],  # Beginning of the description
        'limitations': [],  # Value limitations found in the description
        'choices': [],  # Choices of values which are considered valid
        'notes': [],  # Documentation which is flagged as extra noteworthy
        'required_version': '',  # When the type was introduced to the API
        'tail': [],  # End of the description
    }

    description_keys = ('head', 'tail')
    contents = filter(lambda value: value != ' ', description.contents)
    is_tail_paragraph = False
    for node in contents:
        node_name = node.name

        # Replace all code references in the documentation with
        # ``code_reference``. All references are placed within a samp
        # tag with the codeph class - like the type name itself.
        code_references = node('samp', 'codeph')
        for reference in code_references:
            reference.replaceWith('``%s``' % reference.string)

        if node_name == 'p':
            # The paragraph tag can contain either our head or tail
            # along with character limitations and required version
            # information.
            key = description_keys[is_tail_paragraph]
            parse_type_docstring_paragraph(node, sections, key)
        elif node_name == 'div':
            # Only notes are placed within the div node
            parse_type_docstring_notes(node, sections)
            is_tail_paragraph = True
        elif node_name == 'ul':
            # Only choices are listed within the ul node
            parse_type_docstring_choices(node, sections)
            is_tail_paragraph = True

    return sections


def generate_type_docstring(description):
    # Parse and retrieve all the docstring sections found
    # in given description. The parse_docstring_sections is
    # the workhorse in this case while this function merely
    # concatenates the sections into one docstring.
    sections = parse_docstring_sections(description)

    lines = generate_docstring_description(sections['head'])

    choices = sections['choices']
    if choices:
        lines.extend(generate_docstring_choices(choices))

    limitations = sections['limitations']
    if limitations:
        lines.extend(generate_docstring_limitations(limitations))

    notes = sections['notes']
    if notes:
        lines.extend(generate_docstring_notes(notes))

    required_version = sections['required_version']
    if required_version:
        lines.append('')
        lines.append(' Available since API version: %s' % required_version)

    tail = sections['tail']
    if tail:
        lines.append('')
        lines.extend(generate_docstring_description(tail))

    docstring = '#:' + '\n#:'.join(lines)
    return docstring


def scrape_type(tag):
    # Retrieve the name of the current type. We achieve this by
    # retrieving the first <samp class="codeph"> node which
    # sanitized contains the type name.
    type_name = tag.find('samp', 'codeph').findAll(text=True)
    type_name = normalize_text(type_name)

    # The type description, i.e the text from which we generate
    # the docstring, is located in the second column of the
    # current type row.
    description_column = tag('td')[1]
    docstring = generate_type_docstring(description_column)

    # Print the type name along with the generated docstring
    print '%s' % type_name
    print '#' + '~' * 78
    print docstring
    print '\n'


def scrape_type_group(tag):
    # Print group name header
    group_name = get_type_group_name(tag)
    separator = '#' + '-' * 78
    print '%s\n# %s\n%s\n' % (separator, group_name, separator)

    table = tag.find('table')
    tbody = table.find('tbody')
    rows = tbody('tr')

    # All types are contained within the group table in their
    # own seperate row, i.e tr node.
    for row in rows:
        scrape_type(row)


def scrape_type_groups(container, is_request_type):
    # Print RESPONSE or REQUEST header depending on type of groups
    separator = '#' * 79
    headline = ('RESPONSE TYPES', 'REQUEST TYPES')[is_request_type]
    print '%s\n# %s\n%s\n' % (separator, headline, separator)

    # Each type is contained within a div.nested2 node
    groups = container('div', 'nested2')
    for group in groups:
        scrape_type_group(group)


def scrape_documentation(service, method):
    url = generate_documentation_url(service, method)
    documentation = get_documentation_html(url)
    soup = BeautifulSoup(documentation)

    # Everything we need is within the .field-item node
    content = soup.find('div', 'field-item')
    # Extract response types. Once done all remaining div.nested1
    # nodes will correspond to request types only.
    response_types = content.find('div', 'nested1').extract()
    scrape_type_groups(content, is_request_type=True)
    scrape_type_groups(response_types, is_request_type=False)


def main(argc, argv):
    try:
        service, method = argv[1:]
    except ValueError:
        print 'Usage: %s <API Service> <API Method Name>' % argv[0]
        return 1

    scrape_documentation(service, method)
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
