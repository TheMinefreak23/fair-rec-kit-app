<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Poject course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Documentation tab which shows all algorithms, metrics, datasets, etc. and their meaning.
*/

import { ref } from 'vue'
import { structure } from '../documentation/documentation_structure.vue'
import { doctext } from '../documentation/documentation_items.vue'

// hardcoded documentation_items.txt
let itemDicts = ref();
let sidenavOpened = ref();
sidenavOpened = false;

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
  console.log(items);
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
  console.log(dict);
  return dict;
}

/**
 * Recursive .
 * @param {} text 
 * @param {*} start_i 
 */
function parseStructure(text, start_i) {
  eval("let x=1;");
  console.log(x);
  // let itemName = ""
  // for (let i = start_i; i < text.length; i++) {
  //   let c = text[i];
  //   if (c == "{") {
  //     i = parseStructure(text.slice(i, text.length), i);
  //   }
  //   else if (c =="}") {
  //     return i;
  //   }
  //   else {
  //     itemName += c;
  //   }
  // }
}
// function 


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

pre {
  background-color: #eee;
  border: 1px solid #999;
  display: block;
  padding: 5px;
  margin: 5px;
}
pre {
  counter-reset: line;
}
code {
  counter-increment: line;
}
code:before {
  content: counter(line);
  margin-right: 30px;
  -webkit-user-select: none;
  color: gray;
}

</style>

<template>
<div id="main">
  <span class="position-fixed" style="font-size:30px;cursor:pointer" v-on:click="openCloseNav()">&#9776;</span>
  <div id="docSidenav" class="sidenav">
    <!-- <a href="javascript:void(0)" class="closebtn position-fixed-left" v-on:click="closeNav()">&times;</a> -->
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
