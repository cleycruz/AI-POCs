import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.core.config import settings

def setup_telemetry():
    logger = logging.getLogger(__name__)
    # Conectamos con el Instrumentation Key de Azure
    logger.addHandler(AzureLogHandler(
        connection_string=f'InstrumentationKey={settings.APPINSIGHTS_KEY}')
    )
    logger.setLevel(logging.INFO)
    return logger