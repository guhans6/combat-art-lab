// Browser teaching diagrams only. Original image files are never changed.
const practiceImage = new Image();
const imagePath = document.querySelector('[data-size-image]')?.dataset.sizeImage;
if (imagePath) {
  practiceImage.addEventListener('load', () => {
    document.querySelectorAll('[data-budget-lab]').forEach(setupBudgetLab);
    document.querySelectorAll('[data-framing-lab]').forEach(setupFramingLab);
    document.querySelectorAll('[data-lab-status]').forEach(node => {
      node.textContent = 'Ready. Change a control and watch what stays the same.';
    });
  });
  practiceImage.addEventListener('error', () => {
    document.querySelectorAll('[data-lab-status]').forEach(node => {
      node.textContent = 'The image could not load. The written examples below still work; open the lesson beside its assets folder.';
    });
  });
  practiceImage.src = imagePath;
}

function paintBudget(canvas, width, height) {
  const draft = document.createElement('canvas');
  draft.width = width;
  draft.height = height;
  const draftContext = draft.getContext('2d');
  draftContext.imageSmoothingEnabled = false;
  draftContext.drawImage(practiceImage, 0, 0, width, height);
  const context = canvas.getContext('2d');
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.imageSmoothingEnabled = false;
  context.drawImage(draft, 0, 0, canvas.width, canvas.height);
}

function setupBudgetLab(lab) {
  const select = lab.querySelector('select');
  const update = () => {
    const width = Number(select.value);
    const height = width * 1.5;
    paintBudget(lab.querySelector('[data-draft-canvas]'), width, height);
    paintBudget(lab.querySelector('[data-original-canvas]'), 128, 192);
    lab.querySelector('[data-draft-caption]').textContent = `Resampled draft: ${width} × ${height} source pixels.`;
    lab.querySelector('[data-budget-output]').textContent = width === 128
      ? 'Both use the same 128 × 192 source. They should match. The browser has not drawn new detail.'
      : `Both pictures occupy the same display area. The ${width} × ${height} draft has fewer source samples; enlarging those samples does not restore the lost eye or fold information.`;
  };
  select.addEventListener('change', update);
  update();
}

function setupFramingLab(lab) {
  const heightSelect = lab.querySelector('[data-character-height]');
  const scaleSelect = lab.querySelector('[data-window-scale]');
  const update = () => {
    const visibleHeight = Number(heightSelect.value);
    const windowScale = Number(scaleSelect.value);
    const canvas = lab.querySelector('canvas');
    const context = canvas.getContext('2d');
    context.fillStyle = '#e9ede2';context.fillRect(0, 0, 640, 360);
    context.fillStyle = '#d4ddcf';
    context.fillRect(40, 90, 120, 210);context.fillRect(430, 140, 155, 160);
    context.fillStyle = '#c0cbb8';context.fillRect(0, 300, 640, 60);
    context.fillStyle = '#71806b';context.fillRect(0, 300, 640, 1);
    // Verified nontransparent bounds of the copied practice image: (32,2)-(104,185).
    // Rescale this crop as a framing stand-in, not an independently drawn sprite.
    const targetWidth = visibleHeight * 72 / 183;
    context.imageSmoothingEnabled = false;
    context.drawImage(practiceImage, 32, 2, 72, 183, 245 - targetWidth / 2, 300 - visibleHeight, targetWidth, visibleHeight);
    context.strokeStyle = '#ad593c';
    context.beginPath();context.moveTo(320, 300);context.lineTo(320, 300-visibleHeight);context.stroke();
    context.font = '16px system-ui';context.fillStyle = '#243c34';
    context.fillText(`${visibleHeight} px`, 330, 300-visibleHeight/2);
    context.fillText('640 × 360 design view', 18, 29);
    const fraction = (visibleHeight / 360 * 100).toFixed(1);
    const result = `${visibleHeight} ÷ 360 = ${fraction}% of the view height. At ${windowScale}×, the window is ${640*windowScale} × ${360*windowScale} and the figure is ${visibleHeight*windowScale} display pixels tall. Its share of the view stays ${fraction}%.`;
    lab.querySelector('[data-framing-output]').textContent = result;
    canvas.setAttribute('aria-label', `Schematic 640 by 360 game view with a ${visibleHeight}-pixel-tall figure. ${result}`);
  };
  heightSelect.addEventListener('change', update);
  scaleSelect.addEventListener('change', update);
  update();
}
