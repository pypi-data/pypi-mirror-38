import colored
from functools import wraps
from contextlib import contextmanager

from jira import JIRA


class JiraPatchIssue(object):
    PATCH_END_MASSAGE = "patch finished: Issue {key}"
    PATCH_DESCRIPTION = "patch description: {description}"
    PATCH_START_MASSAGE = "patch started: {name} ({key}) - {status}"

    RESOLVED_COLOR = "blue"
    UNRESOLVED_COLOR = "light_pink_4"

    ISSUE_KEY = NotImplemented
    DESCRIPTION = ""

    def __init__(self, host, oauth_dict, logger, resolved_color=RESOLVED_COLOR,
                 unresolved_color=UNRESOLVED_COLOR):
        self.jira_manager = JIRA(host, oauth=oauth_dict)
        self.logger = logger
        self.resolved_color = resolved_color
        self.unresolved_color = unresolved_color

    @classmethod
    def resolved(cls, issue):
        """Returns if given issue has been resolved."""
        resolution = issue.fields.resolution

        if not resolution:
            return False

        return resolution.name == "Done"

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
        color = self.resolved_color if is_resolved else self.unresolved_color
        style = colored.fg(color) + colored.attr("bold")

        return colored.stylize(message, style)

    def log(self, message, is_resolved):
        """Write to logger styled message depends on issue resolution."""
        styled_message = self.styled_message(message=message,
                                             is_resolved=is_resolved)
        self.logger.warning(styled_message)

    @property
    @contextmanager
    def patch(self):
        issue = self.jira_manager.issue(self.ISSUE_KEY)
        is_resolved = self.resolved(issue)
        summary = issue.fields.summary
        status = issue.fields.status.statusCategory.name

        self.log(message=self.start_patch_message(status, summary),
                 is_resolved=is_resolved)

        if self.DESCRIPTION:
            self.log(message=self.description_message, is_resolved=is_resolved)

        yield

        self.log(message=self.end_patch_message, is_resolved=is_resolved)

    def patch_function(self, func):
        """Decorator to apply patch over given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.patch:
                return func(*args, **kwargs)

        return wrapper
