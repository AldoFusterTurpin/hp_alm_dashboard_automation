import requests


def log_in():
    # default HTTP Basic Auth
    r = requests.post(url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate",
                     auth=("carmen.pardo_hp.com", "sun.ill-21"),
                     data="<alm-authentication><user>carmen.pardo_hp.com</user><password>sun.ill-21</password></alm-authentication>")
    print("Status response of log_in: {}".format(r.status_code))
    print("Log_in headers response: {}".format(r.headers))
    print("Cookies response of log_in:")
    [print(c) for c in r.cookies]
    print("*" * 50)

    return r.cookies


def check_logged_in(_cookies):
    r = requests.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
                     headers={"Content-Type": "application/xml"},
                     cookies=_cookies,
                     auth=("carmen.pardo_hp.com", "sun.ill-21"))
    # print("checked_logged_in headers response: {}".format(r.headers))
    print(r.text)
    print("*" * 50)


def open_session(_cookies):
    r = requests.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session",
                      cookies=_cookies,
                      auth=("carmen.pardo_hp.com", "sun.ill-21"))

    # with this I obtain more cookies that I'll need for the future GET's
    return r.cookies


def first_get(_cookies):
    r = requests.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects",
                     auth=("carmen.pardo_hp.com", "sun.ill-21"),
                     cookies=_cookies,
                     params={'query': "{user-90['PrintOS']}"})
    print("First get body: \n" + r.text)

    # print("_____________")
    # print("First get headers:")
    # print(r.headers)
    # print("_____________")
    print("*" * 50)


def main():
    _cookies = log_in()
    check_logged_in(_cookies)
    _cookies = open_session(_cookies)
    print(_cookies)


main()
