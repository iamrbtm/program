from docquery import document, pipeline

def test():
    p = pipeline.get_pipeline()
    doc = document.load_document("/Users/rbtm2006/Library/CloudStorage/OneDrive-UniversityofthePeople/2023/2023-T1/PHIL 1402/Unit 1/1. Learning Guide/2375350.pdf")
    for q in ["what impulses does a mans life divide between?"]:
        print(q, p(question=q, **doc.context))

if __name__ == "__main__":
    test()