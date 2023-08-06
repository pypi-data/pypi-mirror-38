import requests, zipfile, io, os, shutil, argparse

version = 'v0.1-alpha'

class Duplicate(Exception):
    pass

class DownloadError(Exception):
    pass

URL = 'http://github.com/arissupriy/dooflask/archive/{}.zip'
def create_url(version):
    return URL.format(version)

def download(version, name, path=None):
    http = requests.get(create_url(version))
    
    if http.status_code == 404:
        raise DownloadError('404, Version of dooflask not found, please use another version')
        exit(1)
    if http.status_code != 200:
        raise DownloadError('Error downloading Template')
        exit(1)

    a = http.content
    

    zf = zipfile.ZipFile(io.BytesIO(a))

    with zf as zip_file:
        for member in zip_file.namelist():
            all_dir = os.path.dirname(member).split('/')
            del all_dir[0]

            filename = os.path.basename(member)        

            # skip directories
            if not filename:
                continue
            
            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            
            target = open(os.path.join(name, filename), "wb")
            if len(all_dir) != 0:
                base = os.path.join(*all_dir)
                if not os.path.isdir(os.path.join(name, base)):
                    os.mkdir(os.path.join(name, base))
                target = open(os.path.join(name, os.path.join(base, filename)), "wb")
            
            print(target)
                
            with source, target:
                shutil.copyfileobj(source, target)


def doo():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    
    parser = argparse.ArgumentParser(
            description=""
            )
    parser.add_argument('--name', metavar='project_name', help='Name of project')
    parser.add_argument('--dooversion', metavar='version', help='dooflask version want to install', default=version)
    parser.add_argument('--path', metavar='PATH', help='custom path can you use', default=str(os.getcwd()))
    parser.add_argument('-v', help='version of latest dooflask', action='store_true', default=version)
    
    
    args, unknown = parser.parse_known_args()

    argdic = vars(args)

    if args.v == True:
        print("dooflask {}".format(version))
        exit(1)


    if not all( v for _,v in argdic.items() ):
        parser.print_help()
        exit(1)

    path = os.path.join(argdic['path'], argdic['name'])
    if os.path.isdir(path):
        raise Duplicate("Project {} is exists, please use other name".format(argdic['name']))
        exit(1)

    try:
        import sys
        print("...........")
        print("create folder {}".format(argdic['name']))
        os.mkdir(path)
        download(argdic['dooversion'], argdic['name'], path)
        print("...........")
        print("project {} created".format(argdic['name']))
    except Exception as e:
        print
        print(e)
        print("deleting folder {}".format(argdic['name']))
        print("error creating project")
        os.rmdir(path)
    
    exit(1)