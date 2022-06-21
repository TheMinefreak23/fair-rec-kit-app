<template>
  <div class="tree-menu">
    <b-card class="border-end-0 border-top-0 border-bottom-0 border-5 bg-secondary">
      <b-card-title>{{label}} 
        <b-button v-b-toggle='label.replace(" ", "_")' variant="secondary">
          <span class="when-open"><i class="bi bi-caret-up" /></span>
          <span class="when-closed"><i class="bi bi-caret-down" /></span>
        </b-button>
      </b-card-title>
      <!-- v-if because if there is no description -> undefined, which takes space. -->    
      <b-collapse :id='label.replace(" ", "_")' class="collapse show">
        <tree-menu 
          v-for="node in nodes" 
          :nodes="node.nodes" 
          :label="node.label"
          :depth="depth+1"
        >
        </tree-menu>
      
        <b-card-text v-if='itemDicts[label]["description"]'>
          <span v-html='itemDicts[label]["description"]'></span>
        </b-card-text>
      </b-collapse>     
    </b-card> 
  </div>
</template>
<script>
export default { 
  props: [ 'label', 'nodes' ],
  name: 'tree-menu'
}
import { doctext } from './documentation_items.vue'
import { ref } from 'vue'

const collapse =ref([])
let itemDicts = ref();

itemDicts = parse(doctext);

/**
 * Parses the content of documentation_items.txt into items.
 * @param {String} text - documentation_items.txt as one string.
 * @return {[Dict]} Array of items represented as a dictionary.
 */
function parse(text) {
  let stringItems = parseTextIntoItems(text);
  let items = {};
  for (let i = 0; i< stringItems.length; i++) {
    let idict = parseItem(stringItems[i]);
    items[idict["name"]] = idict;
  }
  return items;
}

/**
 * Parses documents_items.txt into an array of items.
 * @param {String} text - The whole content of documents_items.txt as one String.
 * @return {[String]} An array of strings of items: ["<name>...</name>\n<description>...</description>", "..."].
 */
function parseTextIntoItems(text) {
  // An item is defined as anything between -{...}- as defined in documents_items.txt
  let items = [];
  let item = "";
  let readItem = false;
  let textLines = text.split("\n");

  for (let j = 0;  j < textLines.length; j++) {
    // Parse each sentence
    let line = textLines[j];
    for (let i = 0; i < line.length; i++) {
      let character = line[i];
      if (character + line[i+1] == "-{") {
        readItem = true;
        i += 1;
        continue;
      }
      if (character + line[i+1] == "}-") {
        readItem = false;
        items.push(item);
        item = ""
      }
      if (readItem) {
        item += character;
      }
    }
    item += "\n";
  }
  return items
}

/**
 * Parses an item into a dictionary so that it can be referred to as e.g., dict["name"], dict["description"].
 * @param {String} item - An item as a string: "<name>...</name>\n<description>...</description>".
 * @return {Dict} Dictionary of an item as key, value: dict["name"] = "Algorithm 123".
 */
function parseItem(item) {
  let dict = {};
  let key = "";
  let value = "";
  let keytagFound = false; // Prevents nested tags.
  let itemLines = item.split("\n");
  for (let j = 0; j < itemLines.length; j++) {
    let words = itemLines[j].split(" ");
    for (let i = 0; i < words.length; i++) {
      let word = words[i];
      if (word.match(/<.*>/)) {
        const endTag = new RegExp("</" + key + ">", 'g'); // Ending tag e.g., </name>.
        if (word.match(endTag)) {
          value = value.slice(0, -1); // Remove trailing whitespace.
          dict[key] = value;
          key = "";
          value = "";
          keytagFound = false;
          i -= 1;
        }
        // Starting tag e.g., <name>.
        else if (!keytagFound && word.match(/<[^\/].*>/)) {
          keytagFound = true;
          key = word.match(/(?<=<).*(?=>)/)[0];
          value = "";
          continue;
        }
      }
      if (key) { value += word + " "; }
    }
    value += "\n";
  }
  return dict;
}

</script>

<style>
  .collapsed > .when-open {
    display: none;
  }
  :not(.collapsed) > .when-closed {
    display: none;
  }
</style>