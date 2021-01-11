import uuid

from nbst.domain.cluster import Cluster


def test_cluster_model_init():
    id = uuid.uuid4()

    cluster = Cluster(name="test-cluster", id=id, type="test-type")

    assert cluster.name == "test-cluster"
    assert cluster.id == id
    assert cluster.type == "test-type"


def test_cluster_model_from_dict():

    id = uuid.uuid4()
    init_dict = {"id": id, "name": "test-cluster", "type": "test-type"}

    cluster = Cluster.from_dict(init_dict)

    assert cluster.id == id
    assert cluster.name == "test-cluster"
    assert cluster.type == "test-type"


def test_cluster_model_to_dict():
    init_dict = {"id": uuid.uuid4(), "name": "test-cluster", "type": "test-type"}

    cluster = Cluster.from_dict(init_dict)

    assert cluster.to_dict() == init_dict


def test_cluster_model_repr():

    init_dict = {"id": 1, "name": "test-cluster", "type": "test-type"}

    cluster = Cluster.from_dict(init_dict)

    assert cluster.__repr__() == "Cluster(id=1, name=test-cluster, type=test-type)"
