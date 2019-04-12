from .solver import parse_claim, Claim, Fabric


def test_parse_claim():
    assert parse_claim('#1357 @ 789,377: 13x14') == (1357, 789, 377, 13, 14)


def test_claim():
    claim = Claim.create_claim_from_string('#1337 @ 111,112: 1x99')
    assert claim.id == 1337
    assert claim.left == 111
    assert claim.top == 112
    assert claim.width == 1
    assert claim.height == 99


def test_fabric():
    fabric = Fabric()
    assert fabric.claims == []
    assert fabric.squares == {}

    for claim_string in ('#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2'):
        claim = Claim.create_claim_from_string(claim_string)
        fabric.add_claim(claim)

    assert fabric.claims[0].id == 1
    assert fabric.claims[2].id == 3
    assert len(fabric.squares) == 6*6-4

    assert 1 not in fabric.squares[(3, 1)].claims
    assert 2 in fabric.squares[(3, 1)].claims
    assert 3 not in fabric.squares[(3, 1)].claims

    assert 1 in fabric.squares[(1, 3)].claims
    assert 2 not in fabric.squares[(1, 3)].claims
    assert 3 not in fabric.squares[(1, 3)].claims

    assert 1 in fabric.squares[(3, 3)].claims
    assert 2 in fabric.squares[(3, 3)].claims
    assert 3 not in fabric.squares[(3, 3)].claims

    assert 1 not in fabric.squares[(6, 6)].claims
    assert 2 not in fabric.squares[(6, 6)].claims
    assert 3 in fabric.squares[(6, 6)].claims

    assert fabric.number_of_squares_with_more_than_one_claim() == 4

    assert fabric.find_good_claim().id == 3
