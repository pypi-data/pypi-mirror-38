from mock import MagicMock
from attrdict import AttrDict
from property_manager import cached_property


class MockIssue(MagicMock):
    def __init__(self, issue_key, resolution, summary, status,
                 *args, **kwargs):
        super(MockIssue, self).__init__(*args, **kwargs)
        self.issue_key = issue_key
        self.resolution = resolution
        self.summary = summary
        self.status = status

    @cached_property
    def fields(self):
        resolution = AttrDict({"name": self.resolution})
        status = AttrDict({"statusCategory": {"name": self.status}})

        return AttrDict({
            "resolution": resolution,
            "summary": self.summary,
            "status": status
        })
