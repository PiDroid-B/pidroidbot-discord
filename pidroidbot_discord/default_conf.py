DEFAULT_CONFIG = """---

log:
  version: 1
  disable_existing_loggers: false
  formatters:
    full:
      format: '%(asctime)s %(name)-20s %(levelname)-8s %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
  handlers:
    stderr:
      class: logging.StreamHandler
      stream: ext://sys.stderr
      level: WARNING
      formatter: full
    stderr_file:
      class : logging.handlers.RotatingFileHandler
      filename: ../log/logconfig.log
      maxBytes: 1024000
      backupCount: 3
      level: INFO
      formatter: full
    stdout:
      class: logging.StreamHandler
      stream: ext://sys.stdout
      level: DEBUG
      formatter: full
  loggers:
    main:
      level: DEBUG
      handlers: [stdout,stderr_file]
    plugins:
      level: DEBUG
      handlers: [stdout,stderr_file]
cogs:
  list_ignore: []
bot:
  prefix: "."
  token: "YOUR_TOKEN"
debug:
  what_i_see: False
lang: 'en_UK'
git:
  url: "https://github.com/PiDroid-B/BotMarkdownForDiscord"


"""
