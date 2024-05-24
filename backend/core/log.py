import logging


# logging.basicConfig(
#     level=logging.INFO,
#     format="[{asctime}] #{levelname:8} {filename}: {lineno} - {name} - {message}",
#     style="{",
# )

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] #{levelname:8} {filename}:{lineno}:{funcName} - {name} - {message}",
    style="{",
)
