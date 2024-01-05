import logging

logging.basicConfig(
    filename='er_edf_stack_resource.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s: %(message)s',
)

logger = logging.getLogger(__name__)
