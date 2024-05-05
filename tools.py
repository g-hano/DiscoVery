import os
import fitz
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
import logging

from PIL import Image
import ollama
from io import BytesIO

DIRNAME = "Extracted"
def PDFExtractor(path: str) -> dict:
    print(f"====== PDFExtractor used ======")
    pairs = {}
    path = os.path.normpath(path)
    path = path.replace("\\","/")
    
    try:
        doc = fitz.open(path)
        print(f"Opened document: {path}")
    except Exception as e:
        print(f"Failed to open document: {e}")
        return {}

    for page_n, page in enumerate(doc):
        img_list = page.get_images(full=True)
        text = page.get_text()
        for idx, img in enumerate(img_list):
            xref = img[0]
            base_img = doc.extract_image(xref)
            img_bytes = base_img["image"]
            img_ext = base_img["ext"]
            img_file_name = f"{DIRNAME}/image{page_n+1}_{idx+1}.{img_ext}"
            
            try:
                with open(img_file_name, "wb") as img_file:
                    img_file.write(img_bytes)
                    print("Saved image to", img_file_name)
            except Exception as e:
                print(f"Failed to save image: {e}")
                continue

            pairs[img_file_name] = text
    doc.close()
    return pairs


def AskVisionModel(content) -> str:
    def read_images_from_folder_as_bytes(folder_path='Extracted'):
        images_bytes = []
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        if not os.path.exists(folder_path):
            print(f"Error: Directory {folder_path} does not exist.")
            return images_bytes
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(supported_formats):
                img_path = os.path.join(folder_path, filename)
                try:
                    with Image.open(img_path) as img:
                        byte_arr = BytesIO()
                        img.save(byte_arr, format=img.format)
                        images_bytes.append(byte_arr.getvalue())
                        print(f"Loaded image as bytes: {img_path}")
                except IOError as e:
                    print(f"Failed to load image {img_path}: {e}")
        return images_bytes

    print(f"====== AskVisionModel used ======")
    images = read_images_from_folder_as_bytes()

    with open("llava_prompt.txt", "r") as f:
        prompt = f.readlines()

    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": content,
                "images": images
            }
        ]
    )
    
    return response["message"]["content"] 


def StructuredFileReader(question: str) -> str:
    logging.info("====== DirectoryReader used ======")
    allowed_extensions = [".csv", ".txt", ".xlsx", ".xls"]
    documents = SimpleDirectoryReader(DIRNAME, required_exts=allowed_extensions).load_data(show_progress=True)

    Settings.chunk_size = 512
    Settings.chunk_overlap = 50
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")

    index = VectorStoreIndex.from_documents(
        documents,
    )

    query_engine = index.as_query_engine(similarity_top_k=4, llm=llm)

    return query_engine.query(question)


def Report(analysis: str):
    try:
        with open("analysis.txt", "w") as f:
            f.write(analysis)
        print("Succesfully saved")
    except Exception:
        print("Exception Occurred: ", Exception)