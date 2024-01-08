from openai import OpenAI
import requests
from json import JSONDecodeError
from typing import Literal
import os
from dotenv import load_dotenv
load_dotenv()

# Enter your own valid API Key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def talk_to_gpt_model(base_context: str, prompt: str, model: str = "gpt-4"):
    try:
        completion = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": base_context + " [json]"},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Exception catching for any status not 200.
        if completion["http_status"] == 200:
            return completion["choices"][0]["message"]["content"]
        else:
            raise Exception(f"unexpected response status: {completion['http_status']}")

        # return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def talk_to_dal_e_3(
        prompt: str, model: str = "dall-e-3", number_of_images:int = 1,
        size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024"):
    response_url = ""

    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            n=number_of_images,
            size=size
        )
        print(response.data[0].url)
        response_url = response.data[0].url
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        # Handle specific HTTP errors

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        # Handle connection errors

    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
        # Handle timeouts

    except JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        # Handle JSON parsing errors

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle any other exceptions

    finally:
        return response_url

def main():
    base_content = "enter your base content here"
    user_prompt = "enter your prompt here"

    try:
        result = talk_to_gpt_model(base_content, user_prompt)
    except Exception as e:
            print(f'Error has occurred: {str(e)}')

if __name__ == "__main__":
    main()
    
