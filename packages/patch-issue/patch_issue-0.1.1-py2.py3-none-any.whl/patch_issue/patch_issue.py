import colored
from contextlib import contextmanager

from jira import JIRA
from .default_logger import get_logger


default_logger = get_logger()
default_jira_manager = JIRA("https://panager.atlassian.net/", auth=("ronenya4321@gmail.com", "12345678"))


@contextmanager
def patch(jira_issue, logger=default_logger, description="",
          jira_manager=default_jira_manager):
    issue = jira_manager.issue(jira_issue)
    resolution = issue.fields.resolution
    resolved = resolution is not None and resolution.name == "Done"

    color = "blue" if resolved else "light_pink_4"
    style = colored.fg(color) + colored.attr("bold")

    logger.warning(
        colored.stylize("patch started: {name} ({key}) - {status}".format(
            key=jira_issue,
            name=issue.fields.summary, status=issue.fields.status.statusCategory.name), style))

    if description:
        logger.warning(colored.stylize("patch description: {description}".format(
            description=description), style))

    yield

    logger.warning(colored.stylize("patch finished: Issue {key}".format(
        key=jira_issue), style))


def patch_function(jira_issue, logger=default_logger, description="",
                   jira_manager=default_jira_manager):
    def new_func(func):
        def wrapper(*args, **kwargs):
            with patch(jira_issue, logger, description,jira_manager):
                return func(*args, **kwargs)

        return wrapper
    return new_func
