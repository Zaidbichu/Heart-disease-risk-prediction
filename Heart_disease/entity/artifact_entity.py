from dataclasses import dataclass
@dataclass
class Dataingestionartifact:
    raw_data_path:str
    train_file_path:str
    test_file_path:str