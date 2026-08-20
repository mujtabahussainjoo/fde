"""Practice embeddings, collections, and semantic search with ChromaDB."""

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# The default all-MiniLM-L6-v2 model creates one vector with 384 numbers.
EMBEDDING_DIMENSIONS = 384


def main():
    # Creates a temporary in-memory database; data is deleted when the program stops.
    # This creates the temporary Chroma database environment.
    # It is like opening a temporary database server or storage system in memory.
    # It creates the database connection.
    # It does not store documents yet.
    # Data disappears when the program ends.
    # It can contain multiple collections.
    client = chromadb.EphemeralClient()
    # DefaultEmbeddingFunction is provided by Chroma; this variable name is chosen by us.
    # We could call it text_encoder or my_embedding_function instead.
    embedding_function = DefaultEmbeddingFunction()

    custom_text = "Chroma stores text as searchable vectors."
    # The function expects a list of texts and returns one embedding per text.
    # [0] selects the first embedding from the returned list.
    custom_embedding = embedding_function([custom_text])[0]

    print(f"Embedding length: {len(custom_embedding)}")
    # Stop the program if the selected model does not produce 384 dimensions.
    assert len(custom_embedding) == EMBEDDING_DIMENSIONS
    print("Confirmed: the embedding has 384 dimensions.")
    # This creates a named collection inside the database.
    # A collection is similar to a table or folder where related documents and embeddings are stored.
    # client is the database environment.
    # my_collection is one storage area inside that environment.
    # Documents are inserted using .add().
    my_collection = client.create_collection(
        # Create a named storage area for related documents and their vectors.
        # `name` is a predefined Chroma parameter; "my_collection" is our custom value.
        # Other common create_collection parameters are `metadata`, `configuration`,
        # `embedding_function`, and `data_loader`.
        name="my_collection",
        # This is another predefined parameter receiving our local variable.
        # Chroma can use it to create embeddings automatically during queries or inserts.
        embedding_function=embedding_function,
    )
    # Uses Chroma's default distance configuration.
    # In current Chroma versions, this is generally l2 distance.
    # Stores documents and embeddings.
    # You display its data using .peek().
    # You do not perform a semantic query on it in this script.




    # These are the text documents that we want to store and search later.
    documents = ["document one", "document two", "document three"]
    # Each document needs its own unique ID inside the collection.
    document_ids = ["id1", "id2", "id3"]
    # Convert all three documents into numerical vectors for semantic search.
    document_embeddings = embedding_function(documents)

    # Store the IDs, original text, and matching embeddings together.
    my_collection.add(
        # These are predefined add() parameters; their values and variable names are ours.
        # Common optional parameters include `metadatas` for labels or extra information.
        ids=document_ids,
        documents=documents,
        embeddings=document_embeddings,
    )

    # Show a small preview of the data currently stored in the collection.
    print("\nmy_collection preview:")
    print(my_collection.peek())

    # Create another collection that compares vectors using cosine similarity.
    cosine_collection = client.create_collection(
        name="cosine_collection",
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=embedding_function,
    )

    # Uses an HNSW search index.
    # Explicitly compares vectors using cosine distance.
    # Is used for semantic searches.
    # Finds documents with similar meaning, even when exact words differ.



    # Store two documents that can be compared with a meaning-based search.
    cosine_collection.add(
        ids=["id1", "id2"],
        documents=[
            "Big cats such as lions, tigers, and leopards are powerful wild animals.",
            "The solar system contains the Sun, planets, moons, asteroids, and comets.",
        ],
    )

    # Search for one document whose meaning is related to wildlife.
    wildlife_result = cosine_collection.query(
        # `query_texts` and `n_results` are predefined query() parameters.
        # Other common parameters include `query_embeddings`, `where`, `where_document`,
        # and `include` to filter results or choose returned fields.
        query_texts=["Animals living in the wild"],
        n_results=1,
    )

    # The first [0] selects the first query; the second [0] selects its best result.
    print("\nWildlife search result:")
    print(wildlife_result["documents"][0][0])

    # Add two more documents to the same collection using new unique IDs.
    cosine_collection.add(
        ids=["id3", "id4"],
        documents=[
            "The internal combustion engine was a groundbreaking invention "
            "that paved the way for the modern automobile.",
            "The North Pole is among the coldest places on the planet, home to "
            "polar bears, seals, and penguins.",
        ],
    )

    # Search for the car-related document without copying its exact wording.
    car_result = cosine_collection.query(
        query_texts=["A machine that changed transportation through fuel-powered travel"],
        n_results=1,
    )

    # Print the single best matching document returned by the semantic search.
    print("\nCar-related search result:")
    print(car_result["documents"][0][0])


# Run main() only when this file is executed directly, not when imported.
if __name__ == "__main__":
    main()
