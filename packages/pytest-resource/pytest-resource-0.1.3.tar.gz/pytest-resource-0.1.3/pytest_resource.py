import pytest


@pytest.fixture(scope='function')
def resource(request):
    """
    指定されたpathからファイルを読み込む

    @pytest.mark.resource(PATH)
    def test_hoge(resource):
        pass
    """
    resource = request.node.get_closest_marker('resource')
    if resource:
        path = resource.args[0]
        with open(path, 'r') as f:
            data = f.read()

        return data

    else:
        raise ValueError("Resource not found")
