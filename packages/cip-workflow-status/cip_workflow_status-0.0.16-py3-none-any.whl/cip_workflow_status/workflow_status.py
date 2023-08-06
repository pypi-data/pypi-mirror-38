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
    TRANSCODED_MEZZANINE_REMOVE = 11
    TRANSCODED = 12
    TRANSCODER_CANCELED = 13
    TRANSCODER_ERROR = 14
    TRANSCODER_PROCESS_FINISHED = 15
    TRANSCODED_COPY_ERROR = 16

    STATUS_TO_STR = [
        'error-ingest',
        'ingest-select-file',
        'ingest-fill-metadata',
        'ingest-copy-storage',
        'ingest-complete',
        'queue-transcoder-new',
        'queue-transcoder-copy',
        'error-transcoder-copy',
        'queue-transcoder',
        'transcoder-transcoding',
        'transcoder-transcoded-copy',
        'transcoder-transcoded-delete',
        'transcoder-transcoded',
        'cancelled-transcoder-canceled',
        'error-transcoder',
        'transcoder-process-finished',
        'error-transcoded-copy'
    ]

    STATUS_TO_FRIENDLY_STR = [
        'ERRO: INGEST',
        'INGESTANDO',
        'INGESTANDO',
        'INGESTANDO',
        'INGESTADO',
        'FILA TRANSCODING',
        'FILA TRANSCODING',
        'ERRO: TRANSCODING',
        'FILA TRANSCODING ',
        'TRANSCODING',
        'TRANSCODING FINALIZANDO',
        'TRANSCODING FINALIZANDO',
        'TRANSCODING FINALIZANDO',
        'TRANSCODING CANCELADO',
        'ERRO: TRANSCODING',
        'TRANSCODER FINALIZADO',
        'ERRO: TRANSCODING'
    ]

    def to_string(self):
        return WorkflowStep.STATUS_TO_STR.value[self.value]

    @staticmethod
    def from_string(status_string):
        return WorkflowStep(WorkflowStep.STATUS_TO_STR.value.index(status_string))

    def to_friendly_string(self):
        return WorkflowStep.STATUS_TO_FRIENDLY_STR.value[self.value]

    @staticmethod
    def string_to_friendly_string(status_string):
        job_status = WorkflowStep.STATUS_TO_STR.value.index(status_string)
        return WorkflowStep.STATUS_TO_FRIENDLY_STR.value[job_status]
