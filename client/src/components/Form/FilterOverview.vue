<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { underscoreToSpace, capitalise } from '../../helpers/resultFormatter'
import { reformat } from '../../helpers/optionsFormatter'

defineProps({ filters: Object })
</script>

<template>
  <b-list-group>
    <template v-if="reformat(filters).length === 0">
      No filters selected
    </template>
    <b-list-group-item v-for="f in reformat(filters)">
      <b>{{ capitalise(underscoreToSpace(f.name)) }}</b>
      <p>
        {{
          f.params
            .map(
              (p) =>
                underscoreToSpace(p.name) +
                ': ' +
                (p.name === 'range'
                  ? 'min: ' + p.value.min + ' max: ' + p.value.max
                  : p.value)
            )
            .join(', ')
        }}
      </p>
    </b-list-group-item>
  </b-list-group>
</template>
