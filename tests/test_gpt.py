# STL
import logging

# PDM
import gpt4free
from gpt4free import Provider

LOG = logging.getLogger(__name__)


def test_gpt():
    response = gpt4free.Completion.create(
        Provider.You, prompt="Write a poem on Lionel Messi"
    )
    LOG.info("Response: %s", response)
    assert response != "Unable to fetch the response, Please try again."
