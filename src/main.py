import requests
import os
from src import parse_xml


def get_defect_printos(session, start_index: int = None) -> str:
    payload = {'query': "{user-90['PrintOS']}"}

    if start_index is not None:
        payload['start-index'] = str(start_index)

    url = "https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects"

    print("_" * 30)
    print("NEW REQUEST: \n url: {}".format(url))
    print("----------\nurl params: ")
    [print("{}: {}".format(k, v)) for k, v in payload.items()]
    print("----------")

    response = session.get(url=url, params=payload)

    response_status_code = response.status_code
    if response_status_code != 200:
        raise Exception("Error during get_defects_printos. Response status was: {}".format(response_status_code))

    print("Response status: {}".format(response_status_code))
    print("_" * 30)

    xml_response = response.text  # type str
    # print("type of xml_response: {}".format(type(xml_response))) # debug info
    return xml_response


def get_defect_printos_and_write_file(session, out_file_name: str, start_index: int = None) -> str:
    xml = get_defect_printos(session, start_index)
    with open(out_file_name, "w", encoding="utf-8") as out_file:
        out_file.write(xml)
    return xml


def finish_action(xml_result) -> None:
    '''Given the final xml ('xml_result') after the requests and modifications, this function indicates what to do with
    the result (write it on disk, send an email or send it to Google drive, etc.)'''
    # print(xml_result)

    file_path = os.path.join("..", "output", "result.xml")
    with open(file_path, "w", encoding="utf-8") as out_file:
        out_file.write(xml_result)


def main():
    # The Session object allows you to persist certain parameters across requests.
    # It also persists cookies across all requests made from the Session instance
    with requests.Session() as session:
        file_path = os.path.join("..", "credentials.txt")
        with open(file_path, "r", encoding="utf-8") as credentials_file:
            username = credentials_file.readline().strip()
            password = credentials_file.readline().strip()

        # activating authentication for the session
        session.auth = (username, password)

        # post authentication SignIn
        response = session.post(url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate?login-form-required=y",
                     data="<alm-authentication><user>" + username + "</user><password>" + password + "</password></alm-authentication>")
        response_status_code = response.status_code
        if response_status_code != 200:
            raise Exception("Error during authentication SignIn. Response status was: {}".format(response_status_code))

        # check if authenticated (optional)
        # session.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
        #       headers={"Content-Type": "application/xml"})

        # post OpenSession
        response = session.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")
        response_status_code = response.status_code
        if response_status_code != 201:
            raise Exception("Error during OpenSession. Response status was: {}".format(response_status_code))

        # I will accumulate the final xml in 'result'
        result = get_defect_printos(session=session, start_index=None)

        # index parameter of the GET requests
        start_index = 101
        while start_index <= 901:
            tmp_xml = get_defect_printos(session=session, start_index=start_index)
            result = parse_xml.merge(original_xml=result, second_xml=tmp_xml)
            start_index += 100

        finish_action(result)


if __name__ == "__main__":
    main()
