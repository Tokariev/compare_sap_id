import sys
from urllib.request import urlopen
import urllib.error as exc
from xml.etree.ElementTree import parse
import os

kaufland_url = 'http://sapxmllogonweb.lidl.net/SAPLOGON_KIS.xml'
sit_url = 'http://sapxmllogonweb.lidl.net/SAPUILandscape.xml'


def get_ids_by_url(url):
    response = urlopen(url)
    xmldoc = parse(response)
    root = xmldoc.getroot()
    systemid_list = []

    for service in root.iter('Service'):
        systemid = service.get('systemid')
        systemid_list.append(systemid)

    return systemid_list


def get_absolut_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name


def run():
    try:
        kaufland_list = get_ids_by_url(kaufland_url)
        sit_list = get_ids_by_url(sit_url)
    except exc.URLError as e:
        print('Reason:', e.reason)
        input("\n\nPress the enter key to exit.")
    except exc.HTTPError as e:
        print('Reason:', e.reason)
        input("\n\nPress the enter key to exit.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        input("\n\nPress the enter key to exit.")
    else:
        missing_list = []

        for kaufland_id in kaufland_list:
            if kaufland_id not in sit_list:
                missing_list.append(kaufland_id)
                print(kaufland_id)

        print('Kaufland IDs:', len(kaufland_list))
        print('SIT IDs:', len(sit_list))
        print('Missing IDs:', len(missing_list))

        name_of_file = 'Missing_IDs_' + str(len(missing_list)) + '.txt'

        try:
            with open(name_of_file, 'w') as f:
                for missing_id in missing_list:
                    f.write("%s\n" % missing_id)

            print('Die Liste mit fehlende System ID wurde erstellt: ', get_absolut_path(name_of_file))
            f.close()
            input("\n\nPress the enter key to exit.")
        except IOError as e:
            print(e)
        finally:
            f.close()


if __name__ == "__main__":
    run()

