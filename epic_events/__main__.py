from dotenv import load_dotenv

from epic_events.controllers import cli

if __name__ == '__main__':
    load_dotenv()
    cli()
