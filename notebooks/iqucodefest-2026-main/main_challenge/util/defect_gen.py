"""
Synthetic grayscale defect images.

Convention: 0 = white, 1 = black.
- Normal pixels live in `normal_range` (default 0.3-0.5) -> mid grey.
- Defect pixels live in `defect_range` (default 0.95-0.99) -> near black.
A defective sample has exactly ONE defect blob of one of `shapes`.
Everything is driven by a seed, so the same args -> the same dataset.
"""

import numpy as np

# (height, width) of each allowed defect -> 1px, 4px(2x2), 6px(2x3 / 3x2)
DEFECT_SHAPES = [(1, 1), (2, 2), (2, 3), (3, 2)]


def make_image(rng, size=8, normal_range=(0.3, 0.5),
               defect_range=(0.95, 0.99), defect=None):
    """One image. `defect` = (h, w) shape, or None for a clean sample."""
    img = rng.uniform(*normal_range, size=(size, size))
    if defect is not None:
        h, w = defect
        if h > size or w > size:
            raise ValueError(f"defect {defect} doesn't fit in {size}x{size}")
        r = int(rng.integers(0, size - h + 1))
        c = int(rng.integers(0, size - w + 1))
        img[r:r + h, c:c + w] = rng.uniform(*defect_range, size=(h, w))
    return img


def generate_dataset(n_samples=100, size=8, defect_rate=0.10,
                     normal_range=(0.3, 0.5), defect_range=(0.95, 0.99),
                     shapes=DEFECT_SHAPES, seed=42):
    """
    Returns (images, labels):
      images: (n_samples, size, size) float array
      labels: (n_samples,) int array, 1 = defective, 0 = clean
    Exactly round(defect_rate * n_samples) samples get a single defect.
    """
    rng = np.random.default_rng(seed)
    n_defect = round(defect_rate * n_samples)
    defect_idx = set(rng.choice(
        n_samples, size=n_defect, replace=False).tolist())

    images = np.empty((n_samples, size, size), dtype=float)
    labels = np.zeros(n_samples, dtype=int)

    for i in range(n_samples):
        if i in defect_idx:
            shape = shapes[int(rng.integers(len(shapes)))]
            images[i] = make_image(
                rng, size, normal_range, defect_range, defect=shape)
            labels[i] = 1
        else:
            images[i] = make_image(rng, size, normal_range, defect_range)

    print("### Dataset generation complete ###")
    print(f"Total samples: {n_samples}")
    print(f"Image size: {size}x{size}")
    print(f"Number of normal images: {(labels == 0).sum()}")
    print(f"Number of defective images: {labels.sum()}")
    print("### ### ###  ### ### ### ### ### ### ### ### ###\n")
    return images, labels


def show_samples(images, labels, n_show=12, cols=6, save=None):
    """Quick visual check. 0=white,1=black -> cmap='gray_r'."""
    import matplotlib.pyplot as plt

    # show a mix: some defective first if available, then clean
    order = list(np.argsort(-labels))[:n_show]
    rows = int(np.ceil(len(order) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 1.4, rows * 1.6))
    for ax, idx in zip(np.ravel(axes), order):
        ax.imshow(images[idx], cmap='gray_r', vmin=0, vmax=1)
        ax.set_title(f"#{idx} {'DEFECT' if labels[idx] else 'clean'}",
                     fontsize=8, color='crimson' if labels[idx] else 'black')
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in np.ravel(axes)[len(order):]:
        ax.axis('off')
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=120, bbox_inches='tight')

    plt.show()
    # return fig


# if __name__ == "__main__":
#     imgs, lbls = generate_dataset(
#         n_samples=50, size=8, defect_rate=0.10, seed=42)
#     print(f"images: {imgs.shape}, defects: {lbls.sum()}/{len(lbls)}")

#     # prove reproducibility
#     imgs2, _ = generate_dataset(
#         n_samples=50, size=8, defect_rate=0.10, seed=42)
#     print("same seed identical:", np.array_equal(imgs, imgs2))

#     show_samples(imgs, lbls, n_show=12, save="samples.png")
#     print("saved samples.png")
