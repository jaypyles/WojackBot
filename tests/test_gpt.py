# PDM
import gpt4free
from gpt4free import Provider


def test_gpt():
    # usage You
    response = gpt4free.Completion.create(
        Provider.You, prompt="Write a poem on Lionel Messi"
    )
    assert response != "Unable to fetch the response, Please try again."
