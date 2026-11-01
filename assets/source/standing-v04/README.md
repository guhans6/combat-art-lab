# v04 sneaker details

`standing.aseprite` is the separate native candidate based on v03. Only existing opaque pixels of `04-sneakers` were revised. The other 11 layers, alpha silhouette, grid and palette are unchanged.

From the repository root, with output folders present:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v04/detail-shoes.lua"
```

The script opens v03, checks other layer images, saves/reopens v04 and exports it. No raster reference is copied into the sprite. See the [record and checks](../../../docs/experiments/2026-10-26-shoe-detail/record.md).
