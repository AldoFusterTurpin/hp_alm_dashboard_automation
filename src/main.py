# built-in
import datetime
import os
import pathlib

# 3rd party
import requests

# user defined
from src import parse_xml


def check_response_status_code(action_name_performed, response_status_code, expected_status_code):
    if response_status_code != expected_status_code:
        raise Exception("Error during" + action_name_performed + ".Response status was: {}".format(response_status_code))


def log_request_info(url, payload, response_status_code):
    print("_" * 30)
    print("NEW REQUEST: \n url: {}".format(url))
    print("----------\nurl params: ")
    [print("{}: {}".format(k, v)) for k, v in payload.items()]
    print("----------")
    print("Response status: {}".format(response_status_code))
    print("_" * 30)


def get_defect_printos(session, start_index: int = None) -> str:
    payload = {'query': "{user-90['PrintOS']}"}
    if start_index is not None:
        payload['start-index'] = str(start_index)

    url = "https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects"
    response = session.get(url=url, params=payload)
    response_status_code = response.status_code
    check_response_status_code(action_name_performed="get_defects_printos",
                               response_status_code=response_status_code,
                               expected_status_code=200)

    log_request_info(url=url, payload=payload, response_status_code=response_status_code)
    xml_response_str = response.text
    return xml_response_str


def get_defect_printos_and_write_file(session, out_file_name: str, start_index: int = None) -> str:
    xml = get_defect_printos(session, start_index)
    with open(out_file_name, "w+", encoding="utf-8") as out_file:
        out_file.write(xml)
    return xml


def read_credentials():
    # credentials_file_path = os.path.join("..", "credentials.txt")
    credentials_file_path = pathlib.Path("..") / "credentials.txt"

    with open(credentials_file_path, "r", encoding="utf-8") as credentials_file:
        username = credentials_file.readline().strip()
        password = credentials_file.readline().strip()
    return username, password


def sign_in(session, username, password):
    response = session.post(
        url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate?login-form-required=y",
        data="<alm-authentication><user>" + username + "</user><password>" + password + "</password></alm-authentication>")

    check_response_status_code(action_name_performed="authentication SignIn",
                               response_status_code=response.status_code,
                               expected_status_code=200)


def open_session(session):
    '''Action needed after sign-in'''
    response = session.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")

    check_response_status_code(action_name_performed="OpenSession",
                               response_status_code=response.status_code,
                               expected_status_code=201)


def finish_action(xml_result) -> None:
    '''Given the final xml ('xml_result') after the requests and modifications, this function indicates what to do with
    the result (write it on disk, send an email or send it to Google drive, etc.)'''

    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d__%H_%M_%S")

    # create (if doesn't exist) folder where we store the output files
    pathlib.Path("../output").mkdir(parents=True, exist_ok=True)
    extension = ".xml"
    output_path = pathlib.Path("../output" + "/" + file_name + extension)

    with open(output_path, "w+", encoding="utf-8") as out_file:
        out_file.write(xml_result)


def main():
    # The Session object allows you to persist certain parameters across requests.
    # It also persists cookies across all requests made from the Session instance
    session = requests.Session()
    username, password = read_credentials()

    # activating authentication for the session
    session.auth = (username, password)

    sign_in(session=session, username=username, password=password)

    open_session(session=session)

    # final xml accumulated in 'result'
    result = get_defect_printos(session=session, start_index=None)

    # index parameter of the GET requests
    start_index = 101

    upper_bound = 901
    while start_index <= upper_bound:
        tmp_xml = get_defect_printos(session=session, start_index=start_index)
        result = parse_xml.merge(original_xml=result, second_xml=tmp_xml)
        start_index += 100

    finish_action(result)


if __name__ == "__main__":
    main()
