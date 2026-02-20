import zlib
import os
import pickle
import platform
def JZIP1(path,output):
    win = platform.system() == "Windows"
    if os.path.isfile(path):
        try:
            with open(path, mode="rb") as f:
                jzip = pickle.load(f)
        except PermissionError:
            print("ERROR PermissionError")
        except pickle.UnpicklingError:
            print("ERROR : It's not a recognized file.")
        os.makedirs(output, exist_ok=True)
        for p, c in jzip["path"].items():
            try:
                if len(p.split("/")) != 1:
                    os.makedirs(os.path.join(output,os.path.dirname(p)), exist_ok=True)
                c = zlib.decompress(c)
                if win:
                    with open(os.path.join(output, p.replace("/","\\")), mode="wb") as f:
                        f.write(c)
                else:
                    with open(os.path.join(output, p), mode="wb") as f:
                        f.write(c)
            except PermissionError:
                continue
def MAIN(path,output):
    if os.path.isfile(path):
        try:
            with open(path, mode="rb") as f:
                jzip = pickle.load(f)
        except PermissionError:
            print("ERROR PermissionError")
        except pickle.UnpicklingError:
            print("ERROR : It's not a recognized file.")
    if jzip["vers"] == "JZIP1":
        JZIP1(path,output)