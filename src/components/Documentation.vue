<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Poject course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Documentation tab which shows all algorithms, metrics, datasets, etc. and their meaning.
*/

import { ref } from 'vue'

let doctexthard = 
`Item list for in documentation tab
Only lines within curly brackets in the following format are read:

{
<name> sometext abcdef </name>
<definition> sometext abcdef </definition>
<link> sometext abcdef </link>
<other1> sometext abcdef </other1>
<other?> sometext abcdef </other?>
}

blabla I'm just a comment...
Documentation items:
{
<name> test1 algorithm </name>
<definition> test1 is a blablabla. </definition>
<link> https://www.hiiii.com </link>
<other1> extendable. </other1>
I'm also a comment actually.
}

{
<name> LFM2B </name>
<definition> Last FM 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation and. 
Next. paragraph.

Paragraph with extra newline.
</definition>
<link> Retrieval.eeeeeeee </link>
<other1> http://www.cp.jku.at/datasets/LFM-2b/ </other1>
}

Datasets:
{
<name> LFM2B </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> LFM1B </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> LFM360K </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> ML25M </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> ML100K </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

------

Recommender approaches:

Elliot:
{
<name> FunkSVD </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> ItemKNN </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> MultiVAE </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> MostPop </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> PureSVD </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Random </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> SVDpp </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> UserKNN </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

Implicit:
{
<name> AlternatingLeastSquares </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> BayesianPersonalizedRanking </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> LogisticMatrixFactorization </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

Lenskit:
{
<name> BiasedMF </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> ImplicitMF </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> PopScore </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Random</name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}
`;
let itemDicts = ref();

/**
 * Has to be changed to internal file selector: no user input needed.
 */
function previewFile() {
  const content = document.querySelector('.content');
  const [file] = document.querySelector('input[type=file]').files;
  const reader = new FileReader();
  
  // Temporary Main
  reader.addEventListener("load", () => {
    let doctext = "";
    // this will then display a text file
    doctext = reader.result;
    itemDicts.value = parse(doctext);
    console.log(itemDicts);
  }, false);

  if (file) {
    reader.readAsText(file);
  }
}
itemDicts = parse(doctexthard);
console.log(itemDicts);
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
  <!-- b-sidebar -->
  <div class="text-center py-2 mx-5">
    <h3>Documentation</h3>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea.</p>
  </div>

  <input type="file" v-on:change=previewFile()><br>
  <p class="content"></p>
  
  <div v-for="itemDict in itemDicts" :key="itemDict">
    <b-card>
      <b-card-title>{{ itemDict["name"] }}</b-card-title>
      <b-card-text>{{ itemDict["definition"] }}</b-card-text>
      <b-link :href='itemDict["link"]'>{{ itemDict["link"] }}</b-link>
      <br>
      <b-button :href='itemDict["other?"]' v-if='itemDict["other?"]'>
        {{ itemDict["other?"] }}
      </b-button>
    </b-card>
  </div>
</template>
