import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker

from students.models import Course


# -------------------------
# FIXTURES
# -------------------------

@pytest.fixture
def api_client():
    """Фикстура для DRF API клиента."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов."""
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов."""
    from students.models import Student
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory


# -------------------------
# TESTS
# -------------------------

@pytest.mark.django_db
def test_get_single_course(api_client, course_factory):
    """Проверка получения одного курса (retrieve)."""
    course = course_factory(name="Python 101")

    url = reverse("courses-detail", args=[course.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == course.id
    assert data["name"] == course.name


@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    """Проверка получения списка курсов (list)."""
    courses = course_factory(_quantity=3)

    url = reverse("courses-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(courses)
    returned_ids = {c["id"] for c in data}
    expected_ids = {c.id for c in courses}
    assert returned_ids == expected_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации курсов по id."""
    courses = course_factory(_quantity=5)
    target = courses[2]

    url = reverse("courses-list")
    response = api_client.get(url, data={"id": target.id})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == target.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации курсов по name."""
    course_factory(name="Python Base")
    target = course_factory(name="Django Pro")

    url = reverse("courses-list")
    response = api_client.get(url, data={"name": target.name})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == target.name


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    url = reverse("courses-list")
    payload = {"name": "New Course"}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert Course.objects.filter(name="New Course").exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса."""
    course = course_factory(name="Old Name")
    url = reverse("courses-detail", args=[course.id])
    payload = {"name": "Updated Name"}

    response = api_client.patch(url, data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]
    course.refresh_from_db()
    assert course.name == payload["name"]


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса."""
    course = course_factory()
    url = reverse("courses-detail", args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()