"""
Test Gemini on first 5 items using its own PDF processing engine
"""

from dotenv import dotenv_values
import requests, json #, sys
import base64
from pathlib import Path


model_id = "google/gemini-3.8-flash"
prompt_id = "001"
test_id = f"{prompt_id}-native"
#query_range_start = int(sys.argv[1])
#query_range_stop = int(sys.argv[2])

env = dotenv_values(".env")
api_key = env["OPENROUTER_API_KEY"]
url = "https://openrouter.ai/api/v1/responses"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Load test set
oup = "model_outputs/gemini_tests.json"
with open(oup, "r") as f:
    test_data = json.load(f)
n_items = len(test_data)
print(f"Test set read from {oup} (n={n_items})")

# Load prompt
inp = f"prompt_{prompt_id}.txt"
with open(inp, "r") as f:
    user_text = f.read()
print(f"Prompt read from {inp}")


def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')


def query_answer(i):
    item = test_data[i]

    ## Skip items already tested
    #if len(item["test_results"]) > 0:
    #    return None

    # Encode pdf
    pdf_path = f"../attachments/{item['opp_id']}.pdf"
    base64_pdf = encode_pdf_to_base64(pdf_path)
    data_url = f"data:application/pdf;base64,{base64_pdf}"

    # Prepare input
    input_items = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": user_text
                },
                {
                    "type": "input_file",
                    "filename": "document.pdf",
                    "file_data": data_url
                },
            ]
        }
    ]
    
    # Configure PDF processing engine
    plugins = [
        {
            "id": "file-parser",
            "pdf": {
                "engine": "native"
            }
        }
    ]
    
    payload = {
        "model": model_id,
        "input": input_items,
        "plugins": plugins,
        #"max_tokens": 6000
    }
    
    print("Calling model ...", end="")
    response = requests.post(url, headers=headers, json=payload)
    print(".")
    return response.json()



# Loop through items
#query_range = range(query_range_start, min(query_range_stop, n_items))
print("Model ID:", model_id)
print("Test ID:", test_id)
print("Prompt:", user_text, sep="\n", flush=True)
for i in range(5):
    print(f"\n\nTrial {i}", flush=True) 
    re = query_answer(i)

    if re is None:
        print("Skipped")
        continue

    # Display some model outputs
    usage = re["usage"]
    output_text = re["output"][1]["content"][0]["text"]
    print("Usage:", usage, sep="\n", end="\n\n")
    print("Output:", output_text, sep="\n", end="\n\n", flush=True)

    # Save output data
    new_data = {
        "test_id": test_id,
        "usage": usage,
        "output_text": output_text,
        "reasoning_text": re["output"][0]["content"][0]["text"]
    }
    test_data[i]["test_results"].append(new_data)
    with open(oup, "w") as f:
        json.dump(test_data, f, indent=4)
    print("Model outputs written to", oup)
print("Fin.")