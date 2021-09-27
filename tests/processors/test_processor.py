from rhoknp.processors.processor import Processor


def test_processor_apply():
    processor = Processor(None)
    try:
        processor.apply(None)
    except NotImplementedError:
        pass
    except Exception:
        raise Exception
