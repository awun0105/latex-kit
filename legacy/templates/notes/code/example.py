import torch


def set_seed(seed: int = 42) -> None:
    """Cố định seed để kết quả tái hiện được."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


if __name__ == "__main__":
    set_seed()
    print(torch.rand(3))
