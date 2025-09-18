import time
from . import chunk_text

def benchmark_chunker(text, chunk_size, overlap, method):
    print(f"Benchmarking {method} chunker...")
    t0 = time.time()
    chunks = chunk_text(text, chunk_size, overlap, method)
    t1 = time.time()
    lens = [len(c["text"]) for c in chunks]
    print(f"Total Chunks: {len(chunks)}")
    print(f"Avg Chunk Size: {sum(lens)/len(lens):.1f}")
    print(f"Min/Max Chunk Size: {min(lens)}/{max(lens)}")
    print(f"Time Taken: {t1-t0:.4f}s")
    print("Sample metadata:", chunks[0]["meta"] if chunks else None)
    print("--- Sample chunk ---")
    if chunks:
        print(chunks[0]["text"][:200])
    print("-" * 40)

if __name__ == "__main__":
  
    text = ("This is a sample paragraph. " * 20 + "\n\n") * 100
    benchmark_chunker(text, chunk_size=300, overlap=50, method="fixed")
    benchmark_chunker(text, chunk_size=300, overlap=0, method="semantic")