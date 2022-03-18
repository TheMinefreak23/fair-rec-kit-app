<script setup>
import { computed, ref } from 'vue'
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Playground component: Shows off a couple Vue 3 + Bootstrap 5 features.
Check out https://vuejs.org/examples 
and https://getbootstrap.com/docs/5.0/getting-started/introduction/ for more
*/
const props = defineProps({
  results: Array,
  headers: Array,

})



const results = ref([{
    dataset: 'LFM-1b',
    algorithm: 'ALS',
    fst_female: '6.7717',
    fst_male: '0.6142',
    hellinger_distance: '0.0988',
    precision_p1: '0.4505',
}, {
    dataset: 'LFM-1b',
    algorithm: 'POP',
    fst_female: '0.1325',
    fst_male: '1.7299',
    hellinger_distance: '0.1577',
    precision_p1: '0.1033',
}]);

const headers = ref([{ name: 'dataset' }, { name: 'algorithm' }, {
    name: 'avg_position',
    subheaders: ['fst_female', 'fst_male'],
}, { name: 'hellinger_distance' }, { name: 'precision_p1' }]);

const subheaders = computed(() => {
    const result = [];

    for (const header of headers.value) {
        if (header.subheaders) {
            result.push(...header.subheaders);
        } else {
            result.push('');
        }
    }

    return result;
});
</script>

<template>
    <b-table-simple
        hover
        striped
        responsive
    >
        <b-thead head-variant="dark">
            <b-tr>
                <b-th
                    v-for="(header, index) in headers"
                    :key="`header-${index}`"
                    :colspan="header.subheaders ? header.subheaders.length : 1"
                >
                    {{ header.name }}
                </b-th>
            </b-tr>
            <b-tr>
                <b-th
                    v-for="(subheader, index) in subheaders"
                    :key="`subheader-${index}`"
                >
                    {{ subheader }}
                </b-th>
            </b-tr>
        </b-thead>
        <b-tbody>
            <b-tr
                v-for="(item, index) of results"
                :key="`item-${index}`"
            >
                <b-td
                    v-for="[key, value] in Object.entries(item)"
                    :key="`${index}-${key}`"
                >
                    <b-td>
                        {{ value }}
                    </b-td>
                </b-td>
            </b-tr>
        </b-tbody>
    </b-table-simple>
</template>


