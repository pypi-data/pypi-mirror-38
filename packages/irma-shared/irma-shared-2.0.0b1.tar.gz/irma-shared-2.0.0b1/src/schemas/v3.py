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


from marshmallow import Schema, fields, post_load
from .base import (
    FileSchema,
    FileExt,
    FileCli,
    FileKiosk,
    FileProbeResult,
    FileSuricata,
    Scan,
    ScanSchema,
    ScanRetrievalCode,
)


__all__ = (
    'FileExtSchema',
    'FileCliSchema',
    'FileKioskSchema',
    'FileProbeResultSchema',
    'FileSuricataSchema',
    'FileResultSchema',
    'Paginated',
    'ScanSchema',
    'ScanRetrievalCodeSchema',
    'SRScanSchema',
)


# {{{ PAGINATED

class Paginated(type):
    def __new__(_, enclosed, **extra):
        class Page(Schema):
            offset = fields.Integer()
            limit = fields.Integer()
            total = fields.Integer()
            items = fields.Nested(enclosed, many=True, **extra)
            # NOTE: APIv3 no longer use the 'data' field

            @post_load
            def make_object(self, data):
                return data

        return Page

# }}}


# {{{ FILEEXT

class FileExtSchema(Schema):

    @classmethod
    def dynschema(cls, data):
        """ Dynamically retrieve required schema
        :param data: data to unmarshall
        :returns: the required schema class
        """
        try:
            submitter = data["submitter"]
            if submitter == FileCli.submitter_type:
                return FileCliSchema
            if submitter == FileKiosk.submitter_type:
                return FileKioskSchema
            if submitter == FileProbeResult.submitter_type:
                return FileProbeResultSchema
            if submitter == FileSuricata.submitter_type:
                return FileSuricataSchema
            return cls
        except KeyError:
            return cls

    id = fields.UUID(attribute="external_id")
    status = fields.Integer(allow_none=True)
    name = fields.String()

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    file = fields.Nested(FileSchema)
    scan = fields.Nested(ScanSchema, allow_none=True, only=('id', 'date'))

    parent_file_sha256 = fields.Pluck(
            FileSchema, 'sha256', attribute="parent", allow_none=True)

    submitter = fields.String()

    other_results = fields.Nested(
        'self', only=("id", "scan", "status"), many=True)

    probe_results = fields.Function(
            lambda fe, ctx: fe.get_probe_results(ctx.get('formatted', True)),
            lambda dct: dct)

    @post_load
    def make_object(self, data):
        return FileExt(**data)


class FileCliSchema(FileExtSchema):
    path = fields.String()


class FileKioskSchema(FileCliSchema):
    submitter_id = fields.String()


class FileProbeResultSchema(FileExtSchema):
    probe_parent = fields.Nested(
        'ProbeResultSchema',
        attribute="probe_result_parent",
        only=('type', 'name', 'status',)
    )


class FileSuricataSchema(FileExtSchema):
    context = fields.Dict()

# }}}


# {{{ FILERESULT

class FileResultSchema(Paginated(
        FileExtSchema,
        exclude=('probe_results', 'files_infos', 'other_results'))):
    file_infos = fields.Nested(FileSchema)

    @post_load
    def make_object(self, data):
        return data

# }}}


# {{{ SRCODE

class SRFileCliSchema(FileCliSchema):
    size = fields.Pluck(FileSchema, 'size', dump_only=True, attribute="file")


class SRScanSchema(Schema):
    id = fields.UUID(attribute="external_id")
    date = fields.Number()
    status = fields.Integer(allow_none=True)

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    results = fields.Nested(
        SRFileCliSchema,
        attribute="files_ext",
        many=True,
        only=('id', 'name', 'size', 'path', 'status')
    )

    @post_load
    def make_object(self, data):
        return Scan(**data)


class ScanRetrievalCodeSchema(Schema):
    id = fields.String(attribute="external_id")

    @post_load
    def make_object(self, data):
        return ScanRetrievalCode(**data)

# }}}
