# Social preview generator

`assets/social-preview/render.py` renders a spec to a 1280x640 PNG with headless Chrome and the vendored Inter and
JetBrains Mono fonts (SIL OFL 1.1, licenses in [`fonts/`](../assets/social-preview/fonts/)). It needs only Python 3 and
Chrome or Chromium; set `CHROME` to override the binary.

From another repository, render with a shallow clone of this one:

```bash
git clone --depth 1 https://github.com/gamaware/.github /tmp/shared
python3 /tmp/shared/assets/social-preview/render.py docs/assets/social-preview.json docs/assets/social-preview.png
```

A spec is JSON with paths relative to the spec file:

```json
{
  "color": "#146C43",
  "heading": ["GitHub Actions to AWS", "without stored keys"],
  "subtitle": "OIDC · scoped deploy role · security gates",
  "steps": [
    {"label": "Trust policy", "icon": "icons/role.svg"},
    {"label": "Scoped deploy role"},
    {"label": "Gated release"}
  ],
  "illustration": "illustration.svg",
  "mark": "mark.svg"
}
```

- `heading` takes one to three lines; `steps` takes exactly three, each with an optional 48 px icon.
- `illustration` is an SVG fragment for a `0 0 728 640` viewBox. The generator adds the blueprint grid, crop marks,
  white 2.5 px round strokes and JetBrains Mono 18 px text, so the same fragments used for Upwork covers render
  unchanged. Use `#FFC34D` (amber) for the single highlighted element.
- `color` is the offer's cover color:

| Offer | Color |
| --- | --- |
| Terraform on AWS audit and fix | `#844FBA` |
| CI/CD pipeline to AWS | `#146C43` |
| AWS security and IAM review | `#232F3E` |
| Kubernetes on Amazon EKS | `#2356C2` |
| Containerize and deploy to ECS Fargate | `#A6400E` |
| AWS landing zone for a new project | `#0B5563` |
| DevOps and Well-Architected assessment | `#2B2F77` |
| AWS cost optimization audit | `#5E4A12` |
| Migration to AWS | `#7B1F6A` |
| AWS workshop and mentoring | `#9E1C2F` |

`make preview` regenerates this repository's own preview from
[`examples/github.json`](../assets/social-preview/examples/github.json).
