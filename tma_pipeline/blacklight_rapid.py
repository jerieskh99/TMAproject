import xml.etree.ElementTree as ET
import subprocess
import time
import random
import os
import shutil


input_directory_txt = '/Users/jeries/PycharmProjects/simpleCrawler/output_rapid/countries/_txt'
input_directory_xml = '/Users/jeries/PycharmProjects/simpleCrawler/output_rapid/countries/_xml'


def analyze_by_country(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract URLs from the <link> tag
    suffixes = [link.get('suffix') for link in root.findall('.//link') if link.get('suffix')]
    print(suffixes)

    return suffixes


# Function to read URLs from the XML file
def read_urls_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract URLs from the <link> tag
    urls = [link.text.strip() for link in root.findall('.//link') if link.text]
    return urls


def analyze_url_with_blacklight(url):
    result = subprocess.run(["./blacklight", url], capture_output=True, text=True)
    return result.stdout


def save_to_text_file(url, data, folder):
    filename = f"{folder}/{url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
    with open(filename, "w") as file:
        file.write(data)


def save_to_xml_file(url, data, folder):
    root = ET.Element("InspectionResult", url=url)
    ET.SubElement(root, "Data").text = data
    tree = ET.ElementTree(root)
    filename = f"{folder}/{url.replace('https://', '').replace('http://', '').replace('/', '_')}.xml"
    tree.write(filename)


def count_suffixes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Count occurrences of each suffix
    suffix_count = {}
    for link in root.findall('.//link'):
        suffix = link.get('suffix')
        if suffix:
            suffix_count[suffix] = suffix_count.get(suffix, 0) + 1

    return suffix_count


def sort_suffixes_by_count(xml_file):
    # Count the suffixes
    suffix_count = count_suffixes(xml_file)

    # Extract the suffixes and sort them by count
    govs_set = list(suffix_count.keys())
    govs_set.sort(key=lambda x: suffix_count[x], reverse=True)

    return govs_set


gov_domains = [
    ".belgium.be", ".gob.ar", ".gob.bo", ".gob.ve", ".gouv.bf", ".gouv.bj",
    ".gouv.mo", ".gouv.ne", ".gouv.sn", ".gouv.td", ".gouv.tg", ".gouverment.lu",
    ".gov", ".gov.ad", ".gov.af", ".gov.ag", ".gov.ai", ".gov.al", ".gov.am",
    ".gov.ao", ".gov.as", ".gov.au", ".gov.az", ".gov.ba", ".gov.bb", ".gov.bd",
    ".gov.bh", ".gov.bm", ".gov.bn", ".gov.br", ".gov.bs", ".gov.bt", ".gov.bw",
    ".gov.by", ".gov.bz", ".gov.cd", ".gov.cf", ".gov.dz", ".gov.is", ".gov.li",
    ".gov.mc", ".gov.md", ".gov.me", ".gov.mg", ".gov.mh", ".gov.mu", ".gov.tv",
    ".gov.vg", ".gov.vi", ".gov.vn", ".gov.ye", ".gov.za", ".gov.zm", ".gov.zw",
    ".government.bg", ".gub.uy", ".gv.at", ".hob.hn", ".overheid.nl", ".pr.gov",
    ".regjeringen.no", ".rks-gov.net", ".va"
]


# Main function
def main():
    xml_file = 'links.xml'  # Path to your XML file
    urls = read_urls_from_xml(xml_file)
    print(urls)
    delay = 5   # Delay in seconds between requests

    # Select a random sublist of URLs
    selected_urls = random.sample(urls, 100)
    print("------------------------------------------------------------------------------------")

    # Select a covid sublist of URLs
    covid_urls = [url for url in urls if 'covid19' in url.lower() or 'covid-19' in url.lower() or 'covid' in url.lower()
                  or 'covid_19' in url.lower()]
    print(covid_urls)
    print("------------------------------------------------------------------------------------")

    # Select travel sublist
    travel_urls = [url for url in urls if 'travel' in url.lower() or 'tourism' in url.lower()]
    print(travel_urls)
    print("------------------------------------------------------------------------------------")

    # Select economy sublist
    economy_urls = [url for url in urls if 'econ' in url.lower()]
    print(economy_urls)
    print("------------------------------------------------------------------------------------")

    # Select finance sublist
    finance_urls = [url for url in urls if 'finance' in url.lower() or 'finans' in url.lower()
                    or 'finances' in url.lower() or 'financieres' in url.lower() or 'finances' in url.lower()]
    print(finance_urls)
    print("------------------------------------------------------------------------------------")

    # Select migration sublist
    visa_urls = [url for url in urls if 'visa' in url.lower() or 'foreign' in url.lower() or
                 'immigration' in url.lower() or 'goc' in url.lower() or 'migr' in url.lower()]
    print(visa_urls)
    print("------------------------------------------------------------------------------------")

    shuffled_urls = urls.copy()
    random.shuffle(shuffled_urls)

    govs = analyze_by_country(xml_file)
    gov_sorted = sort_suffixes_by_count(xml_file)
    govs_set = list(set(govs))
    # for gov in gov_sorted[45:]:
    #     session_id_dir = gov
    #     os.makedirs(os.path.join(input_directory_xml, session_id_dir), exist_ok=True)
    #     os.makedirs(os.path.join(input_directory_txt, session_id_dir), exist_ok=True)
    #
    #     curr_gov = [url for url in urls if gov in url.lower()]
    #     print(gov, len(curr_gov))
    #     print(curr_gov)
    #     print("------------------------------------------------------------------------------------")
    #     for curr in curr_gov:
    #         print(f"Analyzing {curr}...")
    #         try:
    #             output = analyze_url_with_blacklight(curr)
    #             # Replace 'output_folder' with your desired folder path
    #             save_to_text_file(curr, output, 'output_rapid/countries/_txt/' + gov)
    #             save_to_xml_file(curr, output, 'output_rapid/countries/_xml/' + gov)
    #         except Exception as e:
    #             print(f"An error occurred while analyzing {curr}: {e}")
    #         time.sleep(delay)

    # Select migration sublist
    urls = [
        "argentina.gob.ar", "msal.gob.ar", "economia.gob.ar",
        "educacion.gob.ar", "seguridad.gob.ar", "turismo.gob.ar",
        "agroindustria.gob.ar", "transporte.gob.ar", "cultura.gob.ar",
        "ambiente.gob.ar"
    ]

    print(urls)
    print("------------------------------------------------------------------------------------")

    for url in urls:
        print(f"Analyzing {url}...")
        try:
            output = analyze_url_with_blacklight(url)
            # Replace 'output_folder' with your desired folder path
            save_to_text_file(url, output, 'output_rapid/batch6/batch7/nuris_homeland')
            # save_to_xml_file(url, output, 'output_rapid/batch4/')
        except Exception as e:
            print(f"An error occurred while analyzing {url}: {e}")
        time.sleep(delay)
    '''
    for url in urls:
        print(f"Analyzing {url}...")0
        try:
            output = analyze_url_with_blacklight(url)
            print(output)  # or process/store the output as needed
        except Exception as e:
            print(f"An error occurred while analyzing {url}: {e}")
        time.sleep(delay)  # Rate limiting
    '''


if __name__ == "__main__":
    main()
