import unittest

from fastapi import status


class ApiRefactorTest(unittest.TestCase):
    def test_target_modules_are_importable(self):
        import app.database.storage  # noqa: F401
        import app.models.schemas  # noqa: F401
        import app.routes.test_routes  # noqa: F401
        import app.routes.url_routes  # noqa: F401
        import app.services.shortener_service  # noqa: F401
        import app.utils.generator  # noqa: F401

    def test_helper_routes_keep_existing_responses(self):
        from app.routes.test_routes import about, create_user, greet, health, hello, home, square
        from app.models.schemas import User

        self.assertEqual(home(), {"message": "welcome to url shortener"})
        self.assertEqual(
            about(),
            {
                "project": "URL Shortener API",
                "developer": "Prashant",
                "status": "Learning FastAPI",
            },
        )
        self.assertEqual(health(), {"status": "Healthy"})
        self.assertEqual(greet(), {"message": "Hello, Guest!"})
        self.assertEqual(greet("Prashant"), {"message": "Hello, Prashant!"})
        self.assertEqual(square(5), {"number": 5, "square": 25})
        self.assertEqual(hello("Alex"), {"message": "hello Alex"})
        self.assertEqual(
            create_user(User(name="Prashant")),
            {"message": "User 'Prashant' created successfully"},
        )

    def test_url_shortener_routes_keep_existing_behavior(self):
        from app.database.storage import url_database
        from app.models.schemas import ShortenURLRequest
        from app.routes.url_routes import create_short_url, redirect_to_original_url

        url_database.clear()

        response = create_short_url(
            ShortenURLRequest(url="https://example.com/page", custom_alias="example")
        )
        self.assertEqual(str(response["original_url"]), "https://example.com/page")
        self.assertEqual(response["short_url"], "http://localhost:8000/example")

        with self.assertRaises(Exception) as duplicate_context:
            create_short_url(
                ShortenURLRequest(url="https://example.com/other", custom_alias="example")
            )
        self.assertEqual(duplicate_context.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(duplicate_context.exception.detail, "Custom alias already exists")

        redirect_response = redirect_to_original_url("example")
        self.assertEqual(
            redirect_response.status_code,
            status.HTTP_307_TEMPORARY_REDIRECT,
        )
        self.assertEqual(redirect_response.headers["location"], "https://example.com/page")

        with self.assertRaises(Exception) as missing_context:
            redirect_to_original_url("missing-code")
        self.assertEqual(missing_context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(missing_context.exception.detail, "Short URL not found")

    def test_main_registers_all_expected_routes(self):
        from app.main import app

        routes = {(route.path, next(iter(route.methods))) for route in app.routes if route.methods}
        self.assertIn(("/", "GET"), routes)
        self.assertIn(("/about", "GET"), routes)
        self.assertIn(("/health", "GET"), routes)
        self.assertIn(("/greet", "GET"), routes)
        self.assertIn(("/square/{number}", "GET"), routes)
        self.assertIn(("/hello/{name}", "GET"), routes)
        self.assertIn(("/user", "POST"), routes)
        self.assertIn(("/shorten", "POST"), routes)
        self.assertIn(("/{short_code}", "GET"), routes)


if __name__ == "__main__":
    unittest.main()
