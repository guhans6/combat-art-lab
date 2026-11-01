# Modular shop v01
Native master: shop.aseprite, 208x240, one frame, sixteen semantic layers, existing 97-entry palette.
This is a camera-specific facade derived from the prior converted/cleaned shop, with authored board, pot, stems and hidden window/timber repairs. It is not an independently painted replacement or a complete building elevation.
shop-pass01.aseprite retains the first extraction. shop-lamp-edit.aseprite is a duplicate-only twenty-pixel light revision.
construction-final-rle.json is the final pixel input: palette plus bottom-to-top named layers, each encoded as [run length, palette index] over row-major 208x240 pixels. Decode each layer to rows and use Aseprite MCP grid drawing with a legend; skip transparent pixels on an empty cel. Earlier construction-rle.json and the small-planter operation are intermediate checkpoints, not final reconstruction inputs.
Runtime exports: ../../export/shop-modular-v01. Each part has a trimmed PNG and atlas retaining its master-canvas offset. parts-layout.json consolidates offsets. Native source remains the revision master.
