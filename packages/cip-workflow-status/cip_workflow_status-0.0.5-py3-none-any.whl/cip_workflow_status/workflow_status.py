from enum import Enum


class WorkflowStep(Enum):
    INGEST_ERROR = 0
    SELECT_FILE = 1
    FILL_METADATA = 2
    COPY_INGEST_STORAGE = 3
    INGESTED = 4
    TRANSCODER_NEW = 5
    TRANSCODER_COPY = 6
    TRANSCODER_COPY_ERROR = 7
    TRANSCODER_QUEUE = 8
    TRANSCODING = 9
    TRANSCODED_COPY = 10
    TRANSCODED = 11
    TRANSCODER_CANCELED = 12
    TRANSCODER_ERROR = 13

    STATUS_TO_STR = [
        'error-ingest',
        'select-file',
        'fill-metadata',
        'copy-ingest-storage',
        'ingested',
        'transcoder-new',
        'transcoder-copy',
        'error-transcoder',
        'transcoder-queue',
        'transcoder-transcoding',
        'transcoder-transcoded-copy',
        'transcoder-transcoded',
        'transcoder-canceled',
        'error-transcoder'
    ]

    STATUS_TO_FRIENDLY_SRT = [
        'ERRO: INGEST',
        'INGESTANDO',
        'INGESTANDO',
        'INGESTANDO',
        'INGESTADO',
        'FILA TRANSCODING',
        'FILA TRANSCODING',
        'FILA TRANSCODING',
        'FILA TRANSCODING',
        'TRANSCODING',
        'TRANSCODING',
        'TRANSCODING FINALIZADO',
        'TRANSCODING CANCELADO',
        'ERRO: TRANSCODING'
    ]

    def to_string(self):
        return WorkflowStep.STATUS_TO_STR.value[self.value]

    @staticmethod
    def from_string(status_string):
        return WorkflowStep(WorkflowStep.STATUS_TO_STR.value.index(status_string))

    def to_friendly_string(self):
        return WorkflowStep.STATUS_TO_FRIENDLY_SRT.value[self.value]

    @staticmethod
    def string_to_friendly_string(status_string):
        job_status = WorkflowStep.STATUS_TO_STR.value.index(status_string)
        return WorkflowStep.STATUS_TO_FRIENDLY_SRT.value[job_status]
