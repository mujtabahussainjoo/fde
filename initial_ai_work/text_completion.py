import os

from openai import OpenAI, OpenAIError


def translate_to_hindi() -> None:
	input_lang = "English"
	output_lang = "Hindi"
	try:
		sentence = input(f"Enter your sentence in {input_lang} to convert into {output_lang}: ").strip()
	except (EOFError, KeyboardInterrupt):
		print("\nInput cancelled.")
		return

	if not sentence:
		print("Please enter a sentence.")
		return


	client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")

	try:
		result = client.chat.completions.create(
			model="llama-3.1-8b-instant",
			messages=[
				{"role": "system", "content": f"Translate from {input_lang} to {output_lang}."},
				{"role": "user", "content": sentence},
			],
		)
		translation = result.choices[0].message.content
		print(f"Hindi translation: {translation}")
	except OpenAIError as error:
		print(f"Translation request failed: {error}")


def main() -> None:
	if not os.environ.get("GROQ_API_KEY"):
		raise RuntimeError("Set the GROQ_API_KEY environment variable before running this script.")

	try:
		prompt = input("Ask a question: ").strip()
	except (EOFError, KeyboardInterrupt):
		print("\nInput cancelled.")
		return

	if not prompt:
		print("Please enter a question.")
		return

	client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
	try:
		for temperature in (0.2, 0.5, 0.8):
			result = client.chat.completions.create(
				model="llama-3.1-8b-instant",
				messages=[
					{"role": "system", "content": "Answer in complete, clear sentences."},
					{"role": "user", "content": prompt},
				],
				temperature=temperature,
			)
			print(f"Temperature {temperature}: {result.choices[0].message.content}")
	except OpenAIError as error:
		print(f"API request failed: {error}")
		return


if __name__ == "__main__":
	translate_to_hindi()
	main()