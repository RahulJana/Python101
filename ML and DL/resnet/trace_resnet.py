"""Trace a tensor through the ResNet built in resnet.py.

Shows, per block: input shape, F(x) shape, shortcut type (identity vs projection),
and output shape. Then checks that gradients actually reach the stem.
"""

import torch
from resnet import resnet50, BasicBlock, Bottleneck


def trace(model, x):
    print(f"{'block':<22} {'input':<20} {'shortcut':<26} {'output':<20}")
    print("-" * 92)
    print(f"{'stem (7x7 s2 + pool)':<22} {str(tuple(x.shape)):<20} {'—':<26} ", end="")
    h = model.maxpool(model.relu(model.bn1(model.conv1(x))))
    print(f"{str(tuple(h.shape)):<20}")

    n_id = n_proj = 0
    for stage_i, stage in enumerate([model.layer1, model.layer2,
                                     model.layer3, model.layer4], start=1):
        for block_i, blk in enumerate(stage):
            cin = tuple(h.shape)
            out = blk(h)

            if blk.downsample is None:
                short = "identity (raw copy)"
                n_id += 1
            else:
                # the 1x1 conv inside the downsample Sequential
                conv = blk.downsample[0]
                short = f"1x1 conv s{conv.stride[0]}  {conv.in_channels}→{conv.out_channels}"
                n_proj += 1

            name = f"layer{stage_i}.{block_i}"
            print(f"{name:<22} {str(cin):<20} {short:<26} {str(tuple(out.shape)):<20}")
            h = out

    h = model.avgpool(h)
    print(f"{'avgpool + fc':<22} {str(tuple(h.shape)):<20} {'—':<26} ", end="")
    y = model.fc(torch.flatten(h, 1))
    print(f"{str(tuple(y.shape)):<20}")

    print("-" * 92)
    print(f"identity shortcuts: {n_id}   projection shortcuts: {n_proj}   "
          f"(one projection per stage + the layer1 width change)")
    return y


def _strip_skips(model):
    """Rebind every block's forward to drop the shortcut -> a 'plain' net."""
    def plain_forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        return self.relu(out)                     # note: no `+ identity`
    for m in model.modules():
        if isinstance(m, Bottleneck):
            m.forward = plain_forward.__get__(m, Bottleneck)
    return model


def _stage_grads(model, x):
    model.zero_grad()
    model(x).sum().backward()
    # probe the first conv of the first block of each stage, deep -> shallow
    probes = [("stem.conv1", model.conv1),
              ("layer1.0.conv1", model.layer1[0].conv1),
              ("layer2.0.conv1", model.layer2[0].conv1),
              ("layer3.0.conv1", model.layer3[0].conv1),
              ("layer4.0.conv1", model.layer4[0].conv1)]
    return [(n, p.weight.grad.abs().mean().item()) for n, p in probes]


def check_gradients():
    """Compare gradient flow: ResNet vs the same net with skips removed.

    NOTE: zero_init_residual must be OFF here. With bn3.gamma = 0, the gradient
    w.r.t. conv3 is exactly 0 at init (correct, but it makes the comparison
    meaningless). Real training escapes that within a step or two.
    """
    torch.manual_seed(0)
    x = torch.randn(2, 3, 224, 224)

    res = resnet50(zero_init_residual=False).train()
    torch.manual_seed(0)
    plain = _strip_skips(resnet50(zero_init_residual=False).train())

    g_res, g_plain = _stage_grads(res, x), _stage_grads(plain, x)

    print(f"\nmean |grad| per probe, shallow → deep")
    print(f"{'probe':<18} {'with skips':>13} {'skips removed':>15}")
    print("-" * 50)
    for (n, a), (_, b) in zip(g_res, g_plain):
        print(f"{n:<18} {a:>13.3e} {b:>15.3e}")

    spread_r = g_res[0][1] / g_res[-1][1]
    spread_p = g_plain[0][1] / g_plain[-1][1]
    print("-" * 50)
    print(f"shallow/deep spread  with skips : {spread_r:>10,.0f}x")
    print(f"shallow/deep spread  no skips   : {spread_p:>10,.0f}x")
    print(f"skips shrink the spread by      : {spread_p / spread_r:>10,.1f}x")
    print(
        "\nRead this carefully — it is NOT the textbook vanishing-gradient picture:\n"
        "  * Gradients here get LARGER toward the stem, not smaller. At random init\n"
        "    with BatchNorm, BN already rescales activations per layer and prevents\n"
        "    the classic exponential decay. BN alone does a lot of the work.\n"
        "  * So the honest claim is about IMBALANCE, not vanishing: without skips the\n"
        "    gradient magnitude across depth is far more lopsided. Skips pull the\n"
        "    layers closer to a common scale, which is what makes the optimisation\n"
        "    well-conditioned enough to train 50+ layers.\n"
        "  * The real degradation ResNet fixed shows up over TRAINING, not at init —\n"
        "    a plain 56-layer net converges to worse TRAINING error than a 20-layer\n"
        "    one. A single backward pass can't show that; only a training run can."
    )


def zero_init_demo():
    """At init with zero_init_residual, every block starts as a pure identity."""
    m = resnet50().eval()
    blk = m.layer1[1]                       # identity-shortcut block
    x = torch.randn(1, 256, 56, 56)
    with torch.no_grad():
        f = blk.bn3(blk.conv3(blk.relu(blk.bn2(blk.conv2(
            blk.relu(blk.bn1(blk.conv1(x))))))))
        out = blk(x)
    print(f"\nzero_init_residual check on layer1.1:")
    print(f"  max |F(x)| at init : {f.abs().max().item():.6f}  (bn3 gamma is zeroed)")
    print(f"  output == relu(x)? : {torch.allclose(out, torch.relu(x), atol=1e-5)}")
    print("  -> block is born a perfect pass-through; it only learns to deviate.")


if __name__ == "__main__":
    torch.manual_seed(0)
    model = resnet50().eval()
    x = torch.randn(1, 3, 224, 224)

    with torch.no_grad():
        trace(model, x)

    zero_init_demo()
    check_gradients()
