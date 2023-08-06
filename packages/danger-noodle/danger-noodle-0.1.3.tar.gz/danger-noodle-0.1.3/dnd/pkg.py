import urllib2
import sys
import bs4
import os
import shutil

cwd = os.getcwd()

def install(package):
    package_version = get_package(package)
    print "Installing %s" % package_version
    package_name = package_version.split("@")[0]
    if os.path.isdir(package_name):
        return "%s is already installed" % package_version
    else:
        os.mkdir(package_name)
        os.chdir(package_name)
    url = "https://unpkg.com/%s/" % package_version
    path = "%s/js-packages/%s" % (cwd, package_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    traverse(url, path)
    os.chdir(cwd)
    return package_version

def uninstall(package):
    package_name = get_package(package)
    print "Uninstalling %s" % package_name
    shutil.rmtree(package_name.split("@")[0])
    return package_name

def get_package(package):
    if not os.path.isdir("js-packages"):
        os.mkdir("js-packages")
    os.chdir("js-packages")
    url = "https://unpkg.com/%s/" % package
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.geturl().split("/")[3]

def traverse(package_url, path):
    response = urllib2.urlopen(package_url)
    content_type = response.info().getheader('Content-Type').split(";")[0]
    ignore = ["../", "js", "scss"]
    if content_type == "text/html":
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
        html = response.read()
        data = bs4.BeautifulSoup(html, "html.parser")
        for l in data.find_all("a"):
            if l["href"] not in ignore:
                file_url = "%s%s" % (package_url , l["href"])
                new_path = "%s/%s" % (path, file_url.split("/")[-2])
                traverse(file_url, new_path)
        os.chdir("..")
    else:
        with open("%s" % (response.geturl().split("/")[-1]), "w") as f:
            f.write(response.read())

def main():
    if len(sys.argv) > 2:
        print "Searching for %s" % sys.argv[2]
        cmd = sys.argv[1]
        if cmd == "install":
            installed_package_version = install(sys.argv[2])
            with open("%s/snakeskin.txt" % cwd, "a") as f:
                f.write(installed_package_version + "\n")
                f.close()
        elif cmd == "uninstall":
            uninstalled_package_version = uninstall(sys.argv[2])
            with open("%s/snakeskin.txt" % cwd, "r") as f:
                packages = f.read().split("\n")
            packages.remove(uninstalled_package_version)
            with open("%s/snakeskin.txt" % cwd, "w") as f:
                for package in packages:
                    f.write(package)
                f.write("\n")
            
    else:
        if os.path.isfile("%s/snakeskin.txt" % cwd):
            with open("%s/snakeskin.txt" % cwd, "r") as f:
                packages = f.read().split("\n")
            for package in packages:
                if len(package) > 0:
                    install(package)

if __name__ == "__main__":
    main()