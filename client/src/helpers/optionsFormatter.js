const emptyOption = { name: 'Choose...', value: null }

// Full selection options with first default empty option
function selectionOptions(options) {
  return [emptyOption, ...options]
}

/**
 * Returns an empty formgroup
 * @return {object} A javascript object with the required fields
 */
function emptyFormGroup(required) {
  return {
    visible: required, // Show option if it is required
    // For required lists the minimum amount of group items is 1.
    groupCount: required ? 1 : 0,
    choices: [{}],
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

/**
 * Format null values if the parameter value is a list
 * @param {Object} paramValue - the default parameter value
 * @returns the values with a null string instead of undefined value
 */
function formatDefault(paramValue) {
  if (Array.isArray(paramValue) && paramValue.length > 1) {
    const nullIndex = paramValue.indexOf(null)
    if (nullIndex) paramValue[nullIndex] = 'null'
  }
  return paramValue
}

// Change the form format into a data format
function reformat(property) {
  const formattedChoices = []
  for (const i in property.choices) {
    const choices = property.choices[i]
    // console.log('reformat', choices)
    if (choices.main) {
      // Direct settings (inputs/selects)
      let params = []
      if (choices.inputs) params = params.concat(choices.inputs)
      if (choices.selects) params = params.concat(choices.selects)
      formattedChoices[i] = {
        name: choices.main.name,
        params,
      }
      // Nested formgrouplists
      if (choices.lists != null) {
        for (const list of choices.lists) {
          // console.log('list', list)
          if (list.choices[0].single) {
            // formgroup not list
            // TODO refactor
            // If it is a single form group, take the first (and thus last) single option in the list
            formattedChoices[i][list.choices[0].name] = reformat(list)[0]
            /* console.log(
              i,
              list.choices[0].name,
              formattedChoices[i][list.choices[0].name]
            ) */
          } else formattedChoices[i][list.name] = reformat(list)
          // console.log('list', formattedChoices[i][list.name])
        }
      }
    }
  }
  return formattedChoices
}

export {
  emptyOption,
  selectionOptions,
  validateEmail,
  emptyFormGroup,
  formatDefault,
  reformat,
}
