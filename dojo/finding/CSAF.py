import json
import os.path
from datetime import datetime
from dojo.models import Finding
from uuid import uuid4


class RevisionHistory:
    def __init__(self, date, number, summary):
        self.date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        self.number = number
        self.summary = summary


class Tracking:
    def __init__(self, current_release_date, id, initial_release_date, revision_history, status, version):
        self.current_release_date = current_release_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        self.id = id
        self.initial_release_date = initial_release_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        self.revision_history = revision_history
        self.status = status
        self.version = version


class Publisher:
    def __init__(self, category, name, namespace):
        self.category = category
        self.name = name
        self.namespace = namespace


class CSAF:
    def __init__(self, category, csaf_version, publisher, title, tracking):
        self.category = category
        self.csaf_version = csaf_version
        self.publisher = publisher.__dict__
        self.title = title
        self.tracking = tracking.__dict__
        


def generateCSAF(finding: Finding):
    revision = [RevisionHistory(datetime.now(), "1", finding.description).__dict__]
    tracking = Tracking(datetime.now(), uuid4().__str__(), finding.date, revision, "draft", "1")
    publisher = Publisher("discoverer", finding.reporter.get_full_name(), "https://placeholder.com")
    c = CSAF("csaf_base", "2.0", publisher, finding.title, tracking)
    print(c.__str__)
    return json.dumps({"document": c.__dict__}, indent=4)
    
