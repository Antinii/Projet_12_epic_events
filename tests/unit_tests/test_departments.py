from models.departments import Department
from controllers.departments_controller import get_departments


def test_get_departments(session, capsys):
    predefined_departments = [
        {"name": "Commercial"},
        {"name": "Support"},
        {"name": "Management"}
    ]

    for dept in predefined_departments:
        department = Department(name=dept["name"])
        session.add(department)

    session.commit()

    get_departments(session)
    captured = capsys.readouterr()

    for dept in predefined_departments:
        assert dept["name"] in captured.out
