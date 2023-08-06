#
# Copyright (c) 2013-2018 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

import datetime

from marshmallow import fields, Schema, post_load

from ..csts import IrmaScanStatus as ScanStatus

__all__ = (
    'apiid',
    'FileSchema',
    'ProbeResultSchema',
    'ScanSchema',
    'TagSchema',
)


# {{{ TAG

class TagSchema(Schema):
    id = fields.Integer()
    text = fields.String()

    @post_load
    def make_object(self, data):
        return Tag(**data)


class Tag:

    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return "Tag." + str(self.id)

    def __str__(self):
        return "Tag{" + "id: {}; text: {}; ".format(self.id, self.text) + "}"

    def __eq__(self, other):
        return (isinstance(other, Tag)
                and self.id == other.id
                and self.text == other.text)

    def __neq__(self, other):
        return not (self == other)

# }}}


# {{{ FILE

class FileSchema(Schema):
    size = fields.Integer()
    # we could create our own fields for hashes
    sha256 = fields.String()
    sha1 = fields.String()
    md5 = fields.String()

    timestamp_first_scan = fields.Number()
    timestamp_last_scan = fields.Number()
    mimetype = fields.String()
    tags = fields.Nested(TagSchema, many=True)

    @post_load
    def make_object(self, data):
        return File(**data)


class File:

    def __init__(
            self, sha256, *, size=None, sha1=None, md5=None,
            timestamp_first_scan=None, timestamp_last_scan=None,
            mimetype=None, tags=None):
        self.sha256 = sha256
        self.size = size
        self.sha1 = sha1
        self.md5 = md5

        self.timestamp_first_scan = timestamp_first_scan
        self.timestamp_last_scan = timestamp_last_scan

        self.mimetype = mimetype
        self.tags = tags or []

    @property
    def id(self):
        return self.sha256

    @property
    def pdate_first_scan(self):
        try:
            return timestamp_to_date(self.timestamp_first_scan)
        except TypeError:
            return None

    @property
    def pdate_last_scan(self):
        try:
            return timestamp_to_date(self.timestamp_last_scan)
        except TypeError:
            return None

    def __repr__(self):
        return "File." + self.id

    def __str__(self):
        ret = "File{"
        ret += "sha256: {}; ".format(self.sha256)
        # Do not display sha1 and md5 that are just noise in this context
        ret += "tags: [" + " ".join(t.text for t in self.tags) + "]; "
        if self.size is not None:
            ret += "size: {}; ".format(self.size)
        if self.timestamp_first_scan:
            ret += "first scan: {}; ".format(self.pdate_first_scan)
        if self.timestamp_last_scan:
            ret += "last scan: {0}; ".format(self.pdate_last_scan)
        if self.mimetype:
            ret += "mimetype: {0}; ".format(self.mimetype)
        ret += "}"
        return ret

    def __eq__(self, other):
        return isinstance(other, File) and self.id == other.id

    def __neq__(self, other):
        return not (self == other)

# }}}


# {{{ SCAN

class ScanSchema(Schema):
    id = fields.UUID(attribute="external_id")
    date = fields.Number()
    # date = fields.Date()
    status = fields.Integer(allow_none=True)

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    force = fields.Boolean()
    resubmit_files = fields.Boolean()
    mimetype_filtering = fields.Boolean()

    @post_load
    def make_object(self, data):
        return Scan(**data)


