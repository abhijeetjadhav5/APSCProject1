
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from pathlib import Path

# Database file stored in the same folder as main.py
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "registration.db"


# Create the database table automatically
def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                aadhar TEXT,
                name TEXT,
                validate TEXT,
                gender TEXT,
                contact TEXT,
                address TEXT,
                dob TEXT
            )
        """)

    print("Database and table are ready.")


class MyServer(BaseHTTPRequestHandler):

    # Add CORS headers for browser requests
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers", "Content-Type"
        )

    # Test the backend in a browser
    def do_GET(self):
        if self.path in ("/", "/health"):
            body = json.dumps({
                "status": "success",
                "message": "Backend is running successfully!"
            }).encode("utf-8")

            self.send_response(200)
            self.send_cors_headers()
            self.send_header(
                "Content-Type", "application/json; charset=utf-8"
            )
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_json(404, {"error": "Endpoint not found"})

    # Handle browser CORS preflight requests
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    # Register a new user
    def do_POST(self):
        if self.path != "/api/register":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0:
                self.send_json(400, {"error": "Empty request body"})
                return

            raw_data = self.rfile.read(length)
            data = json.loads(raw_data.decode("utf-8"))

            required_fields = [
                "role",
                "aadhar",
                "name",
                "validate",
                "gender",
                "contact",
                "address",
                "dob"
            ]

            # Validate required fields
            for field in required_fields:
                if field not in data:
                    self.send_json(
                        400,
                        {"error": f"Missing field: {field}"}
                    )
                    return

            # Save registration in SQLite
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("""
                    INSERT INTO registrations
                    (role, aadhar, name, validate, gender,
                     contact, address, dob)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(str(data[field]) for field in required_fields))

            print("Registration saved successfully.")

            self.send_json(
                200,
                {"message": "Registration successful!"}
            )

        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "Invalid JSON data"})

        except sqlite3.Error as error:
            print("SQLite error:", repr(error))
            self.send_json(
                500,
                {"error": "Database error. Check the Python terminal."}
            )

        except Exception as error:
            print("Unexpected error:", repr(error))
            self.send_json(500, {"error": "Internal server error"})

    # Send JSON responses
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_cors_headers()
        self.send_header(
            "Content-Type", "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    create_table()

    # Listen only on this computer
    server = HTTPServer(("127.0.0.1", 8096), MyServer)

    print("Backend running at http://127.0.0.1:8096")
    print("Health check: http://127.0.0.1:8096/health")
    print(f"Database location: {DB_PATH}")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBackend stopped.")
    finally:
        server.server_close()
