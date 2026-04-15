export interface BufferedRect {
  top: number;
  bottom: number;
  left: number;
  right: number;
}

export const doRectsOverlap = (a: DOMRect | BufferedRect, b: DOMRect | BufferedRect) => {
  return !(
    a.right < b.left ||
    a.left > b.right ||
    a.bottom < b.top ||
    a.top > b.bottom
  );
};

export const getRectWithBuffer = (rect: DOMRect, buffer: number): BufferedRect => {
  return {
    top: rect.top - buffer,
    bottom: rect.bottom + buffer,
    left: rect.left - buffer,
    right: rect.right + buffer,
  }
}
