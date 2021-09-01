import os
import stat
import sys

# SCRIPT RELATED
FEED_FILE_NAME = "feed.sh"
SHELL_SHEBANG = "#!/bin/bash"
FEED_DL_APP = "youtube-dl"

# FEED FIELDS
FEED_FIELD_TITLE = "title"
FEED_FIELD_XML_URL = "xmlUrl"
# IGNORED FIELDS
FEED_FIELD_TEXT = "text"
FEED_FIELD_TYPE = "type"
FEED_FIELD_HTML_URL = "htmlUrl"

class RssFeed:
    def __init__(self, title, url_xml):
        # self.text = text
        # self.feed_type = feed_type
        # self.url_html = url_html
        self.title = title
        self.url_xml = url_xml

# Feed Builder Functions

def get_feeds_from_opml_file(path):
    feeds = []
    with open(path, "r") as f:
        for line in f.readlines():
            if is_valid_feed(line):
                feed = build_rss_object(line)
                feeds.append(feed)
    return feeds

def is_valid_feed(input):
    return FEED_FIELD_TITLE in input and FEED_FIELD_XML_URL in input


def get_xml_field_value(field_name, xml_string):
    # Start of field name
    cursor = xml_string.index(field_name)
    # End of Field name
    cursor += len(field_name)
    # Start of first "
    cursor += xml_string[cursor:].index('"') + 1
    # Start of last "
    end_point = xml_string[cursor:].index('"')
    # Need to add cursor (current start) to end_point so we get full portion of string
    return xml_string[cursor:cursor + end_point]

def build_rss_object(feed_details):
    # text = get_xml_field_value(FEED_FIELD_TEXT, feed_details)
    # feed_type = get_xml_field_value(FEED_FIELD_TYPE, feed_details)
    # url_html = get_xml_field_value(FEED_FIELD_HTML_URL, feed_details)
    title = get_xml_field_value(FEED_FIELD_TITLE, feed_details)
    url_xml = get_xml_field_value(FEED_FIELD_XML_URL, feed_details)

    #feed = RssFeed(text, title, feed_type, url_html, url_xml)
    feed = RssFeed(title, url_xml)
    return feed

def feed_builder(filepath):
    feeds = get_feeds_from_opml_file(filepath)
    organized = {}
    for feed in feeds:
        if feed.title in organized:
            if feed.url_xml not in organized.get(feed.title):
                organized.append(feed.url_xml)
        else:
            organized[feed.title] = [feed.url_xml]
    # ToDo - In case we have several with the same name, append to name?
    #filtered = {k:v for (k,v) in organized.items() if len(v) != 1}
    return feeds

def normalize_folder_name(folder_name):
    keep_chars = (' ','.','_', '-')
    return "".join(c for c in folder_name if c.isalnum() or c in keep_chars).rstrip()

def feed_downloader(feeds):
    delim = os.path.sep

    for feed in feeds:
        folder_name = normalize_folder_name(feed.title)
        file_path = delim.join([os.getcwd(),  folder_name, FEED_FILE_NAME])

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        feed_dl_file  = []
        feed_dl_file.append(SHELL_SHEBANG)
        feed_dl_file.append("")
        feed_dl_file.append("{} \"{}\"".format(FEED_DL_APP, feed.url_xml))
        dl_file_contents = '\n'.join(feed_dl_file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(dl_file_contents)
                f.close()
                os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IEXEC)

def main():
    if len(sys.argv) == 1:
        exit("No opml filename passed to script. Exiting.")

    filepath = sys.argv[1]
    feeds = feed_builder(filepath)
    feed_downloader(feeds)

if __name__ == '__main__':
    main()