class Scan:

    def __init__(
            self, external_id, *, date=None, status=None,
            probes_finished=None, probes_total=None,
            force=None, resubmit_files=None, mimetype_filtering=None,
            files_ext=None):
        self.external_id = str(external_id)
        self.date = date
        self.status = status

        self.probes_finished = probes_finished
        self.probes_total = probes_total

        self.force = force
        self.resubmit_files = resubmit_files
        self.mimetype_filtering = mimetype_filtering

        self.files_ext = files_ext

    def is_launched(self):
        return self.status == ScanStatus.launched

    def is_finished(self):
        return self.status == ScanStatus.finished

    @property
    def pstatus(self):
        return ScanStatus.label[self.status]

    @property
    def pdate(self):
        return timestamp_to_date(self.date)

    @property
    def id(self):
        return self.external_id

    def __repr__(self):
        return "Scan." + self.id

    def __str__(self):
        ret = "Scan{"
        ret += "id: {}; ".format(self.id)
        ret += "date: {}; ".format(self.pdate)
        ret += "status: {}; ".format(self.pstatus)
        if self.probes_total:
            ret += "probes progress: {}/{}; ".format(
                    self.probes_finished, self.probes_total)
        if self.files_ext is not None:
            ret += "files_ext: {}; ".format(self.files_ext)

        options = []
        if self.force:
            options.append("force")
        if self.mimetype_filtering:
            options.append("mime_filter")
        if self.resubmit_files:
            options.append("resubmit")
        if options:
            ret += "options: [" + " ".join(options) + "]; "
        ret += "}"
        return ret

    def __eq__(self, other):
        return isinstance(other, Scan) and self.id == other.id

    def __neq__(self, other):
        return not (self == other)

# }}}


# {{{ PROBERESULT

# TODO: check real schema
class ProbeResultSchema(Schema):
    type = fields.String()
    plateform = fields.String()
    version = fields.String()

    status = fields.Integer()
    duration = fields.Float()

    error = fields.String(allow_none=True)
    results = fields.Field()

# }}}


# {{{ FILEEXT

class FileExt:
    submitter_type = "whatever"

    def __init__(
            self, external_id, *, status=None, name=None,
            probes_finished=None, probes_total=None,
            file=None, scan=None, parent=None,
            submitter=None,
            probe_results=None, other_results=None):
        self.external_id = str(external_id)
        self.name = name
        self.status = status

        self.probes_finished = probes_finished
        self.probes_total = probes_total

        self.scan = scan
        self.file = file
        self.parent = parent

        self.submitter = submitter
        self.probe_results = probe_results
        self.other_results = other_results

    @property
    def id(self):
        return self.external_id

    @property
    def pscan_date(self):
        return timestamp_to_date(self.scan.date)

    def __repr__(self):
        return "FileExt." + self.id

    def __str__(self):
        ret = "FileExt{"
        ret += "id: {}; ".format(self.id)
        ret += "status: {}; ".format(self.status)
        ret += "scan: {}; ".format(self.scan)
        if self.probes_total:
            ret += "probes progress: {}/{}; ".format(
                self.probes_finished, self.probes_total)
        if self.name:
            ret += "filename: {}; ".format(self.name)
        if self.file is not None:
            ret += "file: {}; ".format(self.file)
        if self.parent:
            ret += "parent: {}; ".format(self.parent)
        if self.probe_results:
            ret += "results: {}; ".format(self.probe_results)
        ret += "}"
        return ret

    def __eq__(self, other):
        return isinstance(other, FileExt) and self.id == other.id

    def __neq__(self, other):
        return not (self == other)


class FileCli(FileExt):
    submitter_type = "cli"

    def __init__(self, *args, path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path


class FileKiosk(FileCli):
    submitter_type = "kiosk"

    def __init__(self, *args, submitter_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitter_id = submitter_id


class FileProbeResult(FileExt):
    submitter_type = "probe_result"

    def __init__(self, *args, probe_parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.probe_parent = probe_parent


class FileSuricata(FileExt):
    submitter_type = "suricata"

    def __init__(self, *args, context=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

# }}}


# {{{ SRCODE

class ScanRetrievalCode:

    def __init__(self, external_id):
        self.external_id = external_id

    @property
    def id(self):
        return self.external_id

    def __eq__(self, other):
        return isinstance(other, ScanRetrievalCode) and self.id == other.id

    def __neq__(self, other):
        return not (self == other)

# }}}


# {{{ HELPERS

def apiid(obj):  # pragma: no cover
    if isinstance(obj, (Tag, File, FileExt, Scan, ScanRetrievalCode)):
        return obj.id
    else:
        return obj


def timestamp_to_date(timestamp):
    if timestamp is None:
        return None
    date = datetime.datetime.fromtimestamp(int(timestamp))
    return date.strftime('%Y-%m-%d %H:%M:%S')

# }}}
