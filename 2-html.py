import re

def kiss(text):

    # vars to be written to by nested functions
    kiss.classes_found = True

    def repl_span(m):
        kiss.classes_found = True
        return '<span class="' + m.group(1) + '">' + re.sub(r'(?<!\<br\ \/\>)\n', r'<br />\n', m.group(2)) + '</span>'

    def repl_list(m):
        return "</p><ul>" + re.sub(r'^\*[ \t]*(.*)$', r'<li>\1</li>', m.group(0), 0, re.MULTILINE).replace('\n','') + "</ul><p>"

    def repl_headings(m):
        head = "h" + str(len(m.group(1))) + ">"
        return "</p><" + head + m.group(2).strip() + "</" + head + "<p>"
    
    # It all began from here

    # preprocessing
    text = "<p>\n" + text + '\n</p>'

    # remove comments
    text = re.sub(r'^#[^\n]*\n', r'', text, 0);

    # links 
    text = re.sub(r'(http:\/\/[a-zA-Z0-9\.\-]+(\/[\=\w\/\_\.\-\?\&\#]*){0,1})(?<![\.\?])', r'<a href="\1">\1</a>', text)
    text = re.sub(r'([\w\.\+]+\@[a-zA-Z0-9\.\-]+(\/[\=\w\/\_\.\-\?\&\#]*){0,1})(?<![\.\?])', r'<a href="mailto: \1">\1</a>', text)
    
    # classes
    while (kiss.classes_found):
        kiss.classes_found = False
        text = re.sub(r'\[([a-z]+)\]((\s|.)*?)\[/\1\]', repl_span, text, 0)

    # lists
    text = re.sub(r'(^\*.*\n){2,}', repl_list, text, 0, re.MULTILINE)

    # headings
    text = re.sub(r'^([=]{1,6})(.*)\1\n', repl_headings, text, 0, re.MULTILINE)

    # now lets cope with those nasty little hobbitses
    text = re.sub(r'(?<!\n)\n(?!\n)', '<br />\n', text)
    text = re.sub(r'(\n){2,}', "</p>\n<p>", text)

    # remove ALL new lines
    text = text.replace('\n', '')

    # in case something has happend to the hobbitses
    text = re.sub(r'/s+\<br \/\>', "<br>", text)
    text = re.sub(r'\<br \/\>/s+', "<br>", text)

    # remove stupid hobbitses (at last)
    text = re.sub(r'\<p\>(\<br \/\>)+', "<p>", text)
    text = re.sub(r'(\<br \/\>)+\<\/p\>', "</p>", text)
    text = re.sub(r'\<p\>\s+', "<p>", text)
    text = re.sub(r'\s+\<\/p\>', "</p>", text)
    text = text.replace("<p></p>", "")

    return text
