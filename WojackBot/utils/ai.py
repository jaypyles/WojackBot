# PDM
import g4f


async def call_ai(prompt: str):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.Bing,
        )
        return response

    except Exception as e:
        print(e)
