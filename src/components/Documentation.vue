<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Poject course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Documentation tab which shows all algorithms, metrics, datasets, etc. and their meaning.
*/

import { ref } from 'vue'

// hardcoded documentation_items.txt
let doctexthard = 
`Item list for in documentation tab
Only lines within curly brackets in the following format are read:

\curlybracket-open
<name> sometext abcdef </name>
<definition> Uses HTML syntax </definition>
<link> sometext abcdef </link>
<other1> sometext abcdef </other1>
Some comment...
<other?> sometext abcdef </other?>
\curlybracket-closed

Adding new <tags> should be manually added to Documentation.vue's template.

=================================================

{
<name> FairRecKit </name>
<definition> 
WebApp to compare different recommender approaches. Developed by RecCoons, from Utrecht University. <br>
dddsa dsfd <h1>fefs</h1>s
cdscs
<p>fsdf
fd
</p>
<br>
<h2>HTML Table</h2>

<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>


</definition>
<link> http://fairreckit.science.uu.nl/ </link>

<other1> sometext </other1>
<other?> sometext </other?>
}

-----
Tabs:

{
<name> New Computation </name>
<definition> In the this tab you can start a new computation of your desired datasets and the recommender approach. There are a few well-known datasets built-in, but custom datasets can be uploaded as well. Apply filter </definition>

<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Active Computations </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Documentation </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Results </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> All results </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}


Datasets:
{
<name> LFM2B </name>
<definition> Last FM 2 Billion dataset is a corpus of Music Listening Events for Music Recommendation. It contains more than two billion listening events, intended to be used for various music retrieval and recommendation tasks. </definition>
<link> http://www.cp.jku.at/datasets/LFM-2b/ </link>
<other1> sometext </other1>
}

{
<name> LFM1B </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> LFM360K </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> ML25M </name>
<definition> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea. </definition>
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

-----

Metrics:
http://www.cp.jku.at/datasets/LFM-2b/

{
<name> Random </name>
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
<name> Random</name>
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

// /**
//  * Has to be changed to internal file selector: no user input needed.
//  */
// function previewFile() {
//   const content = document.querySelector('.content');
//   const [file] = document.querySelector('input[type=file]').files;
//   const reader = new FileReader();
  
//   // Temporary Main
//   reader.addEventListener("load", () => {
//     let doctext = "";
//     // this will then display a text file
//     doctext = reader.result;
//     itemDicts.value = parse(doctext);
//     console.log(itemDicts);
//   }, false);

//   if (file) {
//     reader.readAsText(file);
//   }
// }

itemDicts = parse(doctexthard);

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
  console.log(items);
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
  let keytagFound = false; // Prevents nested tags
  let itemWords = item.split(/\s/);
  for (let i in itemWords) {
    let word = itemWords[i];
    if (word.match(/<.*>/)) {
      // Ending tag e.g., </name>.
      const endTag = new RegExp("</" + key + ">", 'g');
      if (word.match(endTag)) {
        value = value.slice(0, -1); // Remove trailing whitespace.
        dict[key] = value;
        key = "";
        value = "";
        keytagFound = false;
      }
      // Starting tag e.g., <name>.
      else if (!keytagFound) {
        keytagFound = true;
        key = word.match(/(?<=<).*(?=>)/)[0];
        continue;
      }
    }
    if (key) { value += word + " "; }
  }
  return dict;
}

</script>

<style>
/* Can be added in custom.scss */
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>

<template>
  <!-- b-sidebar -->
  <!-- <b-button v-b-toggle.sidebar-1>Toggle Sidebar</b-button>
    <b-sidebar id="sidebar-1" title="Sidebar" shadow>
      <div class="px-3 py-2">
        <p>
          Cras mattis consectetur purus sit amet fermentum. Cras justo odio, dapibus ac facilisis
          in, egestas eget quam. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
        </p>
        <b-img src="https://picsum.photos/500/500/?image=54" fluid thumbnail></b-img>
      </div>
    </b-sidebar> -->

  <!-- <b-button v-b-toggle.toc-sidebar>fdd</b-button>
  <b-collapse class="mt-2" id="toc-sidebar" visible>
    <b-sidebar title="Sidebar" right shadow class="py-1 py-2">
      <p>sdfdssssssssssssssssssssssssssssssssssssssf</p>ddd
    </b-sidebar>
  </b-collapse> -->
  
  <!-- <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-toggle target="sidebar"></b-navbar-toggle>
    <b-collapse id="sidebar" is-nav vertical visible right>
      <b-nav-item>fdsfd</b-nav-item>
      <b-nav-item>fdsfd</b-nav-item>
      <b-nav-item>fdsfd</b-nav-item>
    </b-collapse>
  </b-navbar> -->
  
  
  <div class="text-right py-1 mx-5" v-for="itemDict in itemDicts" :key="itemDict">
    <b-card>
      <b-card-title>{{ itemDict["name"] }}</b-card-title>
      <b-card-text>
        <!-- Uses HTML syntax -->
        <span v-html='itemDict["definition"]'></span>
      </b-card-text>
      <b-link :href='itemDict["link"]'>{{ itemDict["link"] }}</b-link>
      <br>
      <b-button :href='itemDict["other?"]' v-if='itemDict["other?"]'>
        {{ itemDict["other?"] }}
      </b-button>
    </b-card>    
  </div>
</template>
