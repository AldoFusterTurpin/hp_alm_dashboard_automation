import requests


with requests.Session() as s:
    in_file = open("credentials.txt", "r")
    username = in_file.readline().strip()
    password = in_file.readline().strip()
    in_file.close()

    s.auth = (username, password)

    s.post(url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate",
           data="<alm-authentication><user>"+username+"</user><password>"+password+"</password></alm-authentication>")

    # s.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
    #       headers={"Content-Type": "application/xml"})

    s.post(url="https://alm-1.azc.ext.hp.com/qcbin/rest/site-session")

    r = s.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/domains/IPG_GIB/projects/LFP_Programs/defects",
              params={'query': "{user-90['PrintOS']}"})

    with open("out.xml", "w") as out_file:
        out_file.write(r.text)
