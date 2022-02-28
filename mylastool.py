import os
import azure.storage.blob


def listfiles(container, suffix=''):
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith(suffix):
            files.append((blob.size, blob.name))
    return files


def printdirectory(files):
    for (size, name) in files:
        print(f'{size:<20}{name}')


def getcontainer():
    URL = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(URL)


def readtextfile(container, filename):
    if not filename.endswith(".LAS"):
        raise Exception("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines


def sectionindex(lines, prefix):
    idx = 0
    for line in lines:
        if line.strip().startswith(prefix):
            break
        idx += 1
    return idx


def headersection(lines):
    return lines[0:sectionindex(lines, '~A')]


def printheadersection(lines):
    for line in headersection(lines):
        print(line)


def datasection(lines):
    return lines[sectionindex(lines, '~A')+1:]


def printdatasection(lines):
    for line in datasection(lines):
        print(line)


# python mylastool.py                   - print a help message
# python mylastool.py list              - print a directory of files in container
# python mylastool.py <filename>        - print the LAS headersection
# python mylastool.py <filename> data   - print the LAS datasection


def main(argv):
    container = getcontainer()

    if len(argv) == 1:
        print('usage: python mylastool.py <list|header|data> [filename]')
        return 1

    command = argv[1]

    if argv[1] == 'list':
        lasfiles = listfiles(container, suffix='.LAS')
        printdirectory(lasfiles)
        return 0

    if command not in ('header', 'data'):
        print('')


    if len(argv) < 3:
        print('expected a filename as argument')
        return 1
        
            print('')
    elif argv[1] == 'header':

        lines = readtextfile()

    # ...

    lines = readtextfile(
        container, '31_5-7 Eos/07.Borehole_Seismic/TZV_TIME_SYNSEIS_2020-01-17_2.LAS')
    printdatasection(lines)


if __name__ == '__main__':
    main(sys.argv[:])
