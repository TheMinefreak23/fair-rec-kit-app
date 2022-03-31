<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Poject course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Documentation tab which shows all algorithms, metrics, datasets, etc. and their meaning.
*/

import { ref } from 'vue'

let doctext = ref('');

/**
 * Has to be changed to internal file selector: no user input needed.
 */
function previewFile() {
  const content = document.querySelector('.content');
  const [file] = document.querySelector('input[type=file]').files;
  const reader = new FileReader();

  // Temporary Main
  reader.addEventListener("load", () => {
    // this will then display a text file
    doctext = reader.result;
    content.innerText = doctext;
    // console.log(doctext);
    console.log(parse(doctext));
  }, false);

  if (file) {
    reader.readAsText(file);
  }
}

/**
 * Parses the content of documentation_items.txt into items.
 * @param {String} text - documentation_items.txt as one string.
 * @return {[Dict]} Array of items represented as a dictionary.
 */
function parse(text) {
  let stringItems = parseTextIntoItems(text);
  let items = [];
  for (let i in stringItems) {
    items.push(parseItem(stringItems[i]));
  }
  return items;
}

/**
 * Parses documents_items.txt into an array of items.
 * @param {String} text - The whole content of documents_items.txt as one String.
 * @return {[String]} An array of strings of items: ["<name>...</name>\n<description>...</description>", "..."].
 */
function parseTextIntoItems(text) {
  // An item is defined as anything between {} as defined in documents_items.txt
  let items = [];
  let item = "";
  let readItem = false;
  // Parse into items
  for (let i in text) {
    let character = text[i];
    // console.log(character);
    if (character == "{") {
      readItem = true;
      continue;
    }
    if (character == "}") {
      readItem = false;
      items.push(item);
      item = ""
    }
    if (readItem) {
      item += character;
    }
  }
  return items
}

/**
 * Parses an item into a dictionary so that it can be referred to as e.g., dict["name"], dict["definition"].
 * @param {String} item - An item as a string: "<name>...</name>\n<description>...</description>".
 * @return {Dict} Dictionary of an item as key, value: dict["name"] = "Algorithm 123".
 */
function parseItem(item) {
  let dict = {};
  let key = "";
  let value = "";
  let itemWords = item.split(/\s/);
  for (let i in itemWords) {
    let word = itemWords[i];
    if (word.match(/(?<=<).*(?=>)/)) {
      // Ending element e.g., </name>.
      if (word.match(/\/.*/)) {
        value = value.slice(0, -1); // Remove trailing whitespace.
        dict[key] = value;
        key = "";
        value = "";
      }
      // Starting element e.g., <name>.
      else {
        key = word.match(/(?<=<).*(?=>)/);
        continue;
      }
    }
    if (key) { value += word + " "; }
  }
  return dict;
}


</script>

<template>
  <div class="text-center py-2 mx-5">
    <h3>Documentation</h3>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea.</p>
  </div>
  
  <input type="file" v-on:change=previewFile()><br>
  <p class="content"></p>
  
  
</template>


