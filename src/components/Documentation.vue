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
`# Documentation items
Item list for in documentation tab
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
WebApp to compare different recommender approaches. Developed by RecCoons, from Utrecht University.
</definition>
<link> http://fairreckit.science.uu.nl/ </link>
}

-----
Tabs:

{
<name> New Computation </name>
<definition>
<p>In this tab you can start a new computation of your desired datasets and the recommender approach. There are a few well-known datasets built-in, but custom datasets can be uploaded as well. After having chosen the datasets, one or more filters can be applied wat doet dit?.</p>
<p>Next, add the recommender approaches that you want compared and select the number of recommendation per user wat doet dit?. Then, the train-test ratio and the different metrics to compare the performance.</p>
<p>Lastly, enter the metadata to identify your computation. After pressing Send, this data will be added to the queue in Active Computations and send to the server to be executed.</p>
<p>For more information about each step, refer to the list below:</p>
<ul>
<li><a href="#LFM2B">Datasets</li>
<li><a href="#LFM2B">Filters</li>
<li><a href="#FunkSVD">Recommender approaches</li>
<li><a href="###">Train/test-split</li>
<li><a href="tabIndex=1">Metrics</li>
<li><a href="#">Meta</li>
</ul>
</definition>
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
<name> Ra2ndom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

-----

Metrics:
http://www.cp.jku.at/datasets/LFM-2b/

{
<name> Ran2dom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Rando2m </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> R2andom </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

{
<name> Random2 </name>
<definition> sometext </definition>
<link> sometext </link>
<other1> sometext </other1>
<other?> sometext </other?>
}

`;
let itemDicts = ref();
let sidenavOpened = ref();
sidenavOpened = false;

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
  let items = {};
  for (let i in stringItems) {
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

/**
 * Navigation sidebar toggle collapse
 */
function openCloseNav() {
  if (sidenavOpened) {
    closeNav();
  }
  else {
    openNav();
  }
}
function openNav() {
  sidenavOpened = true;
  document.getElementById("docSidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}
function closeNav() {
  sidenavOpened = false;
  document.getElementById("docSidenav").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
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

.sidenav {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  transition: 0.5s;
  padding-top: 60px;
}

.sidenav a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 15px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

.sidenav a:hover {
  color: #f1f1f1;
}

.sidenav .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

#main {
  transition: margin-left .5s;
  padding: 16px;
}

@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}
</style>

<template>
<div id="main">
  <span class="position-fixed" style="font-size:30px;cursor:pointer" v-on:click="openCloseNav()">&#9776;</span>
  <div id="docSidenav" class="sidenav">
    <a href="javascript:void(0)" class="closebtn" v-on:click="closeNav()">
      <div class="position-fixed">&times;</div>
    </a>
    <b-link class="position-relative" :href='"#"+itemDict["name"]' v-for="itemDict in itemDicts" :key="itemDict">{{itemDict["name"]}}</b-link>
  </div>
  
  <div class="text-right py-1 mx-5" v-for="itemDict in itemDicts" :key="itemDict">
    <b-card :id='itemDict["name"]'>
      <b-card-title>{{ itemDict["name"] }}</b-card-title>
      <b-card-text>
        <!-- Uses HTML syntax -->
        <span v-html='itemDict["definition"]'></span>
      </b-card-text>
      <b-link :href='itemDict["link"]'>{{ itemDict["link"] }}</b-link>
      <b-button :href='itemDict["other?"]' v-if='itemDict["other?"]'>
        <br>
        {{ itemDict["other?"] }}
      </b-button>
    </b-card>    
  </div>
</div>
</template>
