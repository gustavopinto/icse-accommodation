from dotenv import load_dotenv

load_dotenv()

from app import create_app, db  # noqa: E402
from app.models import User, AccommodationRequest  # noqa: F401, E402

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "AccommodationRequest": AccommodationRequest}


if __name__ == "__main__":
    app.run()
