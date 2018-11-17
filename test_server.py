import pytest
from server import find_avg
from server import validate_post


@pytest.mark.parametrize("candidate, expected", [
                             ({
                                  "patient_id": "1",
                                  "attending_email": "user@duke.edu",
                                  "user_age": 1,
                                     }, 1),
                             ({
                                  "ptient_id": "1",
                                  "attending_email": "user@duke.edu",
                                  "user_age": 1,
                                     }, 0),
                         ])
def test_validate_post(candidate, expected):
    check = validate_post(candidate)
    assert check == expected


@pytest.mark.parametrize("candidate, expected", [
                             ([1, 3, 5], 3),
                        ])
def test_find_avg(candidate, expected):
    avg = find_avg(candidate)
    assert avg == expected
