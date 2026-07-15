"""
ResNet from scratch — Deep Residual Learning for Image Recognition (He et al., 2015).

Everything is built up from nn.Conv2d / nn.BatchNorm2d. No torchvision models.

Layout of an ImageNet ResNet:

    stem:    7x7 conv s2  ->  BN  ->  ReLU  ->  3x3 maxpool s2      224 -> 56
    stage 1: N blocks @  64 base ch,  stride 1                       56 -> 56
    stage 2: N blocks @ 128 base ch,  stride 2 (first block)         56 -> 28
    stage 3: N blocks @ 256 base ch,  stride 2 (first block)         28 -> 14
    stage 4: N blocks @ 512 base ch,  stride 2 (first block)         14 -> 7
    head:    global avg pool -> fc                                    7 -> 1

The only thing that changes between ResNet-18/34/50/101/152 is which block
type is used and how many blocks sit in each stage.
"""

from typing import List, Type, Union

import torch
import torch.nn as nn


def conv3x3(cin: int, cout: int, stride: int = 1) -> nn.Conv2d:
    """3x3 conv with padding=1 so spatial size is preserved when stride=1."""
    # bias=False everywhere: the BatchNorm right after has its own beta shift,
    # so a conv bias would be redundant (and immediately cancelled by BN).
    return nn.Conv2d(cin, cout, kernel_size=3, stride=stride, padding=1, bias=False)


def conv1x1(cin: int, cout: int, stride: int = 1) -> nn.Conv2d:
    """1x1 conv — mixes channels, touches no spatial neighbours."""
    return nn.Conv2d(cin, cout, kernel_size=1, stride=stride, bias=False)


# --------------------------------------------------------------------------- #
#  Blocks
# --------------------------------------------------------------------------- #

class BasicBlock(nn.Module):
    """Two 3x3 convs. Used by ResNet-18 and ResNet-34.

        x ─┬─► conv3x3 ─ BN ─ ReLU ─ conv3x3 ─ BN ─► (+) ─► ReLU
           └──────────── shortcut ──────────────────┘
    """

    expansion = 1  # out_channels = base_channels * expansion

    def __init__(self, cin: int, base: int, stride: int = 1,
                 downsample: nn.Module = None):
        super().__init__()
        cout = base * self.expansion

        self.conv1 = conv3x3(cin, base, stride)   # stride lives on the FIRST conv
        self.bn1 = nn.BatchNorm2d(base)
        self.conv2 = conv3x3(base, cout)
        self.bn2 = nn.BatchNorm2d(cout)

        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample  # None => identity shortcut

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x                                  # <- the shortcut lane

        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))               # no ReLU yet: add first

        if self.downsample is not None:
            identity = self.downsample(x)             # 1x1 conv projection

        out = out + identity                          # F(x) + x
        return self.relu(out)                         # ReLU *after* the add


class Bottleneck(nn.Module):
    """1x1 squeeze -> 3x3 spatial -> 1x1 expand. Used by ResNet-50/101/152.

    The 3x3 (the expensive one) runs on a narrow tensor, so depth gets cheap.
    Output width is base*4, e.g. base=64 -> 256 channels out.
    """

    expansion = 4

    def __init__(self, cin: int, base: int, stride: int = 1,
                 downsample: nn.Module = None):
        super().__init__()
        cout = base * self.expansion

        self.conv1 = conv1x1(cin, base)             # squeeze channels
        self.bn1 = nn.BatchNorm2d(base)
        self.conv2 = conv3x3(base, base, stride)    # spatial work, stride here (v1.5)
        self.bn2 = nn.BatchNorm2d(base)
        self.conv3 = conv1x1(base, cout)            # expand back out
        self.bn3 = nn.BatchNorm2d(cout)

        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x

        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))             # last BN, still no ReLU

        if self.downsample is not None:
            identity = self.downsample(x)

        out = out + identity
        return self.relu(out)


# --------------------------------------------------------------------------- #
#  Network
# --------------------------------------------------------------------------- #

