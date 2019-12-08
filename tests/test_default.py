

def test_selinux_is_permissive(host):
    cmd = host.run("curl http://localhost | grep 'customos")
    assert cmd.rc == 0
