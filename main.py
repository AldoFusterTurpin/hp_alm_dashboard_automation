from lxml import etree
from copy import deepcopy
import requests


def get_defect_printos(session, start_index: int):
    payload = {'query': "{user-90['PrintOS']}"}

    if start_index is not None:
        payload['start-index'] = str(start_index)

    # important: utf8 encoding
    print("url params:", end=" ")
    [print(k, v) for k, v in payload.items()]
    print()
    url = "https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects"
    response = session.get(url=url, params=payload)
    print("Response status: {}".format(response.status_code))
    print("*" * 50)
    xml_response = response.text.encode('utf8')
    return xml_response


def get_defect_printos_and_write_files(session, out_file_name: str, start_index: int):
    xml = get_defect_printos(session, start_index)
    with open(out_file_name, "wb") as out_file:
        out_file.write(xml)


def main():
    # The Session object allows you to persist certain parameters across requests.
    # It also persists cookies across all requests made from the Session instance
    with requests.Session() as session:
        with open("credentials.txt", "r") as credentials_file:
            username = credentials_file.readline().strip()
            password = credentials_file.readline().strip()

        # activating authentication for the session
        session.auth = (username, password)

        # post authentication
        session.post(url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate?login-form-required=y",
                     data="<alm-authentication><user>" + username + "</user><password>" + password + "</password></alm-authentication>")

        # check if authenticated (optional)
        # s.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
        #       headers={"Content-Type": "application/xml"})

        # post log-in
        session.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")

        start_index = None
        get_defect_printos_and_write_files(session=session, out_file_name="out0.xml", start_index=start_index)
        start_index = 101
        while start_index <= 901:
            get_defect_printos_and_write_files(session=session, out_file_name="out" + str(start_index) + ".xml",
                                               start_index=start_index)
            start_index += 100



if __name__ == "__main__":
    main()
