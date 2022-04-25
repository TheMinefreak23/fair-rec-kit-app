const emptyOption = { text: 'Choose...', value: { params: [] } }

// Full selection options with first default empty option
function selectionOptions(options) {
  return [emptyOption, ...options]
}

export { emptyOption, selectionOptions }
