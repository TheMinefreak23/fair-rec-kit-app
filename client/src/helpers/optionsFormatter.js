const emptyOption = { name: 'Choose...', value: null }

// Full selection options with first default empty option
function selectionOptions(options) {
  return [emptyOption, ...options]
}

function emptyFormGroup(required) {
  return {
    visible: required, // Show option if it is required
    // For required lists the minimum amount of group items is 1.
    groupCount: required ? 1 : 0,
    choices: [{}],
    /*main: [],
    inputs: [],
    selects: [],
    lists: [],*/
  }
}

/**
 * Checks if Email is valid
 * @param {string} email
 * @return {bool} Whether or not the string is valid E-mail adress
 */
function validateEmail(email) {
  if (email == null) {
    return false
  } else {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    )
  }
}

export { emptyOption, selectionOptions, validateEmail, emptyFormGroup }
