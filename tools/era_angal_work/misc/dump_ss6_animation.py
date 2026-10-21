import sys

import UnityPy


def value_text(value):
    if hasattr(value, "x") and hasattr(value, "y"):
        z = getattr(value, "z", None)
        return f"({value.x},{value.y}{',' + str(z) if z is not None else ''})"
    if hasattr(value, "__dict__"):
        return str(value.__dict__)
    return str(value)


def keys(attribute):
    result = []
    for status, value in zip(attribute.ListStatus, attribute.ListValue):
        result.append((status >> 15, status & 0x7FFF, value_text(value)))
    return result


bundle = sys.argv[1]
animation_name = sys.argv[2]
env = UnityPy.load(bundle)
scene = next(o.read() for o in env.objects if o.type.name == "MonoBehaviour" and getattr(o.read(), "m_Name", "") == "scene")
animation = next(a for a in scene.ListDataAnimation if a.Name == animation_name)
print(f"{animation.Name}: {animation.CountFrame} frames @ {animation.FramePerSecond} fps")
for index, part in enumerate(animation.ListAnimationParts):
    if any(getattr(part, attr).ListStatus for attr in ("Position", "Rotation", "Scaling", "RateOpacity", "Priority")) or part.Status.ListStatus != [0]:
        print(f"\n{index}: {scene.ListDataParts[index].Name}")
        for label, attr in (("status", part.Status), ("pos", part.Position), ("rot", part.Rotation), ("scale", part.Scaling), ("opacity", part.RateOpacity), ("priority", part.Priority)):
            ks = keys(attr)
            if ks:
                print(label, ks[:10], "... total", len(ks))