class ResNet(nn.Module):
    def __init__(self,
                 block: Type[Union[BasicBlock, Bottleneck]],
                 layers: List[int],
                 num_classes: int = 1000,
                 zero_init_residual: bool = True):
        super().__init__()
        self.block = block
        self.cin = 64  # running channel count, mutated by _make_stage

        # --- stem: 224 -> 56 -------------------------------------------------
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # --- four stages -----------------------------------------------------
        self.layer1 = self._make_stage(block, 64,  layers[0], stride=1)
        self.layer2 = self._make_stage(block, 128, layers[1], stride=2)
        self.layer3 = self._make_stage(block, 256, layers[2], stride=2)
        self.layer4 = self._make_stage(block, 512, layers[3], stride=2)

        # --- head ------------------------------------------------------------
        self.avgpool = nn.AdaptiveAvgPool2d(1)  # any HxW -> 1x1
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        self._init_weights(zero_init_residual)

    def _make_stage(self, block, base: int, n_blocks: int, stride: int) -> nn.Sequential:
        """Build one stage. Only the FIRST block may stride / change width."""
        downsample = None
        cout = base * block.expansion

        # A projection shortcut is needed exactly when the block changes shape:
        # either it downsamples (stride != 1) or the width changes (cin != cout).
        if stride != 1 or self.cin != cout:
            downsample = nn.Sequential(
                conv1x1(self.cin, cout, stride),
                nn.BatchNorm2d(cout),
            )

        blocks = [block(self.cin, base, stride, downsample)]
        self.cin = cout  # every later block in this stage sees cout channels in

        # Remaining blocks: stride 1, cin == cout, so shortcut is a free identity.
        for _ in range(1, n_blocks):
            blocks.append(block(self.cin, base))

        return nn.Sequential(*blocks)

    def _init_weights(self, zero_init_residual: bool):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        # Zero the LAST BN gamma in every block => F(x) starts at exactly 0,
        # so each block begins life as a clean identity. Worth ~0.5-1% top-1.
        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck):
                    nn.init.constant_(m.bn3.weight, 0)
                elif isinstance(m, BasicBlock):
                    nn.init.constant_(m.bn2.weight, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.maxpool(self.relu(self.bn1(self.conv1(x))))   # [B,  64, 56, 56]
        x = self.layer1(x)                                     # [B, 256, 56, 56] (bneck)
        x = self.layer2(x)                                     # [B, 512, 28, 28]
        x = self.layer3(x)                                     # [B,1024, 14, 14]
        x = self.layer4(x)                                     # [B,2048,  7,  7]
        x = self.avgpool(x)                                    # [B,2048,  1,  1]
        return self.fc(torch.flatten(x, 1))                    # [B, num_classes]


# --------------------------------------------------------------------------- #
#  Standard variants — only the block type and stage depths differ
# --------------------------------------------------------------------------- #

def resnet18(num_classes=1000, **kw):  return ResNet(BasicBlock, [2, 2, 2, 2], num_classes, **kw)
def resnet34(num_classes=1000, **kw):  return ResNet(BasicBlock, [3, 4, 6, 3], num_classes, **kw)
def resnet50(num_classes=1000, **kw):  return ResNet(Bottleneck, [3, 4, 6, 3], num_classes, **kw)
def resnet101(num_classes=1000, **kw): return ResNet(Bottleneck, [3, 4, 23, 3], num_classes, **kw)
def resnet152(num_classes=1000, **kw): return ResNet(Bottleneck, [3, 8, 36, 3], num_classes, **kw)


if __name__ == "__main__":
    torch.manual_seed(0)

    # Official param counts (torchvision, 1000 classes) to check against.
    reference = {
        "resnet18": 11_689_512, "resnet34": 21_797_672, "resnet50": 25_557_032,
        "resnet101": 44_549_160, "resnet152": 60_192_808,
    }

    x = torch.randn(2, 3, 224, 224)
    print(f"{'model':<10} {'params':>12} {'expected':>12}  {'out shape':<14} match")
    print("-" * 62)
    for name, fn in [("resnet18", resnet18), ("resnet34", resnet34),
                     ("resnet50", resnet50), ("resnet101", resnet101),
                     ("resnet152", resnet152)]:
        m = fn().eval()
        with torch.no_grad():
            y = m(x)
        n = sum(p.numel() for p in m.parameters())
        ok = "OK" if n == reference[name] else "MISMATCH"
        print(f"{name:<10} {n:>12,} {reference[name]:>12,}  {str(tuple(y.shape)):<14} {ok}")
