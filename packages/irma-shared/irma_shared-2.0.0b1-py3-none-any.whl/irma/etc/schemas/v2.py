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


from marshmallow import Schema, fields, pre_load, post_load
from .schemas import (
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
            # NOTE: IRMA API is non consistent about the field it puts its
            # results in. This behavior has been removed in v3
            data = fields.Nested(enclosed, many=True, **extra)
            items = fields.Nested(enclosed, many=True, **extra)

            @post_load
            def make_object(self, data):
                return data

        return Page

# }}}


# {{{ SCAN

class ScanSchema(ScanSchema):
    results = fields.Nested(
        'irma.shared.schemas.v2.FileExtSchema',
        many=True,
        attribute="files_ext",
        exclude=('probe_results', 'file_infos', 'other_results')
    )

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

    file = fields.Nested(FileSchema, load_only=True)
    file_infos = fields.Nested(
            FileSchema, attribute="file", dump_only=True)
    file_sha256 = fields.Pluck(
            FileSchema, 'sha256', dump_only=True, attribute="file")

    scan = fields.Nested(ScanSchema, load_only=True, allow_none=True)
    scan_id = fields.Pluck(
            ScanSchema, 'id', attribute='scan', dump_only=True)
    scan_date = fields.Pluck(
            ScanSchema, 'date', attribute='scan', dump_only=True)

    parent_file_sha256 = fields.Pluck(
            FileSchema, 'sha256', attribute="parent", allow_none=True)

    submitter = fields.String()

    other_results = fields.Nested(
        'self', many=True,
        only=("id", "scan", "scan_id", "scan_date", "file", "file_sha256",
              "status"))

    probe_results = fields.Function(
            lambda fe, ctx: fe.get_probe_results(ctx.get('formatted', True)),
            lambda dct: dct)

    @post_load
    def make_object(self, data):
        return FileExt(**data)

    @pre_load
    def merge_scan_fields(self, data):
        try:
            scanid = data.pop('scan_id', None)
            if scanid is None:
                del data['scan_date']
            else:
                data['scan'] = {'id': scanid}
                data['scan']['date'] = data.pop('scan_date')
        except KeyError:
            pass
        return data

    @pre_load
    def merge_file_fields(self, data):
        try:
            data['file'] = {'sha256': data.pop('file_sha256')}

            try:
                data['file']['size'] = data.pop('size')
            except KeyError:
                pass

            try:
                data['file'].update(data.pop('file_infos'))
            except KeyError:
                pass

        except KeyError:
            pass
        return data


class FileCliSchema(FileExtSchema):
    path = fields.String()

    @post_load
    def make_object(self, data):
        return FileCli(**data)


class FileKioskSchema(FileCliSchema):
    submitter_id = fields.String()

    @post_load
    def make_object(self, data):
        return FileKiosk(**data)


class FileProbeResultSchema(FileExtSchema):
    probe_parent = fields.Nested(
        'ProbeResultSchema',
        attribute="probe_result_parent",
        only=('type', 'name', 'status',)
    )

    @post_load
    def make_object(self, data):
        return FileProbeResult(**data)


class FileSuricataSchema(FileExtSchema):
    context = fields.Dict()

    @post_load
    def make_object(self, data):
        return FileSuricata(**data)

# }}}


# {{{ FILERESULT

class FileResultSchema(Paginated(
        FileExtSchema,
        exclude=('probe_results', 'files_infos'))):
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
        only=(
            'id',
            'status',
            'name',
            'path',
            'file', 'file_sha256', 'size',
        )
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
