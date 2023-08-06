import requests
from typing import Tuple, Optional, List

from breathe.exceptions import ObjectDoesNotExist


class Course():
    """Caveats: company training type ID is not retreivable through the API"""
    """
    Example Schema:
        {
          "company_sicknesstype": null,
          "company_training_type_id": null, *
          "employee": null, *
          "name": null, *
          "id": null,
          "start_date": null,
          "end_date": null,
          "half_start": null,
          "half_start_am_pm": null,
          "half_end": null,
          "half_end_am_pm": null,
          "deducted": null,
          "status": null,
          "reason": null,
          "review_notes": null,
          "fit_note_required": null
        }
    """
    def __init__(self, client):
        self.client = client

    def all(self) -> List[dict]:
        """
        Gets all employee training courses
        :return: a list of dictionaries
        """
        endpoint = "employee_training_courses"
        response = self.client.request("GET", endpoint)
        if requests.codes.ok:
            return response.json()[endpoint]
        else:
            return [{}]

    def filter(self, employee_id) -> List[dict]:
        """
        Gets an employee's training courses by their id or email
        :param employee_id: the Breathe ID of the employee to lookup
        :return: list of dicts containing the courses
        :raises: ObjectDoesNotExist
        """

        endpoint = "employee_training_courses/" + employee_id
        response = self.client.request("GET", endpoint)
        if requests.codes.ok:
            return response.json()["employee_training_courses"]
        else:
            return [{}]

    def create(self, course: dict) -> Tuple[bool, dict]:
        """
        Creates a new training course
        :param course: A dict representing the course to add. Required keys:
        employee_id, name
        :return: A tuple containing a boolean whether the course was created and a dict containing the reply
        """
        endpoint = "employee_training_courses"
        required_fields = ['employee_id', 'name',]

        for key in required_fields:
            if key not in course:
                raise TypeError("Missing required course field: " + key)

        # See caveats
        course.update({"company_training_type_id": 1})

        response = self.client.request("POST", endpoint, json={endpoint: course})

        if response and requests.codes.ok:
            return True, response.text
        else:
            return False, response.json()

    def count(self) -> int:
        """
        Counts how many courses there are
        :return: int
        """
        return len(self.all())
