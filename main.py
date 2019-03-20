from lxml import etree
from copy import deepcopy
import requests


def get_defect_printos(session, start_index: int = 0):
    return session.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects",
                       params={'query': "{user-90['PrintOS']}"}).text


def get_defect_printos_and_write_files(session, out_file_name: str, start_index: int = 0):
    with open(out_file_name, "w") as out_file:
        out_file.write(get_defect_printos(session, start_index))


# The Session object allows you to persist certain parameters across requests.
# It also persists cookies across all requests made from the Session instance
with requests.Session() as session:
    with open("credentials.txt", "r") as credentials_file:
        username = credentials_file.readline().strip()
        password = credentials_file.readline().strip()

        # activating authentication for the session
        session.auth = (username, password)

        # post authentication
        session.post(url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate",
                     data="<alm-authentication><user>"+username+"</user><password>"+password+"</password></alm-authentication>")

        # s.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
        #       headers={"Content-Type": "application/xml"})

        # post log-in
        session.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")

        start_index = 0
        get_defect_printos_and_write_files(session=session, out_file_name="out"+str(start_index)+".xml", start_index=start_index)
        start_index = 101
        while start_index <= 901:
            get_defect_printos_and_write_files(session=session, out_file_name="out"+str(start_index)+".xml", start_index=start_index)
            start_index += 100

        # root1 = etree.fromstring(defect_printos.text.encode('utf-8'))
        # tree1 = etree.ElementTree(root1)

