from app.database import Base, SessionLocal, engine
from app.models import Profile, Project, Technology


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Profile).count() > 0:
            print("Banco já possui dados. Seed não executado.")
            return

        profile = Profile(
            name="Ana Desenvolvedora",
            bio="Desenvolvedora backend",
            email="ana@example.com",
            github_url="https://github.com/ana",
            linkedin_url="https://www.linkedin.com/in/ana",
        )
        python = Technology(name="Python")
        fastapi = Technology(name="FastAPI")
        postgres = Technology(name="PostgreSQL")
        db.add_all([profile, python, fastapi, postgres])
        db.flush()

        project = Project(
            title="DevShowcase",
            description="API para divulgação de projetos de desenvolvedores.",
            repository_url="https://github.com/exemplo/devshowcase",
            profile_id=profile.id,
            technologies=[python, fastapi, postgres],
        )
        db.add(project)
        db.commit()
        print("Seed concluído com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
