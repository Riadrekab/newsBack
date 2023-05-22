import requests

url = "http://aiasvm1.amcl.tuc.gr:8085"
username = "your_username"  # remember your username !
password = "your_password"  # remember your password !


def create_project(project_name=""):
    request = requests.post(f"{url}/createProject?project_name={project_name}",
                            auth=(username, password))

    if request.status_code != 200:
        print("Error creating project")
        return False
    return request.json()


# print(create_project("test_project"))


def addFile(file="", project="", type=""):
    files = {'file': open(f'{file}', 'rb')}

    r = requests.post(f"{url}/addFile?project={project}&type={type}", files=files,
                      auth=(username, password))
    if r.status_code != 200:
        print(r.status_code)
        return False
    return r.json()


# print(addFile("testPolicies.pl", "test_project", "gorgias"))


def updateFile(file="", project="", type=""):
    files = {'file': open(f'{file}', 'rb')}

    r = requests.post(f"{url}/updateFile?project={project}&type={type}", files=files,
                      auth=(username, password))
    if r.status_code != 200:
        print("error updating file")
        return False
    return r.json()


# print(updateFile("testPolicies.pl", "test_project", "gorgias"))


def deleteProject(project=""):
    r = requests.post(f"{url}/deleteProject?project={project}", auth=(username, password))
    if r.status_code != 200:
        print("error deleting project")
        return False
    return r.json()


def deleteFile(filename="", project="", ):
    r = requests.post(f"{url}/deleteFile?filename={filename}.pl&project={project}", auth=(username, password))
    if r.status_code != 200:
        print("error deleting file")
        return False
    return r.json()


def queryGorgias(facts=[], gorgias_file=""):
    query = "stay_home"  # prolog query
    data = {
        "facts": facts,
        "gorgiasFiles": [
            gorgias_file
        ],
        "query": query,
        "resultSize": 1
    }

    r = requests.post(f"{url}/GorgiasQuery", json=data, auth=(username, password))

    if r.status_code != 200:
        print("error querying gorgias")
        return False
    return r.json()

# Returns the result of the query
# print(queryGorgias(facts=["nice_movie"], gorgias_file="test_project/testPolicies.pl"))
