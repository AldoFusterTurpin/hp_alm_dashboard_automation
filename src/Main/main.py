import pathlib
import requests
from src.Parse_xml import parse_xml


def check_response_status_code(action_name_performed, response_status_code, expected_status_code):
    if response_status_code != expected_status_code:
        raise Exception("Error during" + action_name_performed + ".Response status was: {}".format(response_status_code))


def log_request_info(url, payload, response_status_code) -> None:
    print("_" * 50)
    print("NEW REQUEST: \n url: {}".format(url))
    print("----------\nurl params: ")
    [print("{}: {}".format(k, v)) for k, v in payload.items()]
    print("----------")
    print("Response status: {}".format(response_status_code))
    print("_" * 50)


def get_defect_printos(session, start_index: int = None) -> str:
    payload = {'query': "{user-90['PrintOS']}"}
    if start_index is not None:
        payload['start-index'] = str(start_index)

    url = "https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects"
    response = session.get(url=url, params=payload)
    check_response_status_code(action_name_performed="get_defects_printos",
                               response_status_code=response.status_code,
                               expected_status_code=200)

    log_request_info(url=url, payload=payload, response_status_code=response.status_code)
    return response.text


def get_defect_printos_and_write_file(session, out_file_name: str, start_index: int = None) -> str:
    xml = get_defect_printos(session, start_index)
    with open(out_file_name, "w+", encoding="utf-8") as out_file:
        out_file.write(xml)
    return xml


def read_credentials():
    credentials_file_path = pathlib.Path("..") / ".." / "credentials.txt"
    with open(credentials_file_path, "r", encoding="utf-8") as credentials_file:
        username = credentials_file.readline().strip()
        password = credentials_file.readline().strip()
    return username, password


def sign_in(session, username, password) -> None:
    response = session.post(
        url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate?login-form-required=y",
        data="<alm-authentication><user>" + username + "</user><password>" + password + "</password></alm-authentication>")

    check_response_status_code(action_name_performed="authentication SignIn",
                               response_status_code=response.status_code,
                               expected_status_code=200)


def open_session(session) -> None:
    '''Action needed after sign-in'''
    response = session.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")

    check_response_status_code(action_name_performed="OpenSession",
                               response_status_code=response.status_code,
                               expected_status_code=201)


def finish_action(xml_result) -> None:
    '''Given the final xml ('xml_result') after the requests and modifications, this function indicates what to do with
    the result (write it on disk, send an email or send it to Google drive, etc.)'''

    out_folder_path_str = "../../output"
    # create (if doesn't exist) folder where we store the output files
    pathlib.Path(out_folder_path_str).mkdir(parents=True, exist_ok=True)

    # file_name = datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S")
    file_name = "result"
    extension = ".xml"

    output_path = pathlib.Path(out_folder_path_str + "/" + file_name + extension)

    with open(output_path, "w+", encoding="utf-8") as out_file:
        out_file.write(xml_result)


def create_requests_session():
    return requests.Session()


def main():
    # The Session object allows you to persist certain parameters across requests.
    # It also persists cookies across all requests made from the Session instance
    session = create_requests_session()
    username, password = read_credentials()

    # activating authentication for the session
    session.auth = (username, password)

    sign_in(session=session, username=username, password=password)
    open_session(session=session)

    # final xml accumulated in 'result'
    result = get_defect_printos(session=session, start_index=None)

    total_entities = parse_xml.get_entities_total_results(result)
    # print("total_entities: {}, type: {}".format(total_entities, type(total_entities)))

    Entity_nodes_counter = parse_xml.get_number_of_Entity_nodes(result)
    # print("Entity_nodes_counter before while: {}, type: {}".format(Entity_nodes_counter, type(Entity_nodes_counter)))

    # index parameter of the GET requests
    start_index = 101

    while Entity_nodes_counter < total_entities:
        # print("{} <= {}".format(Entity_nodes_counter, total_entities))
        # print(Entity_nodes_counter <= total_entities)
        tmp_xml = get_defect_printos(session=session, start_index=start_index)

        Entity_nodes_counter += parse_xml.get_number_of_Entity_nodes(tmp_xml)
        # print("Entity_nodes_counter in while: {}".format(Entity_nodes_counter))

        result = parse_xml.merge(original_xml=result, second_xml=tmp_xml)

        start_index += 100

    session.close()
    finish_action(result)


if __name__ == "__main__":
    main()
