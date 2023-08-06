from attrdict import AttrDict
from mock import MagicMock

from patch_issue.mock_resources.issue import MockIssue


class MockJira(MagicMock):

    DEFAULT_ISSUE = AttrDict({
        "resolution": "UNKNOWN",
        "summary": "UNKNOWN",
        "status": "UNKNOWN",
    })

    def __init__(self, nown_issues=None, *args, **kwargs):
        super(MockJira, self).__init__(*args, **kwargs)
        self.nown_issues = nown_issues if nown_issues is not None else {}

    def issue(self, issue_key):
        issue_details = self.nown_issues.get(issue_key, self.DEFAULT_ISSUE)
        return MockIssue(issue_key, issue_details.resolution,
                         issue_details.summary, issue_details.status)
