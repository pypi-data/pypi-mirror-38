import logging
import colored
from functools import wraps
from contextlib import contextmanager

from .mock_resources import MockJira

RESOLVED_STATUS = "Done"


def get_default_logger():
    default_logger = logging.getLogger("patch_issue")
    default_logger.setLevel(logging.WARNING)

    handler = logging.StreamHandler()
    default_logger.addHandler(handler)
    return default_logger


class JiraPatchIssue(object):
    PATCH_END_MASSAGE = "patch finished: Issue {key}"
    PATCH_DESCRIPTION = "patch description: {description}"
    PATCH_START_MASSAGE = "patch started: {name} ({key}) - {status}"

    RESOLVED_COLOR = "blue"
    UNRESOLVED_COLOR = "light_pink_4"

    ISSUE_KEY = NotImplemented
    DESCRIPTION = ""
    WAY_TO_SOLVE = ""

    def __init__(self, jira=MockJira(), logger=get_default_logger()):
        self.jira = jira
        self.logger = logger

    @classmethod
    def resolved(cls, issue):
        """Returns if given issue has been resolved."""
        resolution = issue.fields.resolution
        status = issue.fields.status.statusCategory.name

        if not resolution:
            return False

        return resolution.name == RESOLVED_STATUS and status == RESOLVED_STATUS

    def start_patch_message(self, status, summary):
        """Returns start patch message.

        Returns:
            str. start patch message.
        """
        return self.PATCH_START_MASSAGE.format(key=self.ISSUE_KEY,
                                               name=summary,
                                               status=status)

    @property
    def end_patch_message(self):
        """Returns end patch message.

        Returns:
            str. start patch message.
        """
        return self.PATCH_END_MASSAGE.format(key=self.ISSUE_KEY)

    @property
    def description_message(self):
        """Returns description message.

        Returns:
             str. description message.
        """
        return self.PATCH_DESCRIPTION.format(description=self.DESCRIPTION)

    def styled_message(self, message, is_resolved):
        """Returns style depends on issue resolution.

        Attributes:
            message (str): message to style.
            is_resolved (bool): True if the issue is resolved
        """
        color = self.RESOLVED_COLOR if is_resolved else self.UNRESOLVED_COLOR
        style = colored.fg(color) + colored.attr("bold")

        return colored.stylize(message, style)

    def log(self, message, is_resolved):
        """Write to logger styled message depends on issue resolution."""
        styled_message = self.styled_message(message=message,
                                             is_resolved=is_resolved)
        self.logger.warning(styled_message)

    def __str__(self):
        issue = self.jira.issue(self.ISSUE_KEY)
        summary = issue.fields.summary
        is_resolved = self.resolved(issue)
        status = issue.fields.status.statusCategory.name
        pattern = "Issue {key}: {name} - {status}"

        return self.styled_message(pattern.format(key=self.ISSUE_KEY,
                                                  name=summary,
                                                  status=status), is_resolved)

    @property
    @contextmanager
    def patch(self):
        issue = self.jira.issue(self.ISSUE_KEY)
        is_resolved = self.resolved(issue)
        summary = issue.fields.summary
        status = issue.fields.status.statusCategory.name

        self.log(message=self.start_patch_message(status, summary),
                 is_resolved=is_resolved)

        if self.DESCRIPTION:
            self.log(message=self.description_message, is_resolved=is_resolved)

        if self.WAY_TO_SOLVE and is_resolved:
            self.log(message=self.WAY_TO_SOLVE, is_resolved=is_resolved)

        yield

        self.log(message=self.end_patch_message, is_resolved=is_resolved)

    def patch_function(self, func):
        """Decorator to apply patch over given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.patch:
                return func(*args, **kwargs)

        return wrapper
