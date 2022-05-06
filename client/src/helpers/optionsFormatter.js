const emptyOption = { name: 'Choose...', value: null }

// Full selection options with first default empty option
function selectionOptions(options) {
  return [emptyOption, ...options]
}


function emptyFormGroup(required) {
  return {
    // For required lists the minimum amount of group items is 1.
    groupCount: required ? 1 : 0,
    main: [],
    inputs: [],
    selects: [],
    lists: [],
  }
}

export { emptyOption, selectionOptions, emptyFormGroup }
