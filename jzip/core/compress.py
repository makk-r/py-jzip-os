import zlib
import os
import pickle
import platform
from concurrent.futures import ThreadPoolExecutor
def read_file(info):
    try:
        root = info["root"]
        file = info["file"]
        root_rp = info["root_rp"]
        os.path.join(root, file)
        with open(os.path.join(root,file), mode="rb") as f:
            text = f.read()
        data = { "conn" : zlib.compress(text), "path" : f"{root_rp}{file}"}
        return data
    except PermissionError:
        return False
def JZIP1(path,output):
    win = platform.system() == "Windows"
    if os.path.isdir(path):
        jzip = {
            "vers" : "JZIP1",
            "path" : {}
        }
        job = []
        for root , dirs, files in os.walk(path):
            root_rp = os.path.relpath(root, path)
            if root_rp == ".":
                root_rp = ""
            if root_rp != "":
                root_rp = root_rp + "/"
            for file in files:
                job.append({"root" : root,"file" : file ,"root_rp" : root_rp})
        cores = os.cpu_count()
        with ThreadPoolExecutor(max_workers=cores * 4) as executor:
            results = executor.map(read_file, job)
        for c in results:
            if c:
                jzip["path"][c["path"].replace("\\","/")] = c["conn"]
        try:
            with open(output, mode="wb") as f:
                pickle.dump(jzip, f)
        except PermissionError:
            print(f"ERROR : PermissionError")