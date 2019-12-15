

def test_apache_httpd_is_working(host):
    cmd = host.run("curl http://localhost | grep 'customos'")
    assert cmd.rc == 0
