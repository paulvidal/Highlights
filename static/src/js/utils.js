export function toUpperCase(str) {
  return str.replace(/(^|\s)\S/g, l => l.toUpperCase())
}