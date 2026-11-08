import torch


def set_seed(seed: int = 42) -> None:
    """<<vi:Cố định seed để kết quả tái hiện được.||en:Fix the seed so results can be reproduced.>>"""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


if __name__ == "__main__":
    set_seed()
    print(torch.rand(3))
