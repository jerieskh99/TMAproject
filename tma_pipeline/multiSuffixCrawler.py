import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as Et
import urllib.parse
import time as t


test_tld = ["gov.it"]


all_tld = [
    "gov.bi", "gov.cv", "gov.kh", "gov.cm", "gc.ca", "gov.ky", "gov.cf", "gouv.td",
    "gob.cl", "gov.cn", "gov.co", "gov.cd", "gouv.cg", "gov.ck", "go.cr", "gov.eg",
    "gob.cu", "gov.cy", "gov.cz", "gov.dk", "gouv.dj", "gov.dm", "gob.do", "gov.tl",
    "gob.ec", "gov.eg", "gob.sv", "gob.gq", "gov.ee", "gov.sz", "gov.et", "gov.fk",
    "gov.fj", "gov.fi", "gouv.fr", "gov.pf", "gouv.ga", "gov.gm", "gov.ge", "bund.de",
    "gov.gh", "gov.gr", "gov.gd", "gov.gov", "gob.gt", "gov.gg", "gov.gn", "gov.gw",
    "gov.gy", "gouv.ht", "hob.hn", "gov.hk", "gov.hu", "gov.is", "gov.in", "go.id",
    "gov.ir", "gov.iq", "gov.ie", "gov.im", "gov.il", "gov.it", "gov.jm", "go.jp",
    "gov.je", "gov.jo", "gov.kz", "go.ke", "gov.ki", "go.kr", "rks-gov.net", "gov.kw",
    "gov.kg", "gov.la", "gov.lv", "gov.lb", "gov.ls", "gov.lr", "gov.ly", "gov.li",
    "gov.lt", "gouverment.lu", "gov.mo", "gov.mg", "gov.mw", "gov.my", "gov.mv",
    "gouv.ml", "gov.mt", "gov.mh", "gov.mr", "gov.mu", "gob.mx", "gov.fm", "gov.md",
    "gouv.mo", "gov.mc", "gov.me", "gov.ms", "gov.ma", "gov.mz", "gov.mm", "gov.na",
    "gov.np", "overheid.nl", "govt.nz", "gob.ni", "gouv.ne", "gov.ng", "gov.nu",
    "gov.mk", "gov.mp", "regjeringen.no", "gov.om", "gov.pk", "gob.pa", "gov.pg",
    "gov.py", "gob.pe", "gov.ph", "gov.pn", "gov.pl", "gov.pt", "pr.gov", "gov.qa",
    "gov.ro", "gov.ru", "gov.rw", "gov.sh", "gov.kn", "gov.lc", "gov.vc", "gov.ws",
    "gov.sm", "gov.st", "gov.sa", "gouv.sn", "gov.rs", "gov.sc", "gov.sl", "gov.sg",
    "gov.sx", "gov.sk", "gov.si", "gov.sb", "gov.so", "gov.za", "gov.ss", "gob.es",
    "gov.lk", "gov.sd", "gov.sr", "gov.se", "admin.ch", "gov.sy", "gov.tw", "gov.tj",
    "go.tz", "go.th", "gouv.tg", "gov.to", "gov.tt", "gov.tn", "gov.tr", "gov.tm",
    "gov.tc", "gov.tv", "gov.vi", "go.ug", "gov.ua", "gov.ae", "gov.uk", "gov",
    "gub.uy", "gov.uz", "gov.vu"
]


def search_duckduckgo(suffix, query, num_results):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Add logic to extract links
    # Note: This part is not implemented in this snippet
    # ...

    # Find all <a> tags in the HTML
    links = soup.find_all('a')

    filtered_links = []

    for link in links:
        href = link.get('href')
        if href and suffix in href:
            # Extract the actual URL from DuckDuckGo's redirect URL
            start = href.find('https')
            if start != -1:
                encoded_url = href[start:]
                # Decode the percent-encoded URL
                decoded_url = urllib.parse.unquote(encoded_url)
                # Optional: truncate URL at a delimiter if necessary
                # end = decoded_url.find('&')
                # if end != -1:
                #     decoded_url = decoded_url[:end]
                # Remove the data after the last slash
                last_slash_index = decoded_url.rfind('/')
                if last_slash_index != -1:
                    decoded_url = decoded_url[:last_slash_index]

                filtered_links.append(decoded_url)

    unique_links = list(set(filtered_links))[:num_results]

    # print(unique_links)

    return unique_links


# def main(all_websites):
#     for suffix in all_websites:
#         print(f"Searching for websites with the suffix: .{suffix}")
#         query = f"site:.{suffix}"
#         links = search_duckduckgo(suffix, query, 50)
#
#         # Process and print the links
#         # This could be replaced with more complex processing or storing logic
#         for link in links:
#             print(link)
#         print("\n")  # Print a newline for readability between different suffix searches

def main(all_websites):
    # Open or create the XML file for writing
    with open('links.xml', 'w') as file:
        # Create the root element of the XML file
        root = Et.Element("root")
        delay = 10
        for suffix in all_websites:
            print(f"Searching for websites with the suffix: .{suffix}")
            query = f"site:.{suffix}"
            links = search_duckduckgo(suffix, query, 50)

            # For each link, create an XML element and append it to the root
            for link in links:
                Et.SubElement(root, "link", suffix=suffix).text = link

        # Convert the tree to a string and write to the file
        tree = Et.ElementTree(root)
        tree.write(file)
        t.sleep(delay)

# Example usage
example = ['gov', 'edu', 'org']  # Example list of website suffixes


if __name__ == '__main__':
    main(test_tld)

