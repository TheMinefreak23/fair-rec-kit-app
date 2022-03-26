<script setup>
import { computed, ref } from 'vue'
import sortBy from 'just-sort-by';
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

const props = defineProps({
  results: Array,
  headers: Array,
})

const subheaders = computed(() => {
    const result = [];

    for (const header of props.headers) {
        if (header.subheaders) {
            result.push(...header.subheaders);
        } else {
            result.push('');
        }
    }

    return result;
});

const sorted = computed(() => sort(sortindex.value))

const sortindex = ref(0)
const descending = ref(false)

function sort(i){
    const res = sortBy(props.results, function(o){
        return Object.values(o)[i]
    } )
    
    if(descending.value){
        return res.reverse()
    }
    return res
}

function setsorting(i){
    if(i === sortindex.value){
        descending.value = !descending.value
    }
    sortindex.value = i
}

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
                    style="cursor: pointer;"
                    @click="setsorting(index)"
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
                v-for="(item, index) in sorted"
                :key="`item-${index}`"
            >
                <b-td
                    v-for="[key, value] in Object.entries(item)"
                    :key="`${descending}_${sortindex}_${index}-${key}`"
                >
                    {{ value }}
                </b-td>
            </b-tr>
        </b-tbody>
    </b-table-simple>
</template>


