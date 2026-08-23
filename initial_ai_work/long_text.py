import base64
import os

from openai import OpenAI, OpenAIError

def main() -> None:
	if not os.environ.get("OPENROUTER_API_KEY"):
		raise RuntimeError("Set the OPENROUTER_API_KEY environment variable before running this script.")

	try:
		prompt = input("Ask a question: ").strip()
	except (EOFError, KeyboardInterrupt):
		print("\nInput cancelled.")
		return

	if not prompt:
		print("Please enter a question.")
		return

	client = OpenAI(
		api_key=os.environ["OPENROUTER_API_KEY"],
		base_url="https://openrouter.ai/api/v1",
	)
	try:
		result = client.images.generate(
			model="openai/gpt-image-1",
			prompt=prompt,
			size="1024x1024",
			output_format="png",
		)
		image_data = result.data[0].b64_json
		if not image_data:
			raise RuntimeError("The API did not return image data.")

		with open("generated_image.png", "wb") as image_file:
			image_file.write(base64.b64decode(image_data))
		print("Image saved to generated_image.png")
	except OpenAIError as error:
		print(f"API request failed: {error}")
		return


if __name__ == "__main__":
	main()