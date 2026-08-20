import os

from openai import OpenAI


def main() -> None:
	if not os.environ.get("GROQ_API_KEY"):
		raise RuntimeError("Set the GROQ_API_KEY environment variable before running this script.")

	prompt = input("Ask a question: ").strip()
	if not prompt:
		raise ValueError("A question is required.")

	client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
	result = client.chat.completions.create(
		model="llama-3.1-8b-instant",
		messages=[{"role": "user", "content": prompt}],
	)
	print(result.choices[0].message.content)


if __name__ == "__main__":
	main()